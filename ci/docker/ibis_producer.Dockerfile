FROM ubuntu:22.04

ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y python3.10 && ln -sf python3 /usr/bin/python
RUN apt install -y pip
RUN pip install --upgrade pip setuptools pytest pytest-snapshot substrait==0.8.0 pyarrow protobuf duckdb filelock datafusion ibis_substrait ibis_framework=7.0.0 JPype1

WORKDIR /substrait_consumer
COPY . .

CMD /usr/bin/python -mpytest -m produce_substrait_snapshot --producer=IbisProducer substrait_consumer/tests/functional/extension_functions
