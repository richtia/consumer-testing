import pytest
from ....common import get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_6",
        "file_names": ["lineitem_1.parquet"],
        "sql_query":
            """
            SELECT
                sum(l_extendedprice * l_discount) AS revenue
            FROM
                '{}'
            WHERE
                l_shipdate >= CAST('1994-01-01' AS date)
                AND l_shipdate < CAST('1995-01-01' AS date)
                AND l_discount BETWEEN 0.05
                AND 0.07
                AND l_quantity < 24
            """,
        "substrait_query": get_substrait_plan('query_6_plan.json')
    }
]