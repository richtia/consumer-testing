import pytest
from ....common import get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_8",
        "file_names": ["part_1.parquet", "supplier_1.parquet", "lineitem_1.parquet",
                       "orders_1.parquet", "customer_1.parquet", "nation_1.parquet",
                       "nation_1.parquet", "region_1.parquet"],
        "sql_query":
            """
            SELECT
                o_year,
                sum(
                    CASE WHEN nation = 'BRAZIL' THEN
                        volume
                    ELSE
                        0
                    END) / sum(volume) AS mkt_share
            FROM (
                SELECT
                    extract(year FROM o_orderdate) AS o_year,
                    l_extendedprice * (1 - l_discount) AS volume,
                    n2.n_name AS nation
                FROM
                    '{}', '{}', '{}', '{}', '{}', '{}' n1, '{}' n2, '{}'
                WHERE
                    p_partkey = l_partkey
                    AND s_suppkey = l_suppkey
                    AND l_orderkey = o_orderkey
                    AND o_custkey = c_custkey
                    AND c_nationkey = n1.n_nationkey
                    AND n1.n_regionkey = r_regionkey
                    AND r_name = 'AMERICA'
                    AND s_nationkey = n2.n_nationkey
                    AND o_orderdate BETWEEN CAST('1995-01-01' AS date)
                    AND CAST('1996-12-31' AS date)
                    AND p_type = 'ECONOMY ANODIZED STEEL') AS all_nations
            GROUP BY
                o_year
            ORDER BY
                o_year
            """,
        "substrait_query": get_substrait_plan('query_8_plan.json')
    }
]