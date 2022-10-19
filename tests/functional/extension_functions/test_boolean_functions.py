from typing import Callable, Iterable

import duckdb
from ibis.expr.types.relations import Table
from ibis_substrait.tests.compiler.conftest import *

from tests.functional.boolean_tests import AGGREGATE_FUNCTIONS, SCALAR_FUNCTIONS
from tests.parametrization import custom_parametrization
from tests.functional.common import substrait_function_test


@pytest.mark.usefixtures("prepare_tpch_parquet_data")
class TestBooleanFunctions:
    """
    Test Class verifying different consumers are able to run substrait plans
    that include substrait boolean functions.
    """

    @staticmethod
    @pytest.fixture(scope="function", autouse=True)
    def setup_teardown_function(request):
        cls = request.cls

        cls.db_connection = duckdb.connect()
        cls.db_connection.execute("install substrait")
        cls.db_connection.execute("load substrait")
        cls.db_connection.execute("create table t (a int, b int, c boolean, d boolean)")
        cls.db_connection.execute(
            "INSERT INTO t VALUES "
            "(1, 1, TRUE, TRUE), (2, 1, FALSE, TRUE), (3, 1, TRUE, TRUE), "
            "(-4, 1, TRUE, TRUE), (5, 1, FALSE, TRUE), (-6, 2, TRUE, TRUE), "
            "(7, 2, FALSE, TRUE), (8, 2, True, TRUE), (9, 2, FALSE, TRUE), "
            "(NULL, 2, FALSE, TRUE);"
        )
        cls.table_t = ibis.table(
            [("a", dt.int32), ("b", dt.int32), ("c", dt.boolean), ("d", dt.boolean)],
            name="t",
        )

        cls.created_tables = set()

        yield

        cls.db_connection.close()

    @custom_parametrization(SCALAR_FUNCTIONS + AGGREGATE_FUNCTIONS)
    def test_boolean_functions(
        self,
        test_name: str,
        file_names: Iterable[str],
        sql_query: str,
        ibis_expr: Callable[[Table], Table],
        producer,
        consumer,
    ) -> None:
        substrait_function_test(
            self.db_connection,
            self.created_tables,
            file_names,
            sql_query,
            ibis_expr,
            producer,
            consumer,
            self.table_t
        )
