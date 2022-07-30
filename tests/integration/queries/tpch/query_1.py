import pytest
from ....common import get_substrait_plan

TESTCASE = [
    {
        "test_name": "test_tpch_sql_1",
        "file_names": ["lineitem_0.1.parquet"],
        "sql_query":
            """
            select
              l_returnflag,
              l_linestatus,
              sum(l_quantity) as sum_qty,
              sum(l_extendedprice) as sum_base_price,
              sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
              sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
              avg(l_quantity) as avg_qty,
              avg(l_extendedprice) as avg_price,
              avg(l_discount) as avg_disc,
              count(*) as count_order
            from
              '{}'
            where
              l_shipdate <= date '1998-12-01' - interval '120' day (3)
            group by
              l_returnflag,
              l_linestatus
            order by
              l_returnflag,
              l_linestatus
            """,
        "substrait_query": get_substrait_plan('query_1_plan.json')
    }
]