"""
Light extensions to pd.DataFrame object.
"""

import datetime
import itertools
import re
from typing import Dict, List, Optional, Tuple

import pandas as pd

from . import errors
from .column import Column
from . import Generic


@pd.api.extensions.register_dataframe_accessor("snf")
class SnowFrame(Generic):
    """Light extension to :class:`pandas.DataFrame` with a ``snf`` entry point.

    """

    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self._obj: pd.DataFrame = df
        self._cols: List[Column] = [Column(c) for c in self._obj.columns]
        self.cols: List[Column] = [Column(c) for c in self._obj.columns]

    def shared_cols(self, df2: pd.DataFrame) -> List[Tuple[pd.Series, pd.Series]]:
        """Returns list of tuples containing column pairs that are common between two DataFrames.
        """
        for col in set(self._obj.columns) & set(df2.columns):
            yield self._obj[col], df2[col]

    @staticmethod
    def series_max_diff_abs(col1: pd.Series, col2: pd.Series, tolerance: float) -> bool:
        """Determines if the max **absolute** difference between two
        :class:`pandas.Series` is within a tolerance level.

        """
        try:
            diff = (col1.astype(float) - col2.astype(float)).abs().max()
            return diff <= abs(tolerance)
        except TypeError as e:
            raise TypeError(e)

    @staticmethod
    def series_max_diff_rel(col1: pd.Series, col2: pd.Series, tolerance: float) -> bool:
        """Determines if the maximum **relative** difference between two
        :class:`pandas.Series` is within a tolerance level.

        """
        try:
            diff = ((col1.astype(float) / col2.astype(float)) - 1).abs().max()
            return diff <= abs(tolerance)
        except TypeError as e:
            raise TypeError(e)

    def df_max_diff_abs(self, df2: pd.DataFrame, tolerance: float) -> bool:
        """Determines if the maximum **absolute** difference between any value
        in the shared columns of 2 DataFrames is within a tolerance level.

        """
        return all(
            self.series_max_diff_abs(col1=c[0], col2=c[1], tolerance=tolerance)
            for c in self.shared_cols(df2=df2)
        )

    def df_max_diff_rel(self, df2: pd.DataFrame, tolerance: float) -> bool:
        """Determines if the maximum **relative** difference between any value
        in the shared columns of 2 DataFrames is within a tolerance level.

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
        """Determines if the column-wise difference between two DataFrames is
        within a relative **or** absolute tolerance level.

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
        if len(partitioned_by) < 2:
            raise errors.SnowFrameInternalError(
                msg=(
                    f"Found one distinct value, '{list(partitioned_by)[0]}' "
                    f"within '{on}' column of DataFrame. A minimum of 2 is required."
                )
            )
        base_partitions = {p: self._obj[self._obj[on] == p] for p in partitioned_by}
        return {p: df.drop(columns=[on]) for p, df in base_partitions.items()}

    # noinspection PyUnresolvedReferences
    def ddl(self, table: str) -> str:
        """Returns a string containing 'create table' DDL given a table name"""
        return (
            pd.io.sql.get_schema(self._obj, table)
            .replace("CREATE TABLE", "CREATE OR REPLACE TABLE")
            .replace('"', "")
        )

    def lower(self, col: Optional[str] = None) -> pd.DataFrame:
        """Lower cases all column names **or** all values within `col` if provided."""
        if col:
            self._obj[col] = self._obj[col].apply(lambda x: str(x).lower())
        else:
            self._obj.rename(
                columns={c.prior: c.lower() for c in self.cols}, inplace=True
            )
        return self._obj

    def upper(self, col: Optional[str] = None) -> pd.DataFrame:
        """Upper cases all column names **or** all values within `col` if provided."""
        if col:
            self._obj[col] = self._obj[col].apply(lambda x: str(x).lower())
        else:
            self._obj.rename(
                columns={c.prior: c.upper() for c in self.cols}, inplace=True
            )
        return self._obj

    def reformat(self):
        """Re-formats DataFrame's columns via :class:`Column.reformat()`."""
        self._obj.rename(
            columns={c.prior: c.reformat() for c in self.cols}, inplace=True
        )
        return self._obj

    def append_dupe_suffix(self):
        """Adds a trailing index number '_i' to duplicate column names."""
        cols = pd.Series(self._obj.columns)
        for dupe_col in cols[cols.duplicated()].unique():
            dupe_indices = cols[cols == dupe_col].index.values.tolist()
            cols[dupe_indices] = [
                f"{dupe_col}_{i}" if i != 0 else dupe_col
                for i in range(sum(cols == dupe_col))
            ]
        self._obj.columns = cols

    def to_list(self, col: Optional[str] = None, n: Optional[int] = None) -> List:
        """Succinctly retrieves a column as a list.

        Args:
            col (str):
                Name of column.
            n (int):
                Number of records to return; defaults to full depth of column.

        """
        if not col:
            col = list(self._obj.columns)[0]
        as_list = list(self._obj[col])
        return as_list if not n else as_list[n - 1]

    def add_tmstmp(self, col_nm: Optional[str] = None) -> pd.DataFrame:
        """Adds a column containing the current timestamp to a DataFrame.

        Args:
            col_nm (str):
                Name for column; defaults to `LOADED_TMSTMP`.

        """
        col = Column(original=(col_nm or "LOADED_TMSTMP"), src="snowmobile")
        self.cols.append(col)
        self._obj[col.current] = datetime.datetime.now()
        return self._obj

    @property
    def original(self) -> pd.DataFrame:
        """Returns the DataFrame in its original form (drops columns added by
        :class:`SnowFrame` and reverts to original column names).

        """
        df: pd.DataFrame = self._obj[
            [c.current for c in self.cols if c.src == "original"]
        ]
        return df.rename(columns={c.current: c.original for c in self.cols})

    @property
    def has_dupes(self) -> bool:
        """DataFrame has duplicate column names."""
        return len(set(self._obj.columns)) != len(list(self._obj.columns))

    def cols_matching(
        self, patterns: List[str], ignore_patterns: List[str] = None
    ) -> List[str]:
        """Returns a list of columns given a list of patterns to find.

        Args:
            patterns (List[str]):
                List of regex patterns to match columns on.
            ignore_patterns (List[str]):
                Optional list of regex patterns to exclude.

        Returns (List[str]):
            List of columns found/excluded.

        """
        to_ignore = list(
            itertools.chain.from_iterable(
                p if isinstance(p, list) else [p] for p in (ignore_patterns or [])
            )
        )
        return [
            col
            for col in self._obj.columns
            if any(re.findall(p_incl, col) for p_incl in patterns)
            and not any(re.findall(col, p_excl) for p_excl in to_ignore)
        ]

    def cols_ending(self, nm: str, ignore_patterns: Optional[List] = None) -> List[str]:
        """Returns all columns up to ``nm`` in a DataFrame.

        Args:
            nm (str):
                Name of column to end index at.
            ignore_patterns (List[str]):
                Optional list of regex patterns to exclude in the list that's
                returned; primarily used to for getting `end-index-at` list
                while excluding `src_description`.

        Returns (List[str]):
            List of column names matching criterion.

        """
        matches = []
        ignore_patterns = ignore_patterns or []
        for i, col in enumerate(self._obj.columns, start=1):
            if col == nm:
                matches = [
                    c
                    for c in list(self._obj.columns)[:i]
                    if not any(list(re.findall(p, c)) for p in ignore_patterns)
                ]
        return matches
