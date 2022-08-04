import pytest

from ....common import get_sql, get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_8",
        "file_names": [
            "part.parquet",
            "supplier.parquet",
            "lineitem.parquet",
            "orders.parquet",
            "customer.parquet",
            "nation.parquet",
            "nation.parquet",
            "region.parquet",
        ],
        "sql_query": get_sql("q8.sql"),
        "substrait_query": get_substrait_plan("query_8_plan.json"),
    }
]
