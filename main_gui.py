import dearpygui.dearpygui as dpg
import json
from transport import Client, Vehicle, TransportCompany, Train, Airplane


company = TransportCompany("My transport company")


def update_clients_table():
    dpg.delete_item("clients_table", children_only=True)
    for client in company.clients:
        with dpg.table_row(parent="clients_table"):
            dpg.add_text(client.name)
            dpg.add_text(str(client.cargo_weight))
            dpg.add_text("Да" if client.is_vip else "Нет")

def update_vehicles_table():
    dpg.delete_item("vehicles_table", children_only=True)
    for vehicle in company.vehicles:
        with dpg.table_row(parent="vehicles_table"):
            dpg.add_text(str(vehicle.vehicle_id))
            dpg.add_text(str(vehicle.capacity))
            dpg.add_text(str(vehicle.current_load))

def show_client_form():
    if dpg.does_item_exist("client_form"):
        return
    with dpg.window(label="Добавить клиента", width=400, height=250, modal=True, tag="client_form"):
        dpg.add_text("Имя клиента:")
        dpg.add_input_text(tag="client_name", width=250)
        dpg.add_text("Вес груза:")
        dpg.add_input_text(tag="client_weight", width=250)
        dpg.add_text("VIP статус:")
        dpg.add_checkbox(tag="client_vip")
        dpg.add_button(label="Сохранить", callback=save_client)
        dpg.add_button(label="Отмена", callback=lambda: dpg.delete_item("client_form"))

def save_client():
    name = dpg.get_value("client_name")
    weight = dpg.get_value("client_weight")
    vip = dpg.get_value("client_vip")

    if name and weight.isdigit() and int(weight) > 0:
        client = Client(name, int(weight), vip)
        company.add_client(client)  
        update_clients_table()  
        dpg.delete_item("client_form")  
    else:
        dpg.set_value("status", "Ошибка: Проверьте введённые данные!")

def get_authorized_clients():
    return [client for client in company.clients if client.is_vip]



def show_authorized_clients():
    if dpg.does_item_exist("authorized_clients_window"):
        dpg.delete_item("authorized_clients_window")
    with dpg.window(label="Авторизованные клиенты", width=400, height=300, modal=True, tag="authorized_clients_window"):
        dpg.add_text("Список VIP клиентов")
        with dpg.table(header_row=True):
            dpg.add_table_column(label="Имя клиента")
            dpg.add_table_column(label="Вес груза")
            for client in get_authorized_clients():
                with dpg.table_row():
                    dpg.add_text(client.name)
                    dpg.add_text(str(client.cargo_weight))


def update_clients_table():
    dpg.delete_item("clients_table", children_only=True)  
    for client in company.clients:  
        with dpg.table_row(parent="clients_table"):
            dpg.add_text(client.name)
            dpg.add_text(str(client.cargo_weight))
            dpg.add_text("Да" if client.is_vip else "Нет")

def show_all_clients():

    if dpg.does_item_exist("all_clients_window"):
        return
    with dpg.window(label="Все клиенты", modal=True, width=600, height=400, tag="all_clients_window"):
        with dpg.table(header_row=True):
            dpg.add_table_column(label="Имя клиента")
            dpg.add_table_column(label="Вес груза")
            dpg.add_table_column(label="VIP статус")
            for client in company.clients:
                with dpg.table_row():
                    dpg.add_text(client.name)  # Имя клиента
                    dpg.add_text(str(client.cargo_weight))  # Вес груза
                    dpg.add_text("Да" if client.is_vip else "Нет")  # VIP статус
        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item("all_clients_window"))


def show_vehicle_form():
    if dpg.does_item_exist("vehicle_form"):
        return
    with dpg.window(label="Добавить транспорт", width=400, height=250, modal=True, tag="vehicle_form"):
        dpg.add_text("Тип транспорта:")
        dpg.add_combo(["Самолет", "Поезд"], tag="vehicle_type", width=250)
        dpg.add_text("Грузоподъемность (тонны):")
        dpg.add_input_text(tag="vehicle_capacity", width=250)
        dpg.add_button(label="Сохранить", callback=save_vehicle)
        dpg.add_button(label="Отмена", callback=lambda: dpg.delete_item("vehicle_form"))

def save_vehicle():
    vehicle_type = dpg.get_value("vehicle_type")
    capacity = dpg.get_value("vehicle_capacity")

    if capacity.isdigit() and int(capacity) > 0:
        capacity = int(capacity)
        if vehicle_type == "Самолет":
            vehicle = Airplane(capacity, 10000) 
        elif vehicle_type == "Поезд":
            vehicle = Train(capacity, 10000)  
        else:
            vehicle = Vehicle(capacity)  
        
        company.add_vehicle(vehicle)  
        update_vehicles_table()  
        dpg.delete_item("vehicle_form")  
    else:
        dpg.set_value("status", "Ошибка: Проверьте введённые данные!")

def get_authorized_vehicles():
    return [vehicle for vehicle in company.vehicles if vehicle.current_load / vehicle.capacity > 0.5]

