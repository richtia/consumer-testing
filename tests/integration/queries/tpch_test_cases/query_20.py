import pytest

from ....common import get_sql, get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_20",
        "file_names": [
            "supplier.parquet",
            "nation.parquet",
            "partsupp.parquet",
            "part.parquet",
            "lineitem.parquet",
        ],
        "sql_query": get_sql("q20.sql"),
        "substrait_query": get_substrait_plan("query_20_plan.json"),
    }
]
