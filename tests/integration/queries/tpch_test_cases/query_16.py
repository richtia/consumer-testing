import pytest

from ....common import get_sql, get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_16",
        "file_names": ["partsupp.parquet", "part.parquet", "supplier.parquet"],
        "sql_query": get_sql("q16.sql"),
        "substrait_query": get_substrait_plan("query_16_plan.json"),
    }
]
