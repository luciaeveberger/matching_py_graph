import pandas as pd
from objects.BusZone import BusZone
from objects.UniversityGroups import UniversityGroups


external_requests = pd.DataFrame.from_csv('participants.csv', encoding='latin-1', index_col=None, sep=';')
accom = pd.DataFrame.from_csv('accomodation.csv', encoding='latin-1', index_col=None, sep=',')

print('total places', sum(accom['capacity']))
print('total people', sum(external_requests['number']))


if __name__ == "__main__":
    university_list = []
    for index, row in external_requests.iterrows():
        university = UniversityGroups(row['university'], row['number'])
        university_list.append(university)

    bus_zone = []
    bz1 = BusZone(1, 80)
    bz2 = BusZone(2, 145)
    bz3 = BusZone(3,152)
    bus_zone.append(bz1)
    bus_zone.append(bz2)
    bus_zone.append(bz3)

    # sorting the bus zone
    sorted_bus = sorted(bus_zone, key=lambda x: x.get_capacity(), reverse=True)

    sorted_university = sorted(university_list, key=lambda x: x.get_participant_capacity(), reverse=True)

    for uni in sorted_university:
        for bus in sorted_bus:
            if bus.get_capacity() >= uni.get_participant_capacity():
                current_bus = bus
                break
            else:
                current_bus = None
        if current_bus is None:
            break
        uni.set_bus_id(current_bus.get_id())
        current_bus.reduce_capacity(uni.get_participant_capacity())
    unasigned=[u for u in sorted_university if u.get_bus_id() == 0]
    print(len(unasigned))
    for item in unasigned:
        print(item)