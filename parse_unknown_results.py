import csv
import os
import sys
from collections import defaultdict

def main(csv_filenames):
  n_completed = defaultdict(int)
  benchmark_results = dict()
  unsolved = set()
  solved = set()
  expected_results = dict()
  solvers = set()

  for csv_filename in csv_filenames:
    print(csv_filename)
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
        if len(row) < 13:
          expected_result = 'starexec-unknown'
        else:
          expected_result = row[12]

        if solver not in solvers:
          solvers.add(solver)

        assert status in ['complete', 'timeout (cpu)', 'timeout (wallclock)', 'memout', 'enqueued']
        assert result in ['sat', 'unsat', 'starexec-unknown', '--']
        assert expected_result in ['starexec-unknown']

        if result in ['sat', 'unsat']:
          n_completed[solver] += 1

          if benchmark_path not in benchmark_results:
            benchmark_results[benchmark_path] = ([], [])
          benchmark_results[benchmark_path][0 if result == 'sat' else 1].append(solver)

          if benchmark_path in unsolved:
            unsolved.remove(benchmark_path)
          solved.add(benchmark_path)
        else:
          unsolved.add(benchmark_path)

  solver_list = list(solvers)
  solved = 0
  partially_solved = 0
  with open('results.csv', 'w') as f:
    f.write('benchmark,result,{}\n'.format(','.join(solver_list)))
    for benchmark_path, results in benchmark_results.items():
      solvers_sat, solvers_unsat = results
      n_solvers_sat = len(solvers_sat)
      n_solvers_unsat = len(solvers_unsat)

      if n_solvers_sat != 0 and n_solvers_unsat != 0:
        print(benchmark_path)
        print('\tsat:\t{}'.format(', '.join(solvers_sat)))
        print('\tunsat:\t{}'.format(', '.join(solvers_unsat)))
      elif max(n_solvers_sat, n_solvers_unsat) >= 2:
        solver_results = ','.join(['sat' if solver in solvers_sat else ('unsat' if solver in solvers_unsat else '--') for solver in solver_list])
        f.write('{},{},{}\n'.format(benchmark_path, 'sat' if n_solvers_sat > 0 else 'unsat', solver_results))
        solved += 1
      else:
        partially_solved += 1

  print()

  print('{} solved, {} partially solved, {} unsolved'.format(solved, partially_solved, len(unsolved)))

if __name__ == '__main__':
  assert len(sys.argv) > 1
  main(sys.argv[1:])
