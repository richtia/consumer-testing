import pytest
from ....common import get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_17",
        "file_names": ["lineitem_1.parquet", "part_1.parquet", "lineitem_1.parquet"],
        "sql_query":
            """
            SELECT
                sum(l_extendedprice) / 7.0 AS avg_yearly
            FROM
                '{}', '{}'
            WHERE
                p_partkey = l_partkey
                AND p_brand = 'Brand#23'
                AND p_container = 'MED BOX'
                AND l_quantity < (
                    SELECT
                        0.2 * avg(l_quantity)
                    FROM
                        '{}'
                    WHERE
                        l_partkey = p_partkey);
            """,
        "substrait_query": get_substrait_plan('query_17_plan.json')
    }
]