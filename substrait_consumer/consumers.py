from __future__ import annotations

import string
from pathlib import Path
from typing import Iterable

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.substrait as substrait

from substrait_consumer.common import SubstraitUtils


class DuckDBConsumer:
    """
    Adapts the DuckDB Substrait consumer to the test framework.
    """

    def __init__(self, db_connection=None):
        if db_connection is not None:
            self.db_connection = db_connection
        else:
            self.db_connection = duckdb.connect()

        self.db_connection.execute("INSTALL substrait")
        self.db_connection.execute("LOAD substrait")

    def setup(self, db_connection, created_tables, file_names: Iterable[str]):
        self.db_connection = db_connection
        self.load_tables_from_parquet(created_tables, file_names)

    def run_substrait_query(self, substrait_query: str) -> pa.Table:
        """
        Run the substrait plan against DuckDB.

        Parameters:
            substrait_query:
                A substrait plan in json format.

        Returns:
            A pyarrow table resulting from running the substrait query plan.
        """
        return self.db_connection.from_substrait_json(substrait_query).arrow()

    def load_tables_from_parquet(
        self,
        created_tables: set,
        file_names: Iterable[str],
    ) -> list:
        """
        Load all the parquet files into separate tables in DuckDB.

        Parameters:
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
            if f"{self.__class__.__name__}{table_name}" not in created_tables:
                create_table_sql = f"CREATE TABLE {table_name} AS SELECT * FROM read_parquet('{file_path}');"
                self.db_connection.execute(create_table_sql)
                created_tables.add(f"{self.__class__.__name__}{table_name}")
            table_names.append(table_name)

        return table_names


class AceroConsumer:
    """
    Adapts the Acero Substrait consumer to the test framework.
    """

    def __init__(self):
        self.tables = {}
        self.table_provider = lambda names, schema: self.tables[names[0].lower()]

    def setup(self, db_connection, created_tables, file_names: Iterable[str]):
        if len(file_names) > 0:
            parquet_file_paths = SubstraitUtils.get_full_path(file_names)
            for file_name, file_path in zip(file_names, parquet_file_paths):
                table_name = Path(file_name).stem
                table_name = table_name.translate(
                    str.maketrans("", "", string.punctuation)
                )
                if f"{self.__class__.__name__}{table_name}" not in created_tables:
                    created_tables.add(f"{self.__class__.__name__}{table_name}")
                    self.tables[table_name] = pq.read_table(file_path)
        else:
            table = pa.table(
                {
                    "a": [1, 2, 3, -4, 5, -6, 7, 8, 9, None],
                    "b": [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
                    "c": [
                        True,
                        False,
                        True,
                        True,
                        False,
                        True,
                        False,
                        True,
                        False,
                        False,
                    ],
                    "d": [
                        True,
                        True,
                        True,
                        True,
                        True,
                        True,
                        True,
                        True,
                        True,
                        True,
                    ],
                }
            )
            self.tables["t"] = table

    def run_substrait_query(self, substrait_query: str) -> pa.Table:
        """
        Run the substrait plan against Acero.

        Parameters:
            substrait_query:
                A substrait plan in json format.

        Returns:
            A pyarrow table resulting from running the substrait query plan.
        """
        substrait_query = pa._substrait._parse_json_plan(substrait_query.encode())

        reader = substrait.run_query(
            substrait_query, table_provider=self.table_provider
        )
        result = reader.read_all()

        return result
