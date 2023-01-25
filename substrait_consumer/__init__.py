from pathlib import Path

from filelock import FileLock
from typing import Iterable
import argparse
import duckdb
import string
import sys


def prepare_data():
    data_path = Path(__file__).parent / "adhoc_data"
    data_path.mkdir(parents=True, exist_ok=True)
    lock_file = data_path / "data.json"
    with FileLock(str(lock_file) + ".lock"):
        con = duckdb.connect()
        con.execute(f"CALL dbgen(sf=0.1)")
        con.execute(f"EXPORT DATABASE '{data_path}' (FORMAT PARQUET);")
    print(f"Parquet data written to {data_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare_data', default=False,
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('--producer', nargs='+', required=True,
                        choices=['CLIIsthmusProducer', 'CLIDuckDBProducer', 'CLIIbisProducer'],
                        help='Substrait Producer')
    parser.add_argument('--consumer', nargs='+', required=False,
                        choices=['AceroConsumer', 'DuckDBConsumer'],
                        help='Substrait Consumer')
    args = parser.parse_args()

    if args.prepare_data is True:
        print(f"prepare data is: {args.prepare_data}")
        prepare_data()
    else:
        print(f"prepare data is: {args.prepare_data}")
        print("Not preparing data.")

    print(f"type: {type(args.producer)}")
    print(f"producers: {args.producer}")

    for producer_str in args.producer:
        producer = str_to_class(producer_str)()
        print(type(producer))
        print(dir(producer))

        producer.produce_substrait()


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


if __name__ == ' __main__':
          main()


class CLIDuckDBProducer:
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
    def produce_substrait():
        print("hello")


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