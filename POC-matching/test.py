from data.create_bus_zones import create_dummy_data
from data.create_participants import create_participants
from objects.UniversityGroups import UniversityGroups


def inital_bus_matcher(sorted_university_list, sorted_bus_list):
    for uni in sorted_university_list:
        for bus in sorted_bus_list:
            if bus.get_capacity() >= uni.get_participant_capacity():
                current_bus = bus
                break
            else:
                current_bus = None
        if current_bus is None:
            break
        uni.set_bus_id(current_bus.get_id())
        current_bus.reduce_capacity(uni.get_participant_capacity())
    unasigned = [u for u in sorted_university_list if u.get_bus_id() == 0]
    for bus in sorted_bus:
        print(bus.get_capacity())
    return unasigned

def match_unassigned(unassigned_university, division_factor=1):
    #print("The count of unassigned", sum(c.get_participant_capacity() for c in unassigned_university))
    total_unassigned_people = sum(c.get_participant_capacity() for c in unassigned_university)
    available_buses = [b for b in sorted_bus if b.get_capacity() > 0]
    total_unassigned_bz = sum(c.get_capacity() for c in available_buses)

    print('count of unassigned', total_unassigned_people)
    print('total of open spots (bus)', total_unassigned_bz)
    for spot in available_buses:
        for element in unassigned_university:
            if spot.get_capacity() == element.get_participant_capacity():
                print("I match", element,  "with" , spot.get_id(), "with the capacity", spot.get_capacity())
                element.set_bus_id(spot.get_id())
                break

    first_pass = [u for u in sorted_university if u.get_bus_id() == 0]
    for elem in first_pass:
        print(elem)


if __name__ == "__main__":
    # collects sorted data
    sorted_bus = create_dummy_data()
    sorted_university = create_participants()

    unassigned = inital_bus_matcher(sorted_university, sorted_bus)
    match_unassigned(unassigned, 2)

