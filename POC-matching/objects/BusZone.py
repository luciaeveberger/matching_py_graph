class BusZone:
    def __init__(self, _bz_id, _initial_capacity):
        self._bz_id = _bz_id
        self._initial_capacity = _initial_capacity
        self._current_capacity = _initial_capacity

    def get_id(self):
        return self._bz_id

    def get_capacity(self):
        return self._current_capacity

    def reduce_capacity(self, capacity):
        self._current_capacity = self._current_capacity - capacity
        #print("the current bus id", self._bz_id)
        #print("the current capacity is", self._current_capacity)

