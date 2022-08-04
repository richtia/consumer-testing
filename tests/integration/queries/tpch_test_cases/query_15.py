import pytest

from ....common import get_sql, get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_15",
        "file_names": [
            "supplier.parquet",
            "lineitem.parquet",
            "lineitem.parquet",
        ],
        "sql_query": get_sql("q15.sql"),
        "substrait_query": get_substrait_plan("query_15_plan.json"),
    }
]
