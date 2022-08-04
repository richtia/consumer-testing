import pytest

from ....common import get_sql, get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_21",
        "file_names": [
            "supplier.parquet",
            "lineitem.parquet",
            "orders.parquet",
            "nation.parquet",
            "lineitem.parquet",
            "lineitem.parquet",
        ],
        "sql_query": get_sql("q21.sql"),
        "substrait_query": get_substrait_plan("query_21_plan.json"),
    }
]
