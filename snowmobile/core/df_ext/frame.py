"""
Light extensions to pd.DataFrame object.
"""

import datetime
import itertools
import re
from typing import Dict, List, Optional, Tuple

import pandas as pd

from .column import Column


# DOCSTRING
@pd.api.extensions.register_dataframe_accessor("snowmobile")
class Frame:
    def __init__(self, df: pd.DataFrame):
        self._obj: pd.DataFrame = df
        self._cols: List[Column] = [Column(c) for c in self._obj.columns]
        self.cols: List[Column] = [Column(c) for c in self._obj.columns]
        self.collection: Dict[str, List] = dict()

    # noinspection PyUnresolvedReferences
    def ddl(self, table: str) -> str:
        return (
            pd.io.sql.get_schema(self._obj, table)
            .replace("CREATE TABLE", "CREATE OR REPLACE TABLE")
            .replace('"', "")
        )

    def lower_cols(self) -> pd.DataFrame:
        self._obj.rename(columns={c.prior: c.lower() for c in self.cols}, inplace=True)
        return self._obj

    def upper_cols(self) -> pd.DataFrame:
        self._obj.rename(columns={c.prior: c.upper() for c in self.cols}, inplace=True)
        return self._obj

    def reformat_cols(self):
        self._obj.rename(
            columns={c.prior: c.reformat() for c in self.cols}, inplace=True
        )
        return self._obj

    def to_list(self, col_nm: str = None, n: int = None) -> List:
        if not col_nm:
            col_nm = list(self._obj.columns)[0]
        as_list = list(self._obj[col_nm])
        return as_list if not n else as_list[n - 1]

    def add_tmstmp(self, col_nm: str = None) -> pd.DataFrame:
        col = Column(original=(col_nm or "LOADED_TMSTMP"), src="snowmobile")
        self.cols.append(col)
        self._obj[col.current] = datetime.datetime.now()
        return self._obj

    @property
    def original(self) -> pd.DataFrame:
        df: pd.DataFrame = self._obj[[c.current for c in self.cols]]
        return df.rename(columns={c.current: c.original for c in self.cols})

    def to_collection(self, collection_nm: str, cols: List[str]) -> None:
        if not self.collection.get(collection_nm):
            self.collection[collection_nm] = cols
        else:
            sub = self.collection[collection_nm]
            for c in cols:
                sub.append(c)

    def cols_matching_patterns(
        self,
        patterns: List[str],
        to_collection: str = None,
        ignore_patterns: List = None,
    ) -> List[str]:
        to_ignore = list(
            itertools.chain.from_iterable(
                p if isinstance(p, list) else [p] for p in (ignore_patterns or [])
            )
        )
        matches = [
            col
            for col in self._obj.columns
            if any(re.findall(p_incl, col) for p_incl in patterns)
            and not any(re.findall(col, p_excl) for p_excl in to_ignore)
        ]
        if to_collection and matches:
            self.to_collection(collection_nm=to_collection, cols=matches)
        return matches

    def cols_ending_at(
        self, column_nm: str, to_collection: str = None, ignore_patterns: List = None
    ) -> List[str]:
        matches = []
        ignore_patterns = ignore_patterns or []
        for i, col in enumerate(self._obj.columns, start=1):
            if col == column_nm:
                matches = [
                    c for c in list(self._obj.columns)[:i] if c not in ignore_patterns
                ]
        if to_collection:
            self.to_collection(collection_nm=to_collection, cols=matches)
        return matches

    def shared_cols(self, df2: pd.DataFrame) -> List[Tuple[pd.Series, pd.Series]]:
        """Returns list of tuples containing column pairs that are common between two DataFrames."""
        for col in set(self._obj.columns) & set(df2.columns):
            yield self._obj[col], df2[col]

    @staticmethod
    def series_max_diff_abs(col1: pd.Series, col2: pd.Series, tolerance: float) -> bool:
        """Determines if the maximum **absolute** difference between two series is within a tolerance level."""
        try:
            diff = (col1.astype(float) - col2.astype(float)).abs().max()
            return diff <= abs(tolerance)
        except TypeError as e:
            raise TypeError(e)

    @staticmethod
    def series_max_diff_rel(col1: pd.Series, col2: pd.Series, tolerance: float) -> bool:
        """Determines if the maximum **relative** difference between two
        :class:`pandas.Series` is within a tolerance level."""
        try:
            diff = ((col1.astype(float) / col2.astype(float)) - 1).abs().max()
            return diff <= abs(tolerance)
        except TypeError as e:
            raise TypeError(e)

    def df_max_diff_abs(self, df2: pd.DataFrame, tolerance: float) -> bool:
        """Determines if the maximum **absolute** difference between all columns of 2 DataFrames
        is within a tolerance level.

        """
        return all(
            self.series_max_diff_abs(col1=c[0], col2=c[1], tolerance=tolerance)
            for c in self.shared_cols(df2=df2)
        )

    def df_max_diff_rel(self, df2: pd.DataFrame, tolerance: float) -> bool:
        """Determines if the maximum **relative** difference between all columns of 2 DataFrames
        is within a tolerance level.

        """
        return all(
            self.series_max_diff_rel(col1=c[0], col2=c[1], tolerance=tolerance)
            for c in self.shared_cols(df2=df2)
        )

    def df_diff(
        self,
        df2: pd.DataFrame,
        abs_tol: Optional[float] = None,
        rel_tol: Optional[float] = None,
    ) -> bool:
        """Determines if the column-wise difference between two DataFrames is within
        a relative **or** absolute tolerance level.

        note:
            *   ``df1`` and ``df2`` are assumed to have a shared, pre-defined index.
            *   Exactly **one** of ``abs_tol`` and ``rel_tol`` is expected to be a
                a valid float; the other is expected to be **None**.
            *   If valid float values are provided for both ``abs_tol`` and ``rel_tol``,
                the outcome of the maximum **absolute** difference with respect to
                ``abs_tol`` will be returned regardless of the value of ``rel_tol``.

        Args:
            df2 (pd.DataFrame): 2nd DataFrame for comparison.
            abs_tol (float): Absolute tolerance; default is None.
            rel_tol (float): Relative tolerance; default is None.

        Returns (bool):
            Boolean indicating whether or not difference is within tolerance.

        """
        if isinstance(abs_tol, float):
            return self.df_max_diff_abs(df2=df2, tolerance=abs_tol)
        else:
            return self.df_max_diff_rel(df2=df2, tolerance=rel_tol)

    def partitions(self, on: str) -> Dict[str, pd.DataFrame]:
        """Returns a dictionary of DataFrames given a DataFrame and a partition column.

        Note:
            *   The number of distinct values within ``partition_on`` column will be
                1:1 with the number of partitions that are returned.
            *   The ``partition_on`` column is dropped from the partitions that are returned.
            *   The depth of a vertical concatenation of all partitions should equal the
                depth of the original DataFrame.

        Args:
            on (str):
                The column name to use for partitioning the data.

        Returns (Dict[str, pd.DataFrame]):
            Dictionary of {(str) partition_value: (pd.DataFrame) associated subset of df}

        """
        partitioned_by = set(self._obj[on])
        assert (
            len(partitioned_by) >= 2
        ), f"""
            DataFrame has {len(partitioned_by)} distinct values within
            '{on}' column; at least 2 required.
            """
        base_partitions = {p: self._obj[self._obj[on] == p] for p in partitioned_by}
        return {p: df.drop(columns=[on]) for p, df in base_partitions.items()}
