from collections import defaultdict
import sys
import xml.etree.ElementTree as ET

def set_solvers_in_hierarchy(node, solvers):
  # Remove old solvers
  for solver in node.findall('Solver'):
    node.remove(solver)

  # Add new solvers
  for solver in solvers:
    node.append(solver)

  # Recurse into subspaces
  for subspace in node.findall('Space'):
    set_solvers_in_hierarchy(subspace, solvers)

def set_solvers_in_xml(root, solvers):
  main_space = root.find('Space')
  for space in main_space.findall('Space'):
    space_name = space.get('name')
    set_solvers_in_hierarchy(space, solvers[space_name])

def get_solvers_from_xml(root):
  solvers = defaultdict(list)
  main_space = root.find('Space')
  for space in main_space.findall('Space'):
    space_name = space.get('name')
    for solver in space.findall('Solver'):
      solvers[space_name].append(solver)
  return solvers

def main(from_xml_filename, to_xml_filename):
  from_tree = ET.parse(from_xml_filename)
  solvers = get_solvers_from_xml(from_tree.getroot())

  to_tree = ET.parse(to_xml_filename)
  set_solvers_in_xml(to_tree.getroot(), solvers)
  to_tree.write('new_output.xml')

if __name__ == '__main__':
  assert len(sys.argv) > 2
  main(sys.argv[1], sys.argv[2])
