from collections import defaultdict
import sys
import xml.etree.ElementTree as ET

def filter_space(stats, node, benchmark_list, path):
  for space in node.findall('Space'):
    prev = len(space.findall('Benchmark'))
    filter_space(stats, space, benchmark_list, path + [space.get('name')])

    # remove spaces that do not contain other spaces or benchmarks
    if len(space.findall('Space')) + len(space.findall('Benchmark')) == 0:
      node.remove(space)

  for benchmark in node.findall('Benchmark'):
    attributes = {'name': benchmark.get('name')}
    for attribute in benchmark.findall('Attribute'):
      attributes[attribute.get('name')] = attribute.get('value')

    status = attributes['status']
    expected_result = attributes['starexec-expected-result']
    assert status == expected_result or \
        (status == 'unknown' and expected_result == 'starexec-unknown')

    if '/'.join(path + [attributes['name']]) not in benchmark_list:
      node.remove(benchmark)
      stats['removed'] += 1
    else:
      stats['unknown'] += 1
      stats['/'.join(path)] += 1

def main(xml_filename, benchmark_list_filename):
  benchmark_list = None
  with open(benchmark_list_filename) as f:
    benchmark_list = [name.strip() for name in f]

  tree = ET.parse(xml_filename)
  root = tree.getroot()
  stats = defaultdict(int)
  filter_space(stats, root, benchmark_list, [])
  tree.write('output_filtered.xml')

  stats_list = ['{}: {}'.format(k, v) for k, v in stats.items()]
  print('\n'.join(sorted(stats_list)))

if __name__ == '__main__':
  assert len(sys.argv) > 1
  main(sys.argv[1], sys.argv[2])
