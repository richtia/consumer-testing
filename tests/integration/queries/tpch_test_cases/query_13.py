import pytest

from ....common import get_sql, get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_13",
        "file_names": ["customer.parquet", "orders.parquet"],
        "sql_query": get_sql("q13.sql"),
        "substrait_query": get_substrait_plan("query_13_plan.json"),
    }
]
