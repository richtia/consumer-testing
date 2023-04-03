from substrait_consumer.producers import *

SQL_SCALAR = {
    "ceil": (
        """
        SELECT PS_SUPPLYCOST, ceil(CAST(PS_SUPPLYCOST AS DOUBLE)) AS CEIL_SUPPLYCOST
        FROM '{}';
        """,
        [DuckDBProducer, IsthmusProducer],
    ),
    "floor": (
        """
        SELECT PS_SUPPLYCOST, floor(CAST(PS_SUPPLYCOST AS DOUBLE)) AS FLOOR_SUPPLYCOST
        FROM '{}';
        """,
        [DuckDBProducer, IsthmusProducer],
    ),
    "round": (
        """
        SELECT L_EXTENDEDPRICE, round(CAST(L_EXTENDEDPRICE AS DOUBLE), 1) AS ROUND_EXTENDEDPRICE
        FROM '{}';
        """,
        [DuckDBProducer, IsthmusProducer],
    ),
}
