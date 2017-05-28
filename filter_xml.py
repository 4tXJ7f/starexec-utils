from collections import defaultdict
import sys
import xml.etree.ElementTree as ET

def filter_space(stats, node, target_attribute, target_value, path):
  for space in node.findall('Space'):
    prev = len(space.findall('Benchmark'))
    filter_space(stats, space, target_attribute, target_value, path + [space.get('name')])

    # remove spaces that do not contain other spaces or benchmarks
    if len(space.findall('Space')) + len(space.findall('Benchmark')) == 0:
      node.remove(space)

  for benchmark in node.findall('Benchmark'):
    attributes = {}
    for attribute in benchmark.findall('Attribute'):
      attributes[attribute.get('name')] = attribute.get('value')

    status = attributes['status']
    expected_result = attributes['starexec-expected-result']
    assert status == expected_result or \
        (status == 'unknown' and expected_result == 'starexec-unknown')

    if target_attribute not in attributes or attributes[target_attribute] != target_value:
      node.remove(benchmark)
      stats['removed'] += 1
    else:
      stats['unknown'] += 1
      stats['/'.join(path)] += 1

def main(xml_filename, target_attribute, target_value):
  tree = ET.parse(xml_filename)
  root = tree.getroot()
  stats = defaultdict(int)
  filter_space(stats, root, target_attribute, target_value, [])
  tree.write('output2.xml')

  stats_list = ['{}: {}'.format(k, v) for k, v in stats.items()]
  print('\n'.join(sorted(stats_list)))

if __name__ == '__main__':
  assert len(sys.argv) > 1
  main(sys.argv[1], sys.argv[2], sys.argv[3])
