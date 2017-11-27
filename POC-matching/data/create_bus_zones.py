from objects.BusZone import BusZone
from objects.Accommodation import Accommodation

import pandas as pd


def create_dummy_data():
    accomodations = pd.DataFrame.from_csv(
        '/Users/luciaeve/Documents/EMSE/code/matching_py_graph/POC-matching/data/accomodation.csv', encoding='latin-1',
        index_col=None, sep=',')
    accomodations_list = []

    for index, row in accomodations.iterrows():
        university = Accommodation(row['buz_zone'], row['capacity'], row['name'])
        accomodations_list.append(university)

    sum_accom = accomodations.groupby('buz_zone').agg('sum')

    bus_zone = []
    for index, row in sum_accom.iterrows():
        bz1 = BusZone(index, row['capacity'])
        bus_zone.append(bz1)

    sorted_bus = sorted(bus_zone, key=lambda x: x.get_capacity(), reverse=True)
    return sorted_bus
