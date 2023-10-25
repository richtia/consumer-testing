import json
import string
from pathlib import Path
from typing import Iterable

import duckdb
import pyarrow as pa
import pytest
import substrait.gen.proto.plan_pb2 as plan_pb2
from datafusion import SessionContext
from datafusion import substrait as ss
from google.protobuf import json_format
from google.protobuf.json_format import MessageToJson
from ibis_substrait.compiler.core import SubstraitCompiler

from substrait_consumer.common import SubstraitUtils
from substrait_consumer.consumers import COLUMN_A, COLUMN_B, COLUMN_C, COLUMN_D
from substrait_consumer.context import get_schema, produce_isthmus_substrait


class DuckDBProducer:
    """
    Adapts the DuckDB Substrait producer to the test framework.
    """
    def __init__(self, db_connection=None):
        if db_connection is not None:
            self._db_connection = db_connection
        else:
            self._db_connection = duckdb.connect()
            self._db_connection.execute("INSTALL substrait")
            self._db_connection.execute("LOAD substrait")

    def set_db_connection(self, db_connection):
        self._db_connection = db_connection

    def produce_substrait(self, sql_query: str, ibis_expr: str = None) -> str:
        """
        Produce the DuckDB substrait plan using the given SQL query.

        Parameters:
            sql_query:
                SQL query.
        Returns:
            Substrait query plan in json format.
        """
        duckdb_substrait_plan = self._db_connection.get_substrait_json(sql_query)
        proto_bytes = duckdb_substrait_plan.fetchone()[0]
        python_json = json.loads(proto_bytes)
        return json.dumps(python_json, indent=2)

    def format_sql(self, created_tables, sql_query, file_names):
        if len(file_names) > 0:
            table_names = load_tables_from_parquet(
                self._db_connection, created_tables, file_names
            )
            sql_query = sql_query.format(*table_names)
        return sql_query

    def name(self):
        return "DuckDBProducer"


class IbisProducer:
    """
    Adapts the Ibis Substrait producer to the test framework.
    """
    def __init__(self, db_connection=None):
        if db_connection is not None:
            self._db_connection = db_connection
        else:
            self._db_connection = duckdb.connect()

        self._db_connection.execute("INSTALL substrait")
        self._db_connection.execute("LOAD substrait")
        self.compiler = SubstraitCompiler()

    def set_db_connection(self, db_connection):
        self._db_connection = db_connection

    def produce_substrait(self, sql_query: str, ibis_expr: str = None) -> str:
        """
        Produce the Ibis substrait plan using the given Ibis expression

        Parameters:
            ibis_expr:
                Ibis expression.
        Returns:
            Substrait query plan in json format.
        """
        if ibis_expr is None:
            pytest.skip("ibis expression currently undefined")
        tpch_proto_bytes = self.compiler.compile(ibis_expr)
        substrait_plan = json_format.MessageToJson(tpch_proto_bytes)
        return substrait_plan

    def format_sql(self, created_tables, sql_query, file_names):
        if len(file_names) > 0:
            table_names = load_tables_from_parquet(
                self._db_connection, created_tables, file_names
            )
            sql_query = sql_query.format(*table_names)
        return sql_query

    def name(self):
        return "IbisProducer"


class IsthmusProducer:
    """
    Adapts the Isthmus Substrait producer to the test framework.
    """
    def __init__(self, db_connection=None):
        if db_connection is not None:
            self._db_connection = db_connection
        else:
            self._db_connection = duckdb.connect()

        self._db_connection.execute("INSTALL substrait")
        self._db_connection.execute("LOAD substrait")
        self.compiler = SubstraitCompiler()
        self.file_names = None

    def set_db_connection(self, db_connection):
        self._db_connection = db_connection

    def produce_substrait(self, sql_query: str, ibis_expr: str = None) -> str:
        """
        Produce the Isthmus substrait plan using the given SQL query.

        Parameters:
            sql_query:
                SQL query.
        Returns:
            Substrait query plan in json format.
        """
        schema_list = get_schema(self.file_names)
        substrait_plan_str = produce_isthmus_substrait(sql_query, schema_list)

        return substrait_plan_str

    def format_sql(self, created_tables, sql_query, file_names):
        sql_query = sql_query.replace("'{}'", "{}")
        sql_query = sql_query.replace("'t'", "t")
        if len(file_names) > 0:
            self.file_names = file_names
            table_names = load_tables_from_parquet(
                self._db_connection, created_tables, file_names
            )
            sql_query = sql_query.format(*table_names)
        return sql_query

    def name(self):
        return "IsthmusProducer"


