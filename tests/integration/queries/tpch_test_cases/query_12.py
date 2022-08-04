import pytest

from ....common import get_sql, get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_12",
        "file_names": ["orders.parquet", "lineitem.parquet"],
        "sql_query": get_sql("q12.sql"),
        "substrait_query": get_substrait_plan("query_12_plan.json"),
    }
]
