import csv
import os
import sys
from collections import defaultdict

def main(csv_filenames):
  wrong_benchmarks = dict()
  n_completed = defaultdict(int)
  benchmark_results = dict()
  unsolved = set()
  solved = set()
  expected_results = dict()

  for csv_filename in csv_filenames:
    with open(csv_filename, 'r') as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',', skipinitialspace=True)

      headers = next(csv_reader)

      for row in csv_reader:
        benchmark_path = row[1]
        solver = row[3]
        configuration = row[5]
        status = row[7]
        wallclock_time = float(row[9])
        result = row[11]
        expected_result = row[12]

        if solver not in wrong_benchmarks:
          wrong_benchmarks[solver] = []

        assert status in ['complete', 'timeout (cpu)', 'timeout (wallclock)', 'memout']
        assert result in ['sat', 'unsat', 'starexec-unknown']
        assert expected_result in ['sat', 'unsat', 'starexec-unknown']

        # Check that result was correct
        if expected_result in ['sat', 'unsat']:
          if result != 'starexec-unknown' and result != expected_result:
            wrong_benchmarks[solver].append((benchmark_path, expected_result, result))
          expected_results[benchmark_path] = expected_result

        if result in ['sat', 'unsat']:
          n_completed[solver] += 1

          if benchmark_path not in benchmark_results:
            benchmark_results[benchmark_path] = ([], [])
          benchmark_results[benchmark_path][0 if result == 'sat' else 1].append(solver)

          if benchmark_path in unsolved:
            unsolved.remove(benchmark_path)
          solved.add(benchmark_path)
        elif benchmark_path not in solved:
          unsolved.add(benchmark_path)

  for solver, benchmarks in wrong_benchmarks.items():
    print('{} ({} completed)'.format(solver, n_completed[solver]))
    for (benchmark, expected_result, result) in benchmarks:
      print('\t{} ({} instead of {})'.format(benchmark, result, expected_result))

  print()

  for benchmark_path, results in benchmark_results.items():
    solvers_sat, solvers_unsat = results
    n_solvers_sat = len(solvers_sat)
    n_solvers_unsat = len(solvers_unsat)

    assert benchmark_path not in unsolved

    if n_solvers_sat != 0 and n_solvers_unsat != 0:
      print(benchmark_path)
      print('\tsat:\t{}'.format(', '.join(solvers_sat)))
      print('\tunsat:\t{}'.format(', '.join(solvers_unsat)))

  print()

  print('Unsolved ({} benchmarks)'.format(len(unsolved)))
  unsolved_with_expected_result = []
  for unsolved_benchmark in sorted(list(unsolved)):
    if unsolved_benchmark in expected_results:
      unsolved_with_expected_result.append(unsolved_benchmark)
    print('{}{}'.format(unsolved_benchmark, ' ({})'.format(expected_results[unsolved_benchmark]) if unsolved_benchmark in expected_results else ''))
  print('Unsolved with expected result: {}'.format(len(unsolved_with_expected_result)))

  with open('list.txt', 'w') as f:
    f.write('\n'.join(unsolved_with_expected_result))

if __name__ == '__main__':
  assert len(sys.argv) > 1
  main(sys.argv[1:])
