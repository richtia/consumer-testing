import pytest

from ....common import get_sql, get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_22",
        "file_names": ["customer.parquet", "customer.parquet", "orders.parquet"],
        "sql_query": get_sql("q22.sql"),
        "substrait_query": get_substrait_plan("query_22_plan.json"),
    }
]