class DataFusionProducer:
    """
    Adapts the DataFusion Substrait producer to the test framework.
    """
    def __init__(self, db_connection=None):
        self._ctx = SessionContext()
        if db_connection is not None:
            self._db_connection = db_connection
        else:
            self._db_connection = db_connection

    def set_db_connection(self, db_connection):
        self._db_connection = db_connection

    def produce_substrait(self, sql_query: str, ibis_expr: str = None) -> str:
        """
        Produce the DataFusion substrait plan using the given SQL query.

        Parameters:
            sql_query:
                SQL query.
        Returns:
            Substrait query plan in json format.
        """
        substrait_proto = plan_pb2.Plan()

        substrait_plan = ss.substrait.serde.serialize_to_plan(sql_query, self._ctx)
        substrait_plan_bytes = substrait_plan.encode()
        substrait_proto.ParseFromString(substrait_plan_bytes)

        return MessageToJson(substrait_proto)

    def register_tables(self, created_tables, file_names):
        """
        Register tables to the datafusion session context.

        Parameters:
            created_tables:
                The set of tables that have already been created.
            file_names:
                Name of parquet files.
        Returns:
            None
        """
        if len(file_names) > 0:
            parquet_file_paths = SubstraitUtils.get_full_path(file_names)
            for file_name, file_path in zip(file_names, parquet_file_paths):
                table_name = Path(file_name).stem
                table_name = table_name.translate(
                    str.maketrans("", "", string.punctuation)
                )
                if f"{self.__class__.__name__}{table_name}" not in created_tables:
                    created_tables.add(f"{self.__class__.__name__}{table_name}")
                    self._ctx.register_parquet(f"{table_name}", file_path)
        else:
            if not self._ctx.table_exist("t"):
                tables = pa.RecordBatch.from_arrays(
                    [
                        pa.array(COLUMN_A),
                        pa.array(COLUMN_B),
                        pa.array(COLUMN_C),
                        pa.array(COLUMN_D),
                    ],
                    names=["a", "b", "c", "d"],
                )
                self._ctx.register_record_batches("t", [[tables]])

    def format_sql(self, created_tables, sql_query, file_names):
        self.register_tables(created_tables, file_names)
        if len(file_names) > 0:
            table_names = load_tables_from_parquet(
                self._db_connection, created_tables, file_names
            )
            sql_query = sql_query.format(*table_names)
        return sql_query

    def name(self):
        return "DataFusionProducer"


def load_tables_from_parquet(
    db_connection,
    created_tables: set,
    file_names: Iterable[str],
) -> list:
    """
    Load all the parquet files into separate tables in DuckDB.

    Parameters:
        db_connection:
            DuckDB Connection.
        created_tables:
            The set of tables that have already been created.
        file_names:
            Name of parquet files.
    Returns:
        A list of the table names.
    """
    parquet_file_paths = SubstraitUtils.get_full_path(file_names)
    table_names = []
    for file_name, file_path in zip(file_names, parquet_file_paths):
        table_name = Path(file_name).stem
        table_name = table_name.translate(str.maketrans("", "", string.punctuation))
        if table_name not in created_tables:
            create_table_sql = f"CREATE TABLE {table_name} AS SELECT * FROM read_parquet('{file_path}');"
            db_connection.execute(create_table_sql)
            created_tables.add(table_name)
        table_names.append(table_name)

    return table_names
