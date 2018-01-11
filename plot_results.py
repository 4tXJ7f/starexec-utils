import csv
import os
import sys
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

def main(csv_filenames):
  wrong_benchmarks = dict()
  n_completed = defaultdict(int)
  benchmark_results = dict()
  unsolved = set()
  solved = set()
  expected_results = dict()

  solvers = set()
  solver_time = defaultdict(float)
  solver_solved = defaultdict(int)
  benchmark_times = defaultdict(lambda: dict())

  vtimeout = 600

  for csv_filename in csv_filenames:
    with open(csv_filename, 'r') as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',', skipinitialspace=True)

      headers = next(csv_reader)

      for row in csv_reader:
        benchmark_path = row[1]
        solver = '{}/{}'.format(row[3], row[5])
        configuration = row[5]
        status = row[7]
        cpu_time = float(row[8])
        wallclock_time = float(row[9])
        result = row[11]
        expected_result = row[12]

        solvers.add(solver)

        assert status in ['complete', 'timeout (cpu)', 'timeout (wallclock)', 'memout']
        assert result in ['sat', 'unsat', 'starexec-unknown']
        assert expected_result in ['sat', 'unsat', 'starexec-unknown']

        if cpu_time > vtimeout:
            cpu_time = vtimeout
            result = 'starexec-unknown'

        solver_time[solver] += cpu_time

        if result in ['sat', 'unsat']:
          solver_solved[solver] += 1

        benchmark_times[benchmark_path][solver] = cpu_time

  for solver, time in solver_time.items():
    print('{}: {}'.format(solver, time))

  for solver, solved in solver_solved.items():
    print('{}: {}'.format(solver, solved))

  solver_list = sorted(list(solvers))

  index = 1
  for i, solver1 in enumerate(solver_list):
    for j, solver2 in enumerate(solver_list[:i]):
      x = []
      y = []
      for benchmark, times in benchmark_times.items():
        x.append(times[solver1])
        y.append(times[solver2])
          
      ax = plt.subplot(1, len(solver_list) * (len(solver_list) - 1) / 2, index)
      ax.set_xscale('log')
      ax.set_yscale('log')
      ax.set_aspect('equal')

      plt.tick_params(axis='both', which='major', labelsize=5)
      plt.tick_params(axis='both', which='minor', labelsize=5)

      plt.scatter(x, y, marker='x', color='gray', s=0.5)
      plt.plot([0, 600], [0, 600], color='black')
      plt.xlabel(solver1, fontsize=5)
      plt.ylabel(solver2, fontsize=5)
      index += 1
  plt.tight_layout()
  plt.savefig('plot.pdf')

if __name__ == '__main__':
  assert len(sys.argv) > 1
  main(sys.argv[1:])
