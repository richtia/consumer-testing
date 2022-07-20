import pytest
from ....common import get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_22",
        "file_names": ["customer_1.parquet", "customer_1.parquet", "orders_1.parquet"],
        "sql_query":
            """
            SELECT
                cntrycode,
                count(*) AS numcust,
                sum(c_acctbal) AS totacctbal
            FROM (
                SELECT
                    substring(c_phone FROM 1 FOR 2) AS cntrycode,
                    c_acctbal
                FROM
                    '{}'
                WHERE
                    substring(c_phone FROM 1 FOR 2) IN ('13', '31', '23', '29', '30', '18', '17')
                    AND c_acctbal > (
                        SELECT
                            avg(c_acctbal)
                        FROM
                            '{}'
                        WHERE
                            c_acctbal > 0.00
                            AND substring(c_phone FROM 1 FOR 2) IN ('13', '31', '23', '29', '30', '18', '17'))
                        AND NOT EXISTS (
                            SELECT
                                *
                            FROM
                                '{}'
                            WHERE
                                o_custkey = c_custkey)) AS custsale
            GROUP BY
                cntrycode
            ORDER BY
                cntrycode;
            """,
        "substrait_query": get_substrait_plan('query_22_plan.json')
    }
]