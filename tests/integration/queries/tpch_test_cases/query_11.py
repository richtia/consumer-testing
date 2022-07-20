TESTCASE = [
    {
        "test_name": "test_tpch_sql_11",
        "file_names": ["partsupp_1.parquet", "supplier_1.parquet", "nation_1.parquet",
                       "partsupp_1.parquet", "supplier_1.parquet", "nation_1.parquet"],
        "sql_query":
            """
            SELECT
                ps_partkey,
                sum(ps_supplycost * ps_availqty) AS value
            FROM
                '{}', '{}', '{}'
            WHERE
                ps_suppkey = s_suppkey
                AND s_nationkey = n_nationkey
                AND n_name = 'GERMANY'
            GROUP BY
                ps_partkey
            HAVING
                sum(ps_supplycost * ps_availqty) > (
                    SELECT
                        sum(ps_supplycost * ps_availqty) * 0.0001000000
                    FROM
                        '{}', '{}', '{}'
                    WHERE
                        ps_suppkey = s_suppkey
                        AND s_nationkey = n_nationkey
                        AND n_name = 'GERMANY')
            ORDER BY
                value DESC;
            """,
        "substrait_query":
            """
            """,
    }
]