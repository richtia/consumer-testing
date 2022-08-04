import pytest

from ....common import get_sql, get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_10",
        "file_names": [
            "customer.parquet",
            "orders.parquet",
            "lineitem.parquet",
            "nation.parquet",
        ],
        "sql_query": get_sql("q10.sql"),
        "substrait_query": get_substrait_plan("query_10_plan.json"),
    }
]
