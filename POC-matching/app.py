#!flask/bin/python
from flask import Flask, request
import json

from data.create_bus_zones import create_accommodations_objects, create_WG_objects
from data.create_participants import create_participants
from objects.UniversityGroups import UniversityGroups


app = Flask(__name__)
sorted_bus = list()
sorted_university = list()
accommodation_list = list()
file = open('results/testfile.txt', 'w')


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
    total_remaining_buses = list()

    for bus_spot in available_buses:
        for element in unassigned_universities:
            if bus_spot.get_capacity() == element.get_participant_capacity():
                element.set_bus_id(bus_spot.get_id())
                unassigned_universities.remove(element)
                bus_spot.reduce_capacity(element.get_participant_capacity())
                break
        if bus_spot.get_capacity() > 0:
            total_remaining_buses.append(bus_spot)
    return total_remaining_buses


def derivitive_match():
    unassigned_buses = match_unassigned()
    for bus in unassigned_buses:
        possible_unis = [u for u in sorted_university if u.get_bus_id() == 0 and u.get_participant_capacity() < bus.get_capacity()]
        if possible_unis:
            optimal_combinations(bus, possible_unis)
    available_buses = [b for b in sorted_bus if b.get_capacity() > 0]
    unassigned_acc = [u for u in accommodation_list if u.get_bus_id() == 0]
    total_unassigned_bz = sum(c.get_capacity() for c in available_buses)
    unassigned_universities = [u for u in sorted_university if u.get_bus_id() == 0]
    total_unassigned_people = sum(c.get_participant_capacity() for c in unassigned_universities)
    unassigned_universities = [u for u in sorted_university if u.get_bus_id() == 0]
    unassigned_dict = {'unassigned_busses': [],
                       'count_un_busses': total_unassigned_bz,
                       'unassigned_unis': [],
                       'count_unassigned_people': total_unassigned_people,
                       'unassigned_accommodations': []
                       }
    for val in unassigned_buses:
        unassigned_dict['unassigned_busses'].append(str(val))

    print(accommodation_list)
    for val in unassigned_acc:
        demo = {'name': val.get_name(), 'capacity': val.get_capacity(), 'buz_zone':val.get_bus_id()}
        unassigned_dict['unassigned_accommodations'].append(demo)

    for val in unassigned_universities:
        demo = {'id': val.get_university_id(), 'university': val.get_university_name(), 'capacity': val.get_participant_capacity()}
        unassigned_dict['unassigned_unis'].append(demo)

    return unassigned_dict


def optimal_combinations(bus_zone, uni_list):
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


def helper_set_accommodations(acc_assigned, bus_assigned_universities):
    for spot in acc_assigned:
        for uni in bus_assigned_universities:
            for val in uni.get_participant_list():
                if val.get_acc_id() == 0 and spot.get_capacity() > 0:
                    acc_details = {'id': spot.get_acc_id(), 'name': spot.get_name(), 'bus_zone': spot.get_bus_id()}
                    val.set_accomondation(acc_details)
                    uni.set_accommodation_id(spot.get_acc_id())
                    spot.reduce_capacity(1)


def set_accommodations():
    return_object = list()

    for i in range(1, 4):
        bus_assigned_universities = [u for u in sorted_university if u.get_bus_id() == i]
        acc_assigned = [u for u in accommodation_list if int(u.get_bus_id()) == i]

        for spot in acc_assigned:
            for uni in bus_assigned_universities:
                for val in uni.get_participant_list():
                    if val.get_acc_id() == 0 and spot.get_capacity() > 0:
                        print(spot)
                        acc_details = {'id': spot.get_acc_id(), 'name': spot.get_name(), 'bus_zone': spot.get_bus_id()}
                        val.set_accomondation(acc_details)
                        uni.set_accommodation_id(spot.get_acc_id)
                        spot.reduce_capacity(1)
        for uni in bus_assigned_universities:
            for val in uni.get_participant_list():
                return_object.append(val.__dict__)
                file.write(str(val) + '\n')
    return return_object


def helper_WG_set_accommodations(acc_assigned, bus_assigned_universities):
    for spot in acc_assigned:
        for uni in bus_assigned_universities:
            for val in uni.get_participant_list():
                if val.get_acc_id() == 0 and spot.get_capacity() > 0:
                    acc_details = {'id': spot.get_acc_id(), 'name': spot.get_name(), 'bus_zone': spot.get_bus_id()}
                    val.set_accomondation(acc_details)
                    spot.reduce_capacity(1)


