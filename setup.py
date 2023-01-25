from setuptools import setup, find_packages
setup(
    name='substrait-consumer-test19',
    version='0.0.1',
    author='Substrait',
    description='A Substrait consumer test bench',
    long_description='Testing Substrait consumers with standard data processing queries',
    url='https://github.com/substrait-io/consumer-testing',
    keywords='substrait, consumer',
    python_requires='>=3.9, <4',
    packages=find_packages(include=['substrait_consumer*', 'substrait_consumer.*']),
    package_data={
        'substrait_consumer': ['tests/integration/queries/tpch_sql/*.sql',
                               'tests/integration/queries/tpch_substrait_plans/*.json'],
        'tests': ['tests/integration',
                  'tests/functional'],
    },
    entry_points={
        'console_scripts': [
            'test_substrait = substrait_consumer:main',
        ]
    }
)
