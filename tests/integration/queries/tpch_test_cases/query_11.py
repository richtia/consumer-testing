import pytest

from ....common import get_sql, get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_11",
        "file_names": [
            "partsupp.parquet",
            "supplier.parquet",
            "nation.parquet",
            "partsupp.parquet",
            "supplier.parquet",
            "nation.parquet",
        ],
        "sql_query": get_sql("q11.sql"),
        "substrait_query": get_substrait_plan("query_11_plan.json"),
    }
]