def match_on_remainders():
    # need to fix this method!
    unmatched_unis = [u for u in sorted_university if u.get_bus_id() == 0]
    unmatched_buses = [u for u in sorted_bus if u.get_capacity() != 0]
    remainder_list = []
    for bus in unmatched_buses:
        for uni in unmatched_unis:
            temp_sum = bus.get_capacity() - uni.get_participant_capacity()
            pair = {'uni': uni, 'bus': bus, 'remainder':temp_sum}
            remainder_list.append(pair)
    rem = remainder_list[len(remainder_list)-1].get('remainder')
    uni = remainder_list[len(remainder_list) - 1].get('uni')
    bus = remainder_list[len(remainder_list) - 1].get('bus')
    uni.set_new_capacity(bus.get_capacity())
    uni.set_bus_id(bus.get_id())
    bus.reduce_capacity(bus.get_capacity())
    sorted_university.append(UniversityGroups(uni.get_university_id(), uni.get_university_name(), abs(rem)))


def derivitive_match_WG():
    unassigned_buses = match_unassigned()
    for bus in unassigned_buses:
        possible_unis = [u for u in sorted_university if u.get_bus_id() == 0 and u.get_participant_capacity() < bus.get_capacity()]
        if possible_unis:
            optimal_combinations(bus, possible_unis)
    available_buses = [b for b in sorted_bus if b.get_capacity() > 0]


def set_WG_accommodations():
    return_object = list()
    for i in range(1, 4):
        bus_assigned_universities = [u for u in sorted_university if u.get_bus_id() == i]
        acc_assigned = [u for u in accommodation_list if int(u.get_bus_id()) == i]
        helper_set_accommodations(acc_assigned, bus_assigned_universities)
        for uni in bus_assigned_universities:
            for val in uni.get_participant_list():
                return_object.append(val.__dict__)
    return return_object



@app.route('/', methods=['POST'])
def index():
    global accommodation_list
    global sorted_bus
    global sorted_university

    data = request.get_json()
    print(json.dumps(data))
    sorted_groups = create_accommodations_objects(data.get('data').get('accommodations'))
    accommodation_list = sorted_groups[0]

    for val in accommodation_list:
        print(val)
    sorted_bus = sorted_groups[1]
    sorted_university = create_participants(data.get('data').get('participants'))

    unassigned_universities = [u for u in sorted_university if u.get_bus_id() == 0]
    total_unassigned_people = sum(c.get_participant_capacity() for c in unassigned_universities)
    total_places = sum(c.get_capacity() for c in accommodation_list)
    print('STARTING SUM:', total_unassigned_people)
    print('STARTING PLACES:', total_places)


    initial_matcher()
    unassigned_information = derivitive_match()
    final_set = set_accommodations()
    json_block = {'data': final_set, 'unassigned_data': unassigned_information}
    return json.dumps(json_block)


@app.route('/with_wg', methods=['POST'])
def with_WG():
    global accommodation_list
    global sorted_bus
    global sorted_university
    data = request.get_json()

    sorted_groups = create_accommodations_objects(data.get('data').get('accommodations'))
    accommodation_list = sorted_groups[0]
    sorted_bus = sorted_groups[1]
    sorted_university = create_participants(data.get('data').get('participants'))

    initial_matcher()
    derivitive_match_WG()
    match_on_remainders()
    final_set = set_WG_accommodations()
    unmatched_places = [u for u in accommodation_list if u.get_bus_id() == 0]
    unmatched_busses = [u for u in sorted_bus if u.get_id() == 0]
    unassigned_universities = [u for u in sorted_university if u.get_bus_id() == 0]

    for uni in sorted_university:
        print('here', uni)
    total_unassigned_people = sum(c.get_participant_capacity() for c in unassigned_universities)

    print('UNASSIGNED ', total_unassigned_people)
    print('the size is accomodations', len(unmatched_busses))
    print('the size of the busses', len(unmatched_places))

    unmatched_unis = [u for u in sorted_university if u.get_bus_id() == 0]
    uni_list = []
    for uni in unmatched_unis:
        uni_list.append(str(uni))
    json_block = {'data': final_set, 'unassigned_data': uni_list}

    return json.dumps(json_block)


if __name__ == "__main__":
    # collects sorted data
    app.run(debug=True)



