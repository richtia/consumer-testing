import pytest
from ....common import get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_21",
        "file_names": ["supplier_1.parquet", "lineitem_1.parquet", "orders_1.parquet",
                       "nation_1.parquet" "lineitem_1.parquet", "lineitem_1.parquet"],
        "sql_query":
            """
            SELECT
                s_name,
                count(*) AS numwait
            FROM
                '{}', '{}' l1, '{}', '{}'
            WHERE
                s_suppkey = l1.l_suppkey
                AND o_orderkey = l1.l_orderkey
                AND o_orderstatus = 'F'
                AND l1.l_receiptdate > l1.l_commitdate
                AND EXISTS (
                    SELECT
                        *
                    FROM
                        '{}' l2
                    WHERE
                        l2.l_orderkey = l1.l_orderkey
                        AND l2.l_suppkey <> l1.l_suppkey)
                AND NOT EXISTS (
                    SELECT
                        *
                    FROM
                        '{}' l3
                    WHERE
                        l3.l_orderkey = l1.l_orderkey
                        AND l3.l_suppkey <> l1.l_suppkey
                        AND l3.l_receiptdate > l3.l_commitdate)
                AND s_nationkey = n_nationkey
                AND n_name = 'SAUDI ARABIA'
            GROUP BY
                s_name
            ORDER BY
                numwait DESC,
                s_name
            LIMIT 100;
            """,
        "substrait_query": get_substrait_plan('query_21_plan.json')
    }
]