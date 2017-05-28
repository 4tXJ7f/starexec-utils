import sys
import os

def main(input_dir):
  results = dict()
  for path, subdirs, filenames in os.walk(input_dir):
    for filename in filenames:
      if filename.endswith('.txt'):
        log_filename = os.path.join(path, filename)
        with open(log_filename) as log_file:
          try:
            lines = log_file.readlines()
            if len(lines) == 2:
              lines = [line[line.find('\t') + 1:].strip() for line in lines]
              assert lines[1] == 'EOF'

              root_benchmark, benchmark = os.path.split(path)
              root_solver, solver = os.path.split(root_benchmark)

              benchmark = root_solver + benchmark
              if benchmark not in results:
                results[benchmark] = ([], [])

              if lines[0] == 'sat':
                results[benchmark][0].append(solver)
              if lines[0] == 'unsat':
                results[benchmark][1].append(solver)
          except UnicodeDecodeError:
            print('Warning: was not able to read {}'.format(log_filename))

  for benchmark, result in results.items():
    n_sat = len(result[0])
    n_unsat = len(result[1])
    n_solvers = max(n_sat, n_unsat)
    assert n_sat == 0 or n_unsat == 0

    result_str = None
    if n_sat > 0:
      result_str = 'sat'
    elif n_unsat > 0:
      result_str = 'unsat'

    if result_str is not None:
      print('{}: {} ({} solvers)'.format(benchmark, result_str, n_solvers))

if __name__ == '__main__':
  assert len(sys.argv) > 1
  main(sys.argv[1])
