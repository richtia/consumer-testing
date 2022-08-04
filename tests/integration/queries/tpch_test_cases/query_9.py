import pytest

from ....common import get_sql, get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_9",
        "file_names": [
            "part.parquet",
            "supplier.parquet",
            "lineitem.parquet",
            "partsupp.parquet",
            "orders.parquet",
            "nation.parquet",
        ],
        "sql_query": get_sql("q9.sql"),
        "substrait_query": get_substrait_plan("query_9_plan.json"),
    }
]
