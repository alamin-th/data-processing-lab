# OOP Data Processing Lab

## Lab Overview

This lab refactors the earlier procedural data-processing script (Commit 1 & 2)
into an object-oriented design. Instead of loose functions operating on a
list of dictionaries, the data is now wrapped in classes:

- **`DataLoader`** reads a CSV file from disk and converts it into a list of
  dictionaries (one dictionary per row).
- **`Table`** wraps a list of dictionaries and exposes `filter`, `aggregate`,
  and `join` operations as methods, so queries can be chained
  (e.g. `table.filter(...).aggregate(...)`).
- **`DB`** acts as a tiny in-memory database: it stores `Table` objects by
  name and lets you retrieve (`search`) them later, modeling how multiple
  related tables would be managed in a real database.

## Project Structure

```
data-processing-lab/
│
├── README.md              # This file
├── Cities.csv              # Cities dataset
├── Countries.csv           # Countries dataset
└── data_processing.py      # OOP implementation (DataLoader, DB, Table) + test/demo code
```

## Design Overview

### `DataLoader`
- **Attributes**
  - `base_path` (`Path`): directory to look for CSV files in. Defaults to
    the directory containing `data_processing.py`.
- **Key methods**
  - `__init__(self, base_path=None)`: sets `base_path`.
  - `load_csv(self, filename)`: opens `base_path/filename`, reads it with
    `csv.DictReader`, and returns the rows as a `list[dict]`.

### `Table`
- **Attributes**
  - `table_name` (`str`): a label for the table, used in `__str__` and to
    name the result of `filter`/`join`.
  - `table` (`list[dict]`): the rows of the table.
- **Key methods**
  - `__init__(self, table_name, table)`: stores the name and rows.
  - `filter(self, condition)`: returns a **new** `Table` containing only the
    rows for which `condition(row)` is `True`. `condition` is any
    one-argument function (typically a `lambda`) that takes a row (dict)
    and returns a bool. Non-destructive — the original table is unchanged.
  - `aggregate(self, aggregation_function, aggregation_key)`: pulls out the
    values under `aggregation_key` from every row (converting to `float`
    when possible, so numeric columns can be summed/averaged), then calls
    `aggregation_function` on that list of values and returns the result.
    This lets the same method support `sum`, `max`, `min`, `len`, or any
    custom `lambda` (e.g. average, unique count).
  - `join(self, other_table, key)`: returns a **new** `Table` whose rows are
    the merged dictionaries of every pair of rows (one from `self`, one
    from `other_table`) whose `key` field matches. Mirrors a SQL inner join.
  - `__str__(self)`: renders the table as `"<table_name>:<rows>"`, so
    `print(a_table)` gives a readable summary.

### `DB`
- **Attributes**
  - `tables` (`dict[str, Table]`): maps a table name to its `Table` object.
- **Key methods**
  - `__init__(self)`: starts with an empty `tables` dict.
  - `insert(self, table)`: registers a `Table` object under `table.table_name`.
  - `search(self, table_name)`: returns the `Table` registered under that
    name (or `None` if not found).

## How to Test and Run Your Code

Make sure `Cities.csv` and `Countries.csv` are in the same folder as
`data_processing.py`, then run:

```bash
python data_processing.py
```

This executes the demo/test queries at the bottom of the file (filtering
cities by country/temperature, aggregating temperatures, counting unique
countries, and joining the `cities` and `countries` tables) and prints the
results to the console. Compare the printed output against the expected
results to confirm the implementation is correct.