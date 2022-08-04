import pytest

from ....common import get_sql, get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_17",
        "file_names": ["lineitem.parquet", "part.parquet", "lineitem.parquet"],
        "sql_query": get_sql("q17.sql"),
        "substrait_query": get_substrait_plan("query_17_plan.json"),
    }
]
