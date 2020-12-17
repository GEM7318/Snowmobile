"""
Module contains the :class:`statement.Diff` object, which is the class
associated with all tags that have :attr:`Tag.Name.anchor`='qa-diff'.
"""
from __future__ import annotations

from typing import Dict, List, Any, Set

import pandas as pd
from snowflake.connector.errors import ProgrammingError

from snowmobile.core import Connector
from snowmobile.core.configuration import schema as cfg
from snowmobile.core.df_ext.frame import Frame

from .statement import Statement


class Diff(Statement):
    """QA class for comparison of values within a table based on
    partitioning on a field.

    Attributes:
        partition_on (str):
            Column name to partition data on before comparing the
            partitioned datasets; defaults to 'src_description`.
        end_index_at (str):
            Column name that marks the last column to use as an index column
            when joining the partitioned datasets back together.
        compare_patterns (list):
            Regex patterns to match columns on that should be *included* in
            comparison (numeric columns you're running QA on).
        ignore_patterns (list):
            Regex patterns to match columns on that should be *ignored* both
            for the comparison and the index.
        generic_metric_col_nm (str):
            Column name to use for the melted field names; defaults to 'Metric'.
        compare_cols (list):
            Columns that are used in comparison once statement is executed
            and parsing is applied.
        drop_cols (list):
            Columns that are dropped once statement is executed and parsing
            is applied.
        idx_cols (list):
            Columns that are used for the index to join the data back
            together once statement is executed and parsing is applied.
        ub_raw (float):
            Maximum absolute raw difference (upper bound) that two fields
            that are being compared can differ from each other without
            causing a failure.
        ub_perc (float):
            Maximum absolute percentage difference (upper bound) that two
            comparison fields can differ from each other without causing a
            failure.

    """

    def __init__(
        self, sn: Connector = None, **kwargs,
    ):
        """Instantiates a ``qa-diff`` statement.

        Args:
            delta_column_suffix (str):
                Suffix to add to columns that comparison is being run on;
                defaults to 'Delta'.
            partition_on (str):
                Column to partition the data on in order to compare.
            end_index_at (str):
                Column name that marks the last column to use as an index
                when joining the partitioned datasets back together.
            compare_patterns (list):
                Regex patterns matching columns to be *included* in
                comparison.
            ignore_patterns (list):
                Regex patterns to match columns on that should be *ignored*
                both for the comparison and the index.
            generic_metric_col_nm (str):
                Column name to use for the melted field names; defaults to
                'Metric'.
            raw_upper_bound (float):
                Maximum absolute raw difference that two fields that are
                being compared can differ from each other without causing a
                failure.
            percentage_upper_bound (float):
                Maximum absolute percentage difference that two comparison
                fields can differ from each other without causing a failure.

        """
        super().__init__(sn=sn, **kwargs)
        # fmt: off
        qa_cfg: cfg.QA = sn.cfg.script.qa

        parsed = self.attrs_parsed

        self.partition_on: str = (
            parsed.get("partition-on", qa_cfg.partition_on)
        )
        self.end_index_at: str = (
            parsed.get("end-index-at", qa_cfg.end_index_at)
        )
        self.compare_patterns: List = (
            parsed.get("compare-patterns", qa_cfg.compare_patterns)
        )
        self.ignore_patterns: List = (
            parsed.get("ignore-patterns", qa_cfg.ignore_patterns)
        )
        self.relative_tolerance = (
            parsed.get('relative-tolerance', qa_cfg.tolerance.relative)
        )
        self.absolute_tolerance = (
            parsed.get('absolute-tolerance', qa_cfg.tolerance.absolute)
            if not self.relative_tolerance else 0
        )

        self.compare_cols: List[str] = list()
        self.drop_cols: List[str] = list()
        self.idx_cols: List[str] = list()
        self.partitions: Dict[Any, pd.DataFrame] = dict()
        self.diff: bool = bool()
        # fmt: on

    def _idx(self) -> None:
        """Isolates columns to use as indices."""
        self.idx_cols = self.results.snowmobile.cols_ending_at(
            self.end_index_at, ignore_patterns=[self.partition_on]
        )
        if not self.idx_cols:
            raise Exception(
                f"Arguments provided don't result in any index columns to join"
                f" DataFrame's partitions back together on."
            )

    def _drop(self) -> None:
        """Isolates columns to ignore/drop."""
        self.drop_cols = self.results.snowmobile.cols_matching_patterns(
            patterns=self.ignore_patterns
        )

    def _compare(self) -> None:
        """Isolate columns to use for comparison."""
        self.compare_cols = self.results.snowmobile.cols_matching_patterns(
            patterns=self.compare_patterns,
            ignore_patterns=[self.partition_on, self.idx_cols, self.drop_cols],
        )
        if not self.compare_cols:
            raise Exception(
                f"Arguments provided don't result in any comparison columns."
            )

    def split_cols(self) -> Diff:
        """Post-processes results returned from a ``qa-diff`` statement.

        Executes private methods to split columns into:
            * Index columns
            * Drop columns
            * Comparison columns

        Then runs checks needed to ensure minimum requirements are met in order
        for a valid partition/comparison to be made.

        """
        try:
            self._idx()
            self._drop()
            self._compare()
        except Exception:
            raise
        # fmt: off
        if self.partition_on not in list(self.results.columns):
            raise Exception(
                f"Column `{self.partition_on}` not found in DataFrames columns."
            )
        # fmt: on

        return self

    def drop_ignored(self) -> Diff:
        """Drops ignored columns from results."""
        if self.drop_cols:
            self.results.drop(columns=self.drop_cols, inplace=True)
        return self

    def set_index(self) -> Diff:
        """Sets index columns before partitioning results."""
        self.results.set_index(keys=self.idx_cols, inplace=True)
        return self

    @property
    def partitioned_by(self) -> Set[Any]:
        """Distinct values within the ``partition_on`` column that data is
        partitioned by.

        """
        return set(self.results[self.partition_on])

    def process(self) -> Diff:
        try:
            self.split_cols()
            self.drop_ignored()
            self.set_index()
            self.partitions = self.results.snowmobile.partitions(on=self.partition_on)
            self._outcome = self.partitions_are_equal(
                partitions=self.partitions,
                abs_tol=self.absolute_tolerance,
                rel_tol=self.relative_tolerance,
            )
            return self
        except Exception as e:
            raise e

    @staticmethod
    def partitions_are_equal(
        partitions: Dict[str, pd.DataFrame], abs_tol: float, rel_tol: float
    ) -> bool:
        """Evaluates if a dictionary of DataFrames are identical.

        Args:
            partitions (Dict[str, pd.DataFrame]):
                A dictionary of DataFrames returned by
                :meth:`snowmobile.DataFrame`.
            abs_tol (float):
                Absolute tolerance for difference in any value amongst the
                DataFrames being compared.
            rel_tol (float):
                Relative tolerance for difference in any value amongst the
                DataFrames being compared.

        Returns (bool):
            Indication of equality amongst all the DataFrames contained in
            ``partitions``.

        """
        partitions_by_index: Dict[int, pd.DataFrame] = {
            i: df for i, df in enumerate(partitions.values(), start=1)
        }
        checks_for_equality: List[bool] = [
            partitions_by_index[i].snowmobile.df_diff(
                df2=partitions_by_index[i + 1], rel_tol=rel_tol, abs_tol=abs_tol
            )
            for i in range(1, len(partitions_by_index))
        ]
        return all(checks_for_equality)

    def __getitem__(self, item):
        return vars(self)[item]

    def __setitem__(self, key, value):
        vars(self)[key] = value

    def __setattr__(self, key, value):
        vars(self)[key] = value
