import pytest
from ....common import get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_14",
        "file_names": ["lineitem_1.parquet", "part_1.parquet"],
        "sql_query":
            """
            SELECT
                100.00 * sum(
                    CASE WHEN p_type LIKE 'PROMO%' THEN
                        l_extendedprice * (1 - l_discount)
                    ELSE
                        0
                    END) / sum(l_extendedprice * (1 - l_discount)) AS promo_revenue
            FROM
                '{}', '{}'
            WHERE
                l_partkey = p_partkey
                AND l_shipdate >= date '1995-09-01'
                AND l_shipdate < CAST('1995-10-01' AS date);
            """,
        "substrait_query": get_substrait_plan('query_14_plan.json')
    }
]