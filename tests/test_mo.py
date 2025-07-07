import os
import sys
import types
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest


class DummyCursor:
    def __init__(self):
        self.sql = None
        self.params = None

    def execute(self, sql, params=None):
        self.sql = sql
        self.params = params


class DummyConnection:
    def __init__(self):
        self.cursor_obj = DummyCursor()
        self.committed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True


# provide a minimal pymysql module for tests
dummy_pymysql = types.ModuleType("pymysql")
dummy_pymysql.connect = lambda *args, **kwargs: DummyConnection()
sys.modules.setdefault("pymysql", dummy_pymysql)

from src.core.save_to_cache.mo import MatrixOne


@patch("pymysql.connect", return_value=DummyConnection())
def test_insert_to_table(mock_connect):
    mo = MatrixOne()
    mo._insert_to_table("my_table", ["a", "b"], [1, "x"])
    assert mo.cursor.sql == "INSERT INTO my_table (a,b) VALUES (%s,%s)"
    assert mo.cursor.params == [1, "x"]
    assert mo.db.committed


@patch("pymysql.connect", return_value=DummyConnection())
def test_insert_to_table_abstract(mock_connect):
    mo = MatrixOne()
    mo._insert_to_table_abstract(["a", "b"], [1, "x"], "my_table")
    assert mo.cursor.sql == "INSERT INTO my_table (a,b) VALUES (%s,%s)"
    assert mo.cursor.params == [1, "x"]
    assert mo.db.committed
