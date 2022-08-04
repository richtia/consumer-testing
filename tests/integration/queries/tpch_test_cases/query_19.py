import pytest

from ....common import get_sql, get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_19",
        "file_names": ["lineitem.parquet", "part.parquet"],
        "sql_query": get_sql("q19.sql"),
        "substrait_query": get_substrait_plan("query_19_plan.json"),
    }
]
