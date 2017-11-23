class Participant:
    def __init__(self, _university_id, _university_name, _first_name=None, _last_name=None):
        self._university_id = _university_id
        self._university_name = _university_name
        self._bus_id = 0

    def set_bus_id(self, bus_id):
        self._bus_id = bus_id

    def __str__(self):
        return "university_id: %s, uni_name: %s,  bus_id %s" % \
               (self._university_id, self._university_name, self._bus_id)
