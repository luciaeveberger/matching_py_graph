from .Participant import Participant


class UniversityGroups:
    def __init__(self, _university_id, _university, _participant_count):
        self._university_id = _university_id
        self._university = _university
        self._participant_count = _participant_count
        self._bus_id = 0
        self._list_of_participants = list()
        self.create_participant_list()

    def create_participant_list(self):
        for i in range(self._participant_count):
            new_participant = Participant(
                self.get_university_id(),
                self.get_university_name(),
                'Alex',
                'Fish')
            self._list_of_participants.append(new_participant)

    def get_university_id(self):
        return self._university_id

    def get_university_name(self):
        return self._university

    def get_participant_capacity(self):
        return self._participant_count

    def set_bus_id(self, bus_id):
        self._bus_id = bus_id
        for participant in self._list_of_participants:
            participant._bus_id = bus_id

    def get_bus_id(self):
        return self._bus_id

    def get_participant_list(self):
        return self._list_of_participants

    def __str__(self):
        return "university: %s, bus_id: %s, capacity: %s" % (self._university, self._bus_id, self._participant_count)
