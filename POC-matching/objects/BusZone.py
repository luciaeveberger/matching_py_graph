class BusZone:
    def __init__(self, _bz_id, _initial_capacity, _coordinates=None):
        self._bz_id = _bz_id
        self._initial_capacity = _initial_capacity
        self._current_capacity = _initial_capacity
        self._coordinates = _coordinates

    def get_id(self):
        return self._bz_id

    def get_capacity(self):
        return self._current_capacity

    def reduce_capacity(self, capacity):
        self._current_capacity = self._current_capacity - capacity
        #print("the current bus id", self._bz_id)
        #print("the current capacity is", self._current_capacity)

    def __str__(self):
        return "bus_id: %s, bus_capacity: %s" % (self._bz_id, self._current_capacity)

