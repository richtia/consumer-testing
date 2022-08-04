import pytest

from ....common import get_sql, get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_18",
        "file_names": [
            "customer.parquet",
            "orders.parquet",
            "lineitem.parquet",
            "lineitem.parquet",
        ],
        "sql_query": get_sql("q18.sql"),
        "substrait_query": get_substrait_plan("query_18_plan.json"),
    }
]
