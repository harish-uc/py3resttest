# Profile the basic test execution

import cProfile

from py3resttest.benchmarks import Benchmark
from py3resttest.binding import self
from py3resttest.contenthandling import ContentHandler
from py3resttest.generators import factory_generate_ids

test = Benchmark()
test.warmup_runs = 0
test.benchmark_runs = 1000
test.raw_metrics = set()
test.metrics = {'total_time'}
test.aggregated_metrics = {'total_time': ['total', 'mean']}

# Basic get test
test.url = 'http://localhost:8000/api/person/'
test.name = 'Basic GET'
print('Basic GET test')
# cProfile.run('resttest.run_benchmark(test)', sort='cumtime')


# Test a generator PUT method
test.method = 'PUT'
test.set_url('http://localhost:8000/api/person/$id/', isTemplate=True)
test.headers = {'Content-Type': 'application/json'}
handler = ContentHandler()
handler.setup('{"first_name": "Gaius","id": "$id","last_name": "Baltar","login": "$id"}',
              is_template_content=True)
test.body = handler
context = self()
context.add_generator('gen', factory_generate_ids(starting_id=10)())
test.generator_binds = {'id': 'gen'}
print('Running templated PUT test')
cProfile.run('resttest.run_benchmark(test, context=context)', sort='cumtime')
