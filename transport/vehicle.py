import uuid

class Vehicle:
    def __init__(self, capacity):
        self.vehicle_id = str(uuid.uuid4())
        self.capacity = capacity
        self.current_load = 0
        self.clients_list = []

    def can_load(self, client):
        return self.current_load + client.cargo_weight <= self.capacity

    def load_cargo(self, client):
        if self.can_load(client):
            self.current_load += client.cargo_weight
            self.clients_list.append(client)
            return True
        return False

    def __str__(self):
        return f"ID транспорта:{self.vehicle_id},грузоподъёмность:{self.capacity},текущая загрузка:{self.current_load}"


class Train(Vehicle):
    
    def __init__(self, capacity, number_of_cars):
        super().__init__(capacity)
        self.number_of_cars = number_of_cars   


class Airplane(Vehicle):

    def __init__(self, capacity, max_altitude):
        super().__init__(capacity)
        self.max_altitude = max_altitude

