import pytest

from ....common import get_sql, get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_6",
        "file_names": ["lineitem.parquet"],
        "sql_query": get_sql("q6.sql"),
        "substrait_query": get_substrait_plan("query_6_plan.json"),
    }
]
