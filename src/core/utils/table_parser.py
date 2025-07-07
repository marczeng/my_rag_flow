"""Utilities for parsing tables from various sources."""
from __future__ import annotations

from typing import List, Dict, Any

import pandas as pd


class TableParser:
    """Convert raw table data into structured representations."""

    def to_dataframe(self, table: List[List[Any]]) -> pd.DataFrame:
        """Return a DataFrame from a two-dimensional list."""
        if not table:
            return pd.DataFrame()
        header, *rows = table
        return pd.DataFrame(rows, columns=header)

    def to_records(self, table: List[List[Any]]) -> List[Dict[str, Any]]:
        """Return a list of row dictionaries from raw table data."""
        df = self.to_dataframe(table)
        return df.to_dict(orient="records")
