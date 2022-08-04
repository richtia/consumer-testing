import pytest

from ....common import get_sql, get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_7",
        "file_names": [
            "supplier.parquet",
            "lineitem.parquet",
            "orders.parquet",
            "customer.parquet",
            "nation.parquet",
            "nation.parquet",
        ],
        "sql_query": get_sql("q7.sql"),
        "substrait_query": get_substrait_plan("query_7_plan.json"),
    }
]
