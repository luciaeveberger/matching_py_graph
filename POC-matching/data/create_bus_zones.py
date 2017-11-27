from objects.BusZone import BusZone
from objects.Accommodation import Accommodation

import pandas as pd


def read_from_source():
    accomodations = pd.DataFrame.from_csv(
        '/Users/luciaeve/Documents/EMSE/code/matching_py_graph/POC-matching/data/accomodation.csv', encoding='latin-1',
        index_col=None, sep=',')
    return accomodations


def create_accommodations_objects():
    accommodations = read_from_source()
    accommodations_list = list()
    for index, row in accommodations.iterrows():
        university = Accommodation(row['buz_zone'], row.count(), row['capacity'], row['name'])
        accommodations_list.append(university)


def create_dummy_data():
    accommodations = read_from_source()
    accommodations_grouped_by_sum = accommodations.groupby('buz_zone').agg('sum')
    bus_zone = list()

    for index, row in accommodations_grouped_by_sum.iterrows():
        bz1 = BusZone(index, row['capacity'])
        bus_zone.append(bz1)

    sorted_bus = sorted(bus_zone, key=lambda x: x.get_capacity(), reverse=True)
    return sorted_bus

