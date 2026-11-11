import csv, os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

cities = []
with open(os.path.join(__location__, 'Cities.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        cities.append(dict(r))


def filter_items(condition, dict_list):
    """
    Return a new list containing only the dictionaries that satisfy
    the given condition function.
    """
    return [item for item in dict_list if condition(item)]


def aggregate(aggregation_key, aggregation_function, dict_list):
    """
    Aggregate values associated with aggregation_key using the
    provided aggregation function.
    """
    values = []
    for item in dict_list:
        v = item[aggregation_key]
        try:
            v = float(v)
        except (TypeError, ValueError):
            pass
        values.append(v)
    return aggregation_function(values)


# Print the average temperature of all the cities
print("The average temperature of all the cities:")
print(aggregate("temperature", lambda t: sum(t) / len(t), cities))
print()

# Print all cities in Germany
print("All cities in Germany:")
germany_cities = filter_items(lambda c: c['country'] == 'Germany', cities)
for city in germany_cities:
    print(city)
print()

# Print all cities in Spain with a temperature above 12°C
print("Cities in Spain with temperature above 12°C:")
spain_hot = filter_items(lambda c: c['country'] == 'Spain' and float(c['temperature']) > 12, cities)
for city in spain_hot:
    print(city)
print()

# Count the number of unique countries
unique_countries = set(c['country'] for c in cities)
print("Number of unique countries:", len(unique_countries))
print()

# Print the average temperature for all the cities in Germany
print("Average temperature in Germany:", aggregate("temperature", lambda t: sum(t) / len(t), germany_cities))
print()

# Print the max temperature for all the cities in Italy
italy_cities = filter_items(lambda c: c['country'] == 'Italy', cities)
print("Max temperature in Italy:", aggregate("temperature", max, italy_cities))