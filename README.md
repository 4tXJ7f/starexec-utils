# starexec-utils

This repository is a collection of scripts that are useful for working with
StarExec. Note: these scripts are neither well written nor very well tested.

## Transferring solvers

To transfer solvers from one hierarchy to another, use `transfer_solvers.py`:

```
python3 transfer_solvers.py <from xml> <to xml>
```

Assuming that both hierarchies have the same structure, the script checks the
list of spaces *just below* the root in the `<from xml>` and collects the
solvers associated with each subspace. Then, it transfers them to the
corresponding subspaces in `<to xml>`. The result is stored in
`transfer_solvers.out.xml`.

## Filtering benchmarks

To keep benchmarks that have a certain attribute, use `filter_attributes.py`:

```
python3 filter_attributes.py <input xml> <attribute name> <attribute value>
```

This produces `filter_attributes.out.xml` where all benchmarks' `<attribute
name>` is `<attribute value>`.

To filter benchmarks by name, use `filter_benchmarks.py`:

```
python3 filter_benchmarks.py <input xml> <input xml> <benchmark list>
```

This produces `filter_benchmarks.out.xml` with only the benchmarks mentioned in
the `<benchmark list>`. The `<benchmark list>` is a simple file where each line
corresponds to a benchmark to keep.

## Analyzing results

The script `parse_results.py` checks whether the benchmarks were solved
correctly:

```
python3 parse_results.py <list of input CSVs>
```

This prints various statistics about the results received from the solvers:

- The number of completed benchmarks for each solver with a list of wrong
  benchmarks.
- The benchmarks that were solved multiple times with different results.
- The list of benchmarks with known results that were not solved by any of the
  solvers.

The script `parse_results_unknown.py` can be used to determine the expected
result for unknown benchmarks:

```
python3 parse_results_unknown.py <list of input CSVs>
```

It generates `results.csv` where each line corresponds to a benchmark that was
solved by at least two solvers. The second column corresponds to the result,
the rest of the columns (one per solver) indicates which solvers produced this
result (`--` means that the benchmark was either not run or did not finish on
the corresponding solver). For benchmarks where different solvers produced
different results, the solver prints out at a warning (these benchmarks are
also *not* included in the result file).

The script `analyze_output.py` analyzes the output of solvers (probably not
terribly useful).
