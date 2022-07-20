TESTCASE = [
    {
        "test_name": "test_tpch_sql_15",
        "file_names": ["supplier_1.parquet", "lineitem_1.parquet", "lineitem_1.parquet"],
        "sql_query":
            """
            SELECT
                s_suppkey,
                s_name,
                s_address,
                s_phone,
                total_revenue
            FROM
                '{}',
                (
                    SELECT
                        l_suppkey AS supplier_no,
                        sum(l_extendedprice * (1 - l_discount)) AS total_revenue
                    FROM
                        '{}'
                    WHERE
                        l_shipdate >= CAST('1996-01-01' AS date)
                        AND l_shipdate < CAST('1996-04-01' AS date)
                    GROUP BY
                        supplier_no) revenue0
            WHERE
                s_suppkey = supplier_no
                AND total_revenue = (
                    SELECT
                        max(total_revenue)
                    FROM (
                        SELECT
                            l_suppkey AS supplier_no,
                            sum(l_extendedprice * (1 - l_discount)) AS total_revenue
                        FROM
                            '{}'
                        WHERE
                            l_shipdate >= CAST('1996-01-01' AS date)
                            AND l_shipdate < CAST('1996-04-01' AS date)
                        GROUP BY
                            supplier_no) revenue1)
            ORDER BY
                s_suppkey;
            """,
        "substrait_query":
            """
            """,
    }
]