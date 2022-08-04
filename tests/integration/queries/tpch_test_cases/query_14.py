import pytest

from ....common import get_sql, get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_14",
        "file_names": ["lineitem.parquet", "part.parquet"],
        "sql_query": get_sql("q14.sql"),
        "substrait_query": get_substrait_plan("query_14_plan.json"),
    }
]
