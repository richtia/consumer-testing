import pytest
from ....common import get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_10",
        "file_names": ["customer_1.parquet", "orders_1.parquet", "lineitem_1.parquet",
                       "nation_1.parquet"],
        "sql_query":
            """
            SELECT
                c_custkey,
                c_name,
                sum(l_extendedprice * (1 - l_discount)) AS revenue,
                c_acctbal,
                n_name,
                c_address,
                c_phone,
                c_comment
            FROM
                '{}', '{}', '{}', '{}'
            WHERE
                c_custkey = o_custkey
                AND l_orderkey = o_orderkey
                AND o_orderdate >= CAST('1993-10-01' AS date)
                AND o_orderdate < CAST('1994-01-01' AS date)
                AND l_returnflag = 'R'
                AND c_nationkey = n_nationkey
            GROUP BY
                c_custkey,
                c_name,
                c_acctbal,
                c_phone,
                n_name,
                c_address,
                c_comment
            ORDER BY
                revenue DESC
            LIMIT 20;
            """,
        "substrait_query": get_substrait_plan('query_10_plan.json')
    }
]