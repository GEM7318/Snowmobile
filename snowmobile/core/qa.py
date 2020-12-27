"""
Module contains the :class:`statement.Diff` object, which is the class
associated with all tags that have :attr:`Tag.Name.anchor`='qa-diff'.
"""
from __future__ import annotations

from typing import Any, Dict, List, Set

import pandas as pd

from . import (
    Connector,
    Statement,
    errors
)


class QA(Statement):
    """Base class for QA statements."""

    MSG = "object-specific exception message goes here."

    def __init__(self, sn: Connector, **kwargs):
        super().__init__(sn=sn, **kwargs)

    def set_outcome(self):
        """Updates ._outcome upon completion of processing invoked by .process().

        """
        # fmt: off
        if self.e.outcome in [-1, 1]:
            return self

        # -- otherwise --
        if self.outcome:  # passed QA check
            self.e.set(outcome=-3)
            self._outcome = -3
        else:             # failed QA check
            self._outcome = -2
            self.e.set(outcome=-2)
            self.e.collect(
                e=self._DERIVED_FAILURE_MAPPING[self.tag.anchor](
                    nm=self.tag.nm,
                    msg=self.MSG,
                    idx=self.index,
                    to_raise=True,
                ),
            )
        # fmt: on

        return self


class Empty(QA):
    """QA class for results expected to be empty."""

    MSG = (
        "a 'qa-empty' check did not pass its validation; this means that "
        "a query you expected to return empty results returned a non-zero "
        "number of records."
    )

    def __init__(self, sn: Connector, **kwargs):
        super().__init__(sn=sn, **kwargs)

    def process(self) -> QA:
        """Over-ride method; checks if results are empty and updates outcome"""
        self.outcome = self.results.empty
        return self.set_outcome()


class Diff(QA):
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

    MSG = (
        "a 'qa-diff' check did not pass its validation; this means that "
        "the difference in the values compared did not fall within the "
        "specified threshold."
    )

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
        self._post_parse_init()
        self.compare_cols: List[str] = list()
        self.drop_cols: List[str] = list()
        self.idx_cols: List[str] = list()
        self.partitions: Dict[Any, pd.DataFrame] = dict()
        self.diff: bool = bool()
        # fmt: on

    def _post_parse_init(self) -> None:
        """Instantiates :class:`Diff` specific attributes.

        Combines arguments declared for the statement within the sql script
        and combines with defaults from ``snowmobile.toml``.

        """
        qa_cfg = self.sn.cfg.script.qa

        self.partition_on: str = (
            self.attrs_parsed.get("partition-on", qa_cfg.partition_on)
        )
        self.end_index_at: str = (
            self.attrs_parsed.get("end-index-at", qa_cfg.end_index_at)
        )
        self.compare_patterns: List = (
            self.attrs_parsed.get("compare-patterns", qa_cfg.compare_patterns)
        )
        self.ignore_patterns: List = (
            self.attrs_parsed.get("ignore-patterns", qa_cfg.ignore_patterns)
        )
        self.relative_tolerance = self.attrs_parsed.get(
            "relative-tolerance", qa_cfg.tolerance.relative
        )
        self.absolute_tolerance = (
            self.attrs_parsed.get("absolute-tolerance", qa_cfg.tolerance.absolute)
            if not self.relative_tolerance
            else 0
        )

    def _idx(self) -> None:
        """Isolates columns to use as indices."""
        self.idx_cols = self.results.snf.cols_ending(
            self.end_index_at, ignore_patterns=[self.partition_on]
        )
        if not self.idx_cols:
            self.e.collect(
                e=errors.StatementPostProcessingError(
                    msg=(
                        f"Arguments provided don't result in any index columns "
                        f"on which to join DataFrame's partitions."
                    ),
                    to_raise=True,
                ),
            ).set(outcome=-1)

    def _drop(self) -> None:
        """Isolates columns to ignore/drop."""
        self.drop_cols = self.results.snf.cols_matching(patterns=self.ignore_patterns)

    def _compare(self) -> None:
        """Isolate columns to use for comparison."""
        self.compare_cols = self.results.snf.cols_matching(
            patterns=self.compare_patterns,
            ignore_patterns=[self.partition_on, self.idx_cols, self.drop_cols],
        )
        if not self.compare_cols:
            self.e.collect(
                e=errors.StatementPostProcessingError(
                    msg=f"Arguments provided don't result in any comparison columns."
                ),
                to_raise=True,
            ).set(outcome=-1)

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
            self.e.collect(
                e=errors.StatementPostProcessingError(
                    msg=(
                        f"Column `{self.partition_on}` not found in DataFrames columns."
                    ),
                    to_raise=True,
                ),
            ).set(outcome=-1)
        # fmt: on

        return self

    @property
    def partitioned_by(self) -> Set[Any]:
        """Distinct values within the ``partition_on`` column that data is
        partitioned by.

        """
        return set(self.results[self.partition_on])

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
            partitions_by_index[i].snf.df_diff(
                df2=partitions_by_index[i + 1], rel_tol=rel_tol, abs_tol=abs_tol
            )
            for i in range(1, len(partitions_by_index))
        ]
        return all(checks_for_equality)

    def process(self) -> Diff:
        """Post-processing for :class:`Diff`-specific results.
        """
        try:
            self.outcome = False

            self.split_cols()
            if self.drop_cols:
                self.results.drop(columns=self.drop_cols, inplace=True)
            self.results.set_index(keys=self.idx_cols, inplace=True)

            try:
                self.partitions = self.results.snf.partitions(on=self.partition_on)
            except Exception as e:
                self.e.collect(
                    e=errors.StatementPostProcessingError(
                        msg=(e.args[0]),
                        to_raise=True,
                    )
                ).set(outcome=-1)

            if self.e.outcome != -1:
                # TESTS: add test to verify what happens if this fails
                self.outcome = self.partitions_are_equal(
                    partitions=self.partitions,
                    abs_tol=self.absolute_tolerance,
                    rel_tol=self.relative_tolerance,
                )

        finally:
            # TODO: Build in a protected message argument to statement tags
            #   so a custom message can be embedded per-check to display
            #   exactly what is being tested to stdout/logs when it fails.
            return self.set_outcome()

    def __getitem__(self, item):
        return vars(self)[item]

    def __setitem__(self, key, value):
        vars(self)[key] = value

    def __setattr__(self, key, value):
        vars(self)[key] = value
