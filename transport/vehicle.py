import uuid

class Vehicle:
    def __init__(self, capacity):
        if capacity.isdigit() or int(capacity)>0:
            self.vehicle_id = str(uuid.uuid4())
            self.capacity = capacity
            self.current_load = 0
            self.clients_list = []
        raise ValueError("Грузоподъемность должна быть положительным числом!")

    def can_load(self, client):
        if client.cargo_weight.isdigit() and client.cargo_weight>0:
            return self.current_load + client.cargo_weight <= self.capacity
        raise ValueError("Вес груза клиента должен быть положительным числом!")


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
        if number_of_cars.isdigit() or int(number_of_cars)>0:
            super().__init__(capacity)
            self.number_of_cars = number_of_cars
        raise ValueError("Количество вагонов должно быть положительным числом!")


class Airplane(Vehicle):

    def __init__(self, capacity, max_altitude):
        if max_altitude.isdigit() or int(max_altitude)>0:
            super().__init__(capacity)
            self.max_altitude = max_altitude
        raise ValueError("Высота полета должна быть положительным числом!")
        

