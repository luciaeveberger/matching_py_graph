#!flask/bin/python
from flask import Flask, request
import json

from data.create_bus_zones import create_accommodations_objects
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


def der_match():
    unassigned_buses = match_unassigned()
    for bus in unassigned_buses:
        possible_unis = [u for u in sorted_university if u.get_bus_id() == 0 and u.get_participant_capacity() < bus.get_capacity()]
        if possible_unis:
            optimal_combinations(bus, possible_unis)

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
    if len(remainder_list) != 0:
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
        bus_assigned_universities = [u for u in sorted_university if int(u.get_bus_id()) == i]
        acc_assigned = [u for u in accommodation_list if int(u.get_bus_id()) == i]
        helper_set_accommodations(acc_assigned, bus_assigned_universities)
        for uni in bus_assigned_universities:
            for val in uni.get_participant_list():
                return_object.append(val.__dict__)
    return return_object


@app.route('/', methods=['GET'])
def init():
    return 'I am up!'


@app.route('/', methods=['POST'])
def index():
    global accommodation_list
    global sorted_bus
    global sorted_university


    data = request.get_json()
    print(data)
    sorted_groups = create_accommodations_objects(data.get('data').get('accommodations'))
    accommodation_list = sorted_groups[0]
    sorted_bus = sorted_groups[1]
    sorted_university = create_participants(data.get('data').get('participants'))

    unassigned_universities = [u for u in sorted_university if u.get_bus_id() == 0]
    total_unassigned_people = sum(c.get_participant_capacity() for c in unassigned_universities)
    total_places = sum(c.get_capacity() for c in accommodation_list)

    initial_matcher()
    der_match()
    final_set = set_accommodations()
    json_block = {'data': final_set,
                  'unassigned_data': format_unmatched_data(),
                  'starting_data': {'total_people': total_unassigned_people,
                                    'total_places': total_places}
                  }
    return json.dumps(json_block)


@app.route('/with_wg', methods=['POST'])
def with_WG():
    global accommodation_list
    global sorted_bus
    global sorted_university

    data = request.get_json()
    print(data)
    sorted_groups = create_accommodations_objects(data.get('data').get('accommodations'))
    accommodation_list = sorted_groups[0]
    sorted_bus = sorted_groups[1]
    sorted_university = create_participants(data.get('data').get('participants'))
    print(sorted_university)

    initial_matcher()
    derivitive_match_WG()
    match_on_remainders()

    final_set = set_WG_accommodations()
    json_block = {'data': final_set, 'unassigned_data': format_unmatched_data()}
    return json.dumps(json_block)


def format_unmatched_data():
    unmatched_places = [u for u in accommodation_list if u.get_bus_id() == 0]
    unassigned_universities = [u for u in sorted_university if u.get_bus_id() == 0]
    unmatched_unis = [u for u in sorted_university if u.get_bus_id() == 0]
    unassigned_response = {'total_unassigned_participants':
                                sum(c.get_participant_capacity() for c in unassigned_universities),
                           'total_unassigned_accommodations':
                                sum(c.get_participant_capacity() for c in unmatched_places),
                           'unassigned_participants': [],
                           'unassigned_accommodations': []}

    for uni in unmatched_unis:
        create_uni = {'id': uni.get_university_id(), 'university': uni.get_university_name(), 'capacity': uni.get_participant_capacity()}
        unassigned_response['unassigned_participants'].append(create_uni)
    for places in unmatched_places:
        unassigned_response['unassigned_accommodations'].append(str(places))
    return unassigned_response




if __name__ == "__main__":
    # collects sorted data
    app.run(debug=True)



