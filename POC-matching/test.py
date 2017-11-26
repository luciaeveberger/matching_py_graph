from data.create_bus_zones import create_dummy_data
from data.create_participants import create_participants
from objects.UniversityGroups import UniversityGroups

sorted_bus = create_dummy_data()
sorted_university = create_participants()


def initial_matcher():
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


def match_unassigned():
    unassigned_universities = [u for u in sorted_university if u.get_bus_id() == 0]
    total_unassigned_people = sum(c.get_participant_capacity() for c in unassigned_universities)
    available_buses = [b for b in sorted_bus if b.get_capacity() > 0]
    total_unassigned_bz = sum(c.get_capacity() for c in available_buses)

    print('count of unassigned', total_unassigned_people)
    print('total of open spots (bus)', total_unassigned_bz)
    total_remaining_buses = list()

    for bus_spot in available_buses:
        for element in unassigned_universities:
            if bus_spot.get_capacity() == element.get_participant_capacity():
                print("I match", element,  "with", bus_spot.get_id(), "with the capacity", bus_spot.get_capacity())
                element.set_bus_id(bus_spot.get_id())
                unassigned_universities.remove(element)
                bus_spot.reduce_capacity(element.get_participant_capacity())
                break
        if bus_spot.get_capacity() > 0:
            total_remaining_buses.append(bus_spot)
    return total_remaining_buses


def derivitive_match():
    unassigned_buses = match_unassigned()
    unassigned_universities = [u for u in sorted_university if u.get_bus_id() == 0]
    print(unassigned_universities)
    print(unassigned_buses)
    for bus in unassigned_buses:
        possible_unis = [u for u in sorted_university if u.get_bus_id() == 0 and u.get_participant_capacity() < bus.get_capacity()]
        if possible_unis:
            optimal_combinations(bus, possible_unis)
    available_buses = [b for b in sorted_bus if b.get_capacity() > 0]
    total_unassigned_bz = sum(c.get_capacity() for c in available_buses)
    unassigned_universities = [u for u in sorted_university if u.get_bus_id() == 0]
    total_unassigned_people = sum(c.get_participant_capacity() for c in unassigned_universities)
    print('total of open spots (bus)', total_unassigned_bz)
    print('toal people', total_unassigned_people)


def optimal_combinations(bus_zone, uni_list):
    capacity = bus_zone.get_capacity()
    sorted_unis = sorted(uni_list, key=lambda x: x.get_participant_capacity(), reverse=True)

    sorted_unis[0].set_bus_id(bus_zone.get_id())
    bus_zone.reduce_capacity(sorted_unis[0].get_participant_capacity())
    sorted_unis.remove(sorted_unis[0])
    for uni in sorted_unis:
        if bus_zone.get_capacity() == 0:
            return
        if bus_zone.get_capacity() >= uni.get_participant_capacity():
            uni.set_bus_id(bus_zone.get_id())
            bus_zone.reduce_capacity(uni.get_participant_capacity())


if __name__ == "__main__":
    # collects sorted data
    initial_matcher()
    derivitive_match()


