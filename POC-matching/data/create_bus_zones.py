from objects.BusZone import BusZone
from objects.Accommodation import Accommodation

import pandas as pd


def read_from_source():
    accomodations = pd.DataFrame.from_csv(
        '/Users/luciaeve/Documents/EMSE/code/matching_py_graph/POC-matching/data/WG.csv', encoding='latin-1',
        index_col=None, sep=',')
    return accomodations


def create_accommodations_objects(accommodations):
    accommodations = pd.DataFrame(accommodations)
    accommodations_list = list()
    count = 0
    for index, row in accommodations.iterrows():
        university = Accommodation(row['buz_zone'], int(row['capacity']), row['id'], row['name'])
        accommodations_list.append(university)
        count = count + 1
    accommodations_grouped_by_sum = accommodations.groupby('buz_zone').agg('sum')
    bus_zone = list()

    for index, row in accommodations_grouped_by_sum.iterrows():
        bz1 = BusZone(int(index), int(row['capacity']))
        bus_zone.append(bz1)

    sorted_bus = sorted(bus_zone, key=lambda x: x.get_capacity(), reverse=True)

    sorted_accomodation_list = sorted(accommodations_list, key=lambda x: x.get_capacity(), reverse=True)
    return sorted_accomodation_list, sorted_bus


def create_WG_objects():
    accommodations = read_from_source()
    count = 1
    accommodations_list = list()
    for index, row in accommodations.iterrows():
        university = Accommodation(row['buz_zone'], int(row['capacity']), count, row['name'])
        accommodations_list.append(university)
        count = count + 1
    accommodations_grouped_by_sum = accommodations.groupby('buz_zone').agg('sum')
    bus_zone = list()

    for index, row in accommodations_grouped_by_sum.iterrows():
        bz1 = BusZone(int(index), int(row['capacity']))
        bus_zone.append(bz1)

    sorted_bus = sorted(bus_zone, key=lambda x: x.get_capacity(), reverse=True)

    sorted_accomodation_list = sorted(accommodations_list, key=lambda x: x.get_capacity(), reverse=True)
    return sorted_accomodation_list, sorted_bus