def show_authorized_vehicles():
    if dpg.does_item_exist("authorized_vehicles_window"):
        dpg.delete_item("authorized_vehicles_window")
    with dpg.window(label="Авторизованные грузовики", width=400, height=300, modal=True, tag="authorized_vehicles_window"):
        dpg.add_text("Грузовики с загрузкой более 50%")
        with dpg.table(header_row=True):
            dpg.add_table_column(label="ID грузовика")
            dpg.add_table_column(label="Загрузка (%)")
            for vehicle in get_authorized_vehicles():
                with dpg.table_row():
                    dpg.add_text(str(vehicle.vehicle_id))
                    dpg.add_text(f"{(vehicle.current_load / vehicle.capacity) * 100:.1f}%")


def update_vehicles_table():
    dpg.delete_item("vehicles_table", children_only=True) 
    for vehicle in company.vehicles:  
        with dpg.table_row(parent="vehicles_table"):
            dpg.add_text(str(vehicle.vehicle_id))
            dpg.add_text(str(vehicle.capacity))
            dpg.add_text(str(vehicle.current_load))

def show_all_vehicles():

    if dpg.does_item_exist("all_vehicles_window"):
        return
    with dpg.window(label="Все транспортные средства", modal=True, width=600, height=400, tag="all_vehicles_window"):
        with dpg.table(header_row=True):
            dpg.add_table_column(label="ID")
            dpg.add_table_column(label="Грузоподъемность")
            dpg.add_table_column(label="Текущая загрузка")
            for vehicle in company.vehicles:
                with dpg.table_row():
                    dpg.add_text(str(vehicle.vehicle_id)) 
                    dpg.add_text(str(vehicle.capacity))  
                    dpg.add_text(str(vehicle.current_load))  
        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item("all_vehicles_window"))



def distribute_cargo():
    company.optimize_cargo_distribution()
    update_vehicles_table()

def export_results():
    data = {
        "clients": [{"name": c.name, "cargo_weight": c.cargo_weight, "is_vip": c.is_vip} for c in company.clients],
        "vehicles": [{"vehicle_id": v.vehicle_id, "capacity": v.capacity, "current_load": v.current_load} for v in company.vehicles]
    }
    with open("export_results.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    dpg.set_value("status", "Результаты экспортированы в файл export_results.json")

def show_about():
    if dpg.does_item_exist("about_window"):
        return  

    with dpg.window(label="О программе", modal=True, width=400, height=200, tag="about_window"):
        dpg.add_text("Лабораторная работа номер 12")
        dpg.add_text("Вариант: 4")
        dpg.add_text("Группа 81 ТП")
        dpg.add_text("Разработчик: Севрук Владислав Сергеевич")
        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item("about_window"))


last_key_pressed = None

def setup_key_handlers():

    def handle_key_press():
        global last_key_pressed
        if last_key_pressed == dpg.mvKey_Escape:

            for window in ["client_form", "vehicle_form", "authorized_clients_window", "authorized_vehicles_window", "about_window","all_clients_window","all_vehicles_window"]:
                if dpg.does_item_exist(window):
                    dpg.delete_item(window)
        elif last_key_pressed == dpg.mvKey_Return:

            if dpg.does_item_exist("client_form"):
                save_client()
            elif dpg.does_item_exist("vehicle_form"):
                save_vehicle()


    with dpg.handler_registry():
        dpg.add_key_press_handler(callback=lambda sender, app_data: set_last_key(app_data))
        dpg.add_key_release_handler(callback=lambda sender, app_data: handle_key_press())

def set_last_key(key):
    global last_key_pressed
    last_key_pressed = key

def setup_fonts():
    with dpg.font_registry():
        with dpg.font("/System/Library/Fonts/ArialHB.ttf", 20) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
            dpg.bind_font(default_font)


def main_window():
    with dpg.window(label="Основное окно", width=800, height=600):
        dpg.add_button(label="О программе", callback=show_about)

        with dpg.group(horizontal=True):

            with dpg.group():
                dpg.add_text("Клиенты", tag="clients_text")
                with dpg.table(tag="clients_table", header_row=True):
                    dpg.add_table_column(label="Имя клиента")
                    dpg.add_table_column(label="Вес груза")
                    dpg.add_table_column(label="VIP статус")
                dpg.add_button(label="Добавить клиента", callback=show_client_form)
                dpg.add_button(label="Показать всех клиентов", callback=show_all_clients)
                dpg.add_button(label="Показать VIP клиентов", callback=show_authorized_clients)
                


            with dpg.group():
                dpg.add_text("Транспортные средства", tag="vehicles_text")
                with dpg.table(tag="vehicles_table", header_row=True):
                    dpg.add_table_column(label="ID")
                    dpg.add_table_column(label="Грузоподъемность")
                    dpg.add_table_column(label="Текущая загрузка")
                dpg.add_button(label="Добавить транспорт", callback=show_vehicle_form)
                dpg.add_button(label="Распределить грузы", callback=distribute_cargo)
                dpg.add_button(label="Показать все транспортные средства", callback=show_all_vehicles)
                dpg.add_button(label="Показать загруженные грузовики", callback=show_authorized_vehicles)
                dpg.add_button(label="Экспортировать результат", callback=export_results)

        dpg.add_text("", tag="status")


dpg.create_context()
setup_fonts()
main_window()


setup_key_handlers()

dpg.create_viewport(title="Transport company", width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()