import pytest
from ....common import get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_18",
        "file_names": ["customer_1.parquet", "orders_1.parquet", "lineitem_1.parquet", "lineitem_1.parquet"],
        "sql_query":
            """
            SELECT
                c_name,
                c_custkey,
                o_orderkey,
                o_orderdate,
                o_totalprice,
                sum(l_quantity)
            FROM
                '{}', '{}', '{}'
            WHERE
                o_orderkey IN (
                    SELECT
                        l_orderkey
                    FROM
                        '{}'
                    GROUP BY
                        l_orderkey
                    HAVING
                        sum(l_quantity) > 300)
                AND c_custkey = o_custkey
                AND o_orderkey = l_orderkey
            GROUP BY
                c_name,
                c_custkey,
                o_orderkey,
                o_orderdate,
                o_totalprice
            ORDER BY
                o_totalprice DESC,
                o_orderdate
            LIMIT 100;
            """,
        "substrait_query": get_substrait_plan('query_18_plan.json')
    }
]