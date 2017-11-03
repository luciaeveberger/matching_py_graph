class UniversityGroups:
    def __init__(self, _university, _participant_count):
        self._university = _university
        self._participant_count = _participant_count
        self._bus_id = 0

    def get_university_name(self):
        return self._university

    def get_participant_capacity(self):
        return self._participant_count

    def set_bus_id(self, bus_id):
        self._bus_id = bus_id

    def get_bus_id(self):
        return self._bus_id

    def __str__(self):
        return "university: %s, bus_id: %s" % (self._university, self._bus_id)
