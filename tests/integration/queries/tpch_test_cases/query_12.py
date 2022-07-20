import pytest
from ....common import get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_12",
        "file_names": ["orders_1.parquet", "lineitem_1.parquet"],
        "sql_query":
            """
            SELECT
                l_shipmode,
                sum(
                    CASE WHEN o_orderpriority = '1-URGENT'
                        OR o_orderpriority = '2-HIGH' THEN
                        1
                    ELSE
                        0
                    END) AS high_line_count,
                sum(
                    CASE WHEN o_orderpriority <> '1-URGENT'
                        AND o_orderpriority <> '2-HIGH' THEN
                        1
                    ELSE
                        0
                    END) AS low_line_count
            FROM
                '{}', '{}'
            WHERE
                o_orderkey = l_orderkey
                AND l_shipmode IN ('MAIL', 'SHIP')
                AND l_commitdate < l_receiptdate
                AND l_shipdate < l_commitdate
                AND l_receiptdate >= CAST('1994-01-01' AS date)
                AND l_receiptdate < CAST('1995-01-01' AS date)
            GROUP BY
                l_shipmode
            ORDER BY
                l_shipmode;
            """,
        "substrait_query": get_substrait_plan('query_12_plan.json')
    }
]