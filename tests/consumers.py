from __future__ import annotations

import asyncio
import string
from pathlib import Path
from typing import Iterable
from functools import wraps, partial

import duckdb
import pyarrow as pa
import pyarrow.substrait as substrait

from .common import SubstraitUtils


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

    def set_db_connection(self, db_connection):
        self.db_connection = db_connection

    async def run_substrait_query(self, substrait_query: bytes) -> pa.Table:
        """
        Run the substrait plan against DuckDB.

        Parameters:
            substrait_query:
                A substrait plan in byte format

        Returns:
            A pyarrow table resulting from running the substrait query plan.
        """
        async_from_substrait = async_wrap(self.db_connection.from_substrait)
        table = await async_from_substrait(substrait_query)
        return table.arrow()

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
            if table_name not in created_tables:
                create_table_sql = f"CREATE TABLE {table_name} AS SELECT * FROM read_parquet('{file_path}');"
                self.db_connection.execute(create_table_sql)
                created_tables.add(table_name)
            table_names.append(table_name)

        return table_names


class AceroConsumer:
    """
    Adapts the Acero Substrait consumer to the test framework.
    """
    def __init__(self, db_connection=None):
        if db_connection is not None:
            self.db_connection = db_connection
        else:
            self.db_connection = duckdb.connect()

        self.db_connection.execute("INSTALL substrait")
        self.db_connection.execute("LOAD substrait")

    def set_db_connection(self, db_connection):
        self.db_connection = db_connection

    @staticmethod
    async def run_substrait_query(substrait_query: bytes) -> pa.Table:
        """
        Run the substrait plan against Acero.

        Parameters:
            substrait_query:
                A json formatted byte representation of the substrait query plan.

        Returns:
            A pyarrow table resulting from running the substrait query plan.
        """
        buf = pa._substrait._parse_json_plan(substrait_query.encode())
        reader = substrait.run_query(buf)
        result = reader.read_all()

        return result

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
            if table_name not in created_tables:
                create_table_sql = f"CREATE TABLE {table_name} AS SELECT * FROM read_parquet('{file_path}');"
                self.db_connection.execute(create_table_sql)
                created_tables.add(table_name)
            table_names.append(table_name)

        return table_names


def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run