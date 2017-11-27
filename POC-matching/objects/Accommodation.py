class Accommodation:
    def __init__(self, _bz_id, _initial_capacity, _name, _coordinates=None):
        self._bz_id = _bz_id
        self._initial_capacity = _initial_capacity
        self._name = _name

    def get_id(self):
        return self._bz_id

    def get_capacity(self):
        return self._current_capacity

    def reduce_capacity(self, capacity):
        self._current_capacity = self._current_capacity - capacity