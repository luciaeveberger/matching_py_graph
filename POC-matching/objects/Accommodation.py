class Accommodation:
    def __init__(self, _bz_id, _initial_capacity,_acc_id, _name, _coordinates=None):
        self._bz_id = _bz_id
        self._acc_id = _acc_id
        self._initial_capacity = _initial_capacity
        self._name = _name
        self._current_capacity = _initial_capacity

    def get_bus_id(self):
        return self._bz_id

    def get_acc_id(self):
        return self._acc_id

    def get_capacity(self):
        return self._current_capacity

    def get_name(self):
        return self._name

    def reduce_capacity(self, capacity):
        self._current_capacity = self._current_capacity - capacity

    def __str__(self):
        return "accommodation: %s, bus_id: %s, capacity: %s, accom_id: %s" % \
               (self._name, self._bz_id, self._current_capacity, self._acc_id)
