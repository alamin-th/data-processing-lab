import csv, os
from pathlib import Path

class DataLoader:
    """Handles loading CSV data files."""

    def __init__(self, base_path=None):
        if base_path is None:
            self.base_path = Path(__file__).parent.resolve()
        else:
            self.base_path = Path(base_path)

    def load_csv(self, filename):
        filepath = self.base_path / filename
        data = []
        with filepath.open() as f:
            rows = csv.DictReader(f)
            for row in rows:
                data.append(dict(row))
        return data

class DB:
    """A simple in-memory database that stores Table objects, keyed by name."""

    def __init__(self):
        self.tables = {}

    def insert(self, table):
        self.tables[table.table_name] = table

    def search(self, table_name):
        return self.tables.get(table_name)

class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table

    def filter(self, condition):
        filtered = [row for row in self.table if condition(row)]
        return Table(self.table_name + '_filtered', filtered)

    def aggregate(self, aggregation_function, aggregation_key):
        values = []
        for row in self.table:
            v = row[aggregation_key]
            try:
                v = float(v)
            except (TypeError, ValueError):
                pass
            values.append(v)
        return aggregation_function(values)

    def join(self, other_table, key):
        joined = []
        for row in self.table:
            for other_row in other_table.table:
                if row[key] == other_row[key]:
                    merged = {**row, **other_row}
                    joined.append(merged)
        new_name = self.table_name + '_' + other_table.table_name + '_joined'
        return Table(new_name, joined)

    def __str__(self):
        return self.table_name + ':' + str(self.table)

loader = DataLoader()
cities = loader.load_csv('Cities.csv')
table1 = Table('cities', cities)
countries = loader.load_csv('Countries.csv')
table2 = Table('countries', countries)

my_DB = DB()
my_DB.insert(table1)
my_DB.insert(table2)

my_table1 = my_DB.search('cities')
print("List all cities in Italy:")
my_table1_filtered = my_table1.filter(lambda x: x['country'] == 'Italy')
print(my_table1_filtered)
print()

print("Average temperature for all cities in Italy:")
print(my_table1_filtered.aggregate(lambda x: sum(x)/len(x), 'temperature'))
print()

my_table2 = my_DB.search('countries')
print("List all non-EU countries:")
my_table2_filtered = my_table2.filter(lambda x: x['EU'] == 'no')
print(my_table2_filtered)
print()

print("Number of countries that have coastline:")
print(my_table2.filter(lambda x: x['coastline'] == 'yes').aggregate(lambda x: len(x), 'coastline'))
print()

my_table3 = my_table1.join(my_table2, 'country')
print("First 5 entries of the joined table (cities and countries):")
for item in my_table3.table[:5]:
    print(item)
print()

print("Cities whose temperatures are below 5.0 in non-EU countries:")
my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'no').filter(lambda x: float(x['temperature']) < 5.0)
print(my_table3_filtered.table)
print()

print("The min and max temperatures for cities in EU countries that do not have coastlines")
my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'yes').filter(lambda x: x['coastline'] == 'no')
print("Min temp:", my_table3_filtered.aggregate(lambda x: min(x), 'temperature'))
print("Max temp:", my_table3_filtered.aggregate(lambda x: max(x), 'temperature'))
print()