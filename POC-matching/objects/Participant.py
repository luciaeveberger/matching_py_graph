class Participant:
    def __init__(self, _university_id, _university_name, _first_name=None, _last_name=None):
        self._university_id = _university_id
        self._university_name = _university_name
        self._bus_id = 0
        self._accommondation_details = 0

    def set_bus_id(self, bus_id):
        self._bus_id = bus_id

    def set_accomondation(self, accomondation_details):
        self._accommondation_details = accomondation_details

    def get_acc_id(self):
        return self._accommondation_details

    def __str__(self):
        return "university_id: %s, uni_name: %s,  bus_id %s, accomodation_details: %s" % \
               (self._university_id, self._university_name,
                self._bus_id, self._accommondation_details)
