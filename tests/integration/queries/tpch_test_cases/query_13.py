TESTCASE = [
    {
        "test_name": "test_tpch_sql_13",
        "file_names": ["customer_1.parquet", "orders_1.parquet"],
        "sql_query":
            """
            SELECT
                c_count,
                count(*) AS custdist
            FROM (
                SELECT
                    c_custkey,
                    count(o_orderkey)
                FROM
                    '{}'
                LEFT OUTER JOIN '{}' ON c_custkey = o_custkey
                AND o_comment NOT LIKE '%special%requests%'
            GROUP BY
                c_custkey) AS c_orders (c_custkey,
                    c_count)
            GROUP BY
                c_count
            ORDER BY
                custdist DESC,
                c_count DESC;
            """,
        "substrait_query":
            """
            """,
    }
]