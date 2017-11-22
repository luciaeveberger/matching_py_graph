from objects.BusZone import BusZone


def create_dummy_data():
    bus_zone = []
    bz1 = BusZone(1, 250)
    bz2 = BusZone(2, 100)
    bz3 = BusZone(3, 30)
    bus_zone.append(bz1)
    bus_zone.append(bz2)
    bus_zone.append(bz3)
    sorted_bus = sorted(bus_zone, key=lambda x: x.get_capacity(), reverse=True)
    return sorted_bus
