import dearpygui.dearpygui as dpg
import json
from transport import Client, Vehicle, TransportCompany, Train, Airplane

# Глобальные переменные для хранения данных
company = TransportCompany("My transport company")

# Функции для обновления таблиц
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
            if isinstance(vehicle, Airplane):
                dpg.add_text(f"Высота: {vehicle.max_altitude}")
            elif isinstance(vehicle, Train):
                dpg.add_text(f"Вагоны: {vehicle.number_of_cars}")

# Вспомогательные функции для вывода транспортных средств и клиентов
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
                    dpg.add_text(client.name)
                    dpg.add_text(str(client.cargo_weight))
                    dpg.add_text("Да" if client.is_vip else "Нет")
        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item("all_clients_window"))


def show_all_vehicles():
    if dpg.does_item_exist("all_vehicles_window"):
        return
    with dpg.window(label="Все транспортные средства", modal=True, width=600, height=400, tag="all_vehicles_window"):
        with dpg.table(header_row=True):
            dpg.add_table_column(label="ID")
            dpg.add_table_column(label="Грузоподъемность")
            dpg.add_table_column(label="Текущая загрузка")
            dpg.add_table_column(label="Особенности")
            for vehicle in company.vehicles:
                with dpg.table_row():
                    dpg.add_text(str(vehicle.vehicle_id))  # ID транспортного средства
                    dpg.add_text(str(vehicle.capacity))  # Грузоподъемность
                    dpg.add_text(str(vehicle.current_load))  # Текущая загрузка
                    if isinstance(vehicle, Airplane):
                        dpg.add_text(f"Высота: {vehicle.max_altitude}")
                    elif isinstance(vehicle, Train):
                        dpg.add_text(f"Вагоны: {vehicle.number_of_cars}")
        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item("all_vehicles_window"))



def show_vip_clients():
    if dpg.does_item_exist("vip_clients_window"):
        return
    with dpg.window(label="VIP клиенты", modal=True, width=600, height=400, tag="vip_clients_window"):
        with dpg.table(header_row=True):
            dpg.add_table_column(label="Имя клиента")
            dpg.add_table_column(label="Вес груза")
            for client in filter(lambda c: c.is_vip, company.clients):
                with dpg.table_row():
                    dpg.add_text(client.name)
                    dpg.add_text(str(client.cargo_weight))
        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item("vip_clients_window"))

def show_loaded_vehicles():
    # Проверка, существует ли уже окно с загруженными транспортными средствами
    if dpg.does_item_exist("loaded_vehicles_window"):
        print("Окно с загруженными транспортными средствами уже существует.")
        return

    # Проверка, есть ли транспортные средства с загрузкой больше нуля
    loaded_vehicles = list(filter(lambda v: v.current_load > 0, company.vehicles))
    if not loaded_vehicles:
        print("Нет загруженных транспортных средств.")
        return

    with dpg.window(label="Загруженные транспортные средства", modal=True, width=600, height=400, tag="loaded_vehicles_window"):
        with dpg.table(header_row=True):
            dpg.add_table_column(label="ID")
            dpg.add_table_column(label="Грузоподъемность")
            dpg.add_table_column(label="Текущая загрузка")
            dpg.add_table_column(label="Особенности")

            # Добавляем загруженные транспортные средства в таблицу
            for vehicle in loaded_vehicles:
                with dpg.table_row():
                    dpg.add_text(str(vehicle.vehicle_id))  # ID транспортного средства
                    dpg.add_text(str(vehicle.capacity))  # Грузоподъемность
                    dpg.add_text(str(vehicle.current_load))  # Текущая загрузка

                    # Проверка типа транспортного средства
                    if isinstance(vehicle, Airplane):
                        dpg.add_text(f"Высота: {vehicle.max_altitude}")  # Высота для самолета
                    elif isinstance(vehicle, Train):
                        dpg.add_text(f"Вагоны: {vehicle.number_of_cars}")  # Холодильник для фургона

        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item("loaded_vehicles_window"))

    print("Окно с загруженными транспортными средствами создано.")



def show_client_form():
    if dpg.does_item_exist("client_form"):
        return
    with dpg.window(label="Добавить клиента", width=400, height=300, modal=True, tag="client_form"):
        dpg.add_text("Имя клиента:")
        dpg.add_input_text(tag="client_name", width=250)
        dpg.add_text("Вес груза:")
        dpg.add_input_text(tag="client_cargo_weight", width=250)
        dpg.add_text("VIP статус:")
        dpg.add_checkbox(tag="client_is_vip")
        dpg.add_button(label="Сохранить", callback=save_client)
        dpg.add_button(label="Отмена", callback=lambda: dpg.delete_item("client_form"))

def save_client():
    name = dpg.get_value("client_name")
    cargo_weight = dpg.get_value("client_cargo_weight")
    is_vip = dpg.get_value("client_is_vip")

    if name and cargo_weight.isdigit() and int(cargo_weight) > 0:
        client = Client(name, int(cargo_weight), is_vip)
        company.add_client(client)
        update_clients_table()
        dpg.delete_item("client_form")
    else:
        dpg.set_value("status", "Ошибка: Проверьте введённые данные!")

def show_vehicle_form():
    if dpg.does_item_exist("vehicle_form"):
        return
    with dpg.window(label="Добавить транспорт", width=400, height=300, modal=True, tag="vehicle_form"):
        dpg.add_text("Тип транспорта:")
        dpg.add_combo(["Самолет", "Поезд"], tag="vehicle_type", width=250, callback=toggle_vehicle_specific_fields)
        dpg.add_text("Грузоподъемность (тонны):")
        dpg.add_input_text(tag="vehicle_capacity", width=250)

        dpg.add_text("Введите высоту полёта:", tag="max_altitude_label", show=False)
        dpg.add_input_text(tag="max_altitude", width=250, show=False)

        dpg.add_text("Введите кол-во вагонов: ", tag="number_of_cars_label", show=False)
        dpg.add_input_text(tag="number_of_cars", show=False)

        dpg.add_button(label="Сохранить", callback=save_vehicle)
        dpg.add_button(label="Отмена", callback=lambda: dpg.delete_item("vehicle_form"))

def toggle_vehicle_specific_fields(sender, app_data):
    if app_data == "Самолет":
        dpg.configure_item("max_altitude_label", show=True)
        dpg.configure_item("max_altitude", show=True)
        dpg.configure_item("number_of_cars_label", show=False)
        dpg.configure_item("number_of_cars", show=False)
    elif app_data == "Поезд":
        dpg.configure_item("max_altitude_label", show=False)
        dpg.configure_item("max_altitude", show=False)
        dpg.configure_item("number_of_cars_label", show=True)
        dpg.configure_item("number_of_cars", show=True)

def save_vehicle():
    vehicle_type = dpg.get_value("vehicle_type")
    capacity = dpg.get_value("vehicle_capacity")

    if capacity.isdigit() and int(capacity) > 0:
        capacity = int(capacity)
        if vehicle_type == "Самолет":
            max_altitude = dpg.get_value("max_altitude")
            if max_altitude.isdigit() and int(max_altitude) > 0:
                vehicle = Airplane(capacity, int(max_altitude))  # Передаем высоту полёта
            else:
                dpg.set_value("status", "Ошибка: Проверьте высоту полёта!")
                return
        elif vehicle_type == "Поезд":
            number_of_cars = dpg.get_value("number_of_cars")
            if number_of_cars.isdigit() and int(number_of_cars) > 0:
                vehicle = Train(capacity, int(number_of_cars))
            else:
                dpg.set_value("status", "Ошибка: Проверьте высоту полёта!")
                return
        else:
            vehicle = Vehicle(capacity)  # Грузовик по умолчанию

        company.add_vehicle(vehicle)  # Добавление транспортного средства
        update_vehicles_table()  # Обновление таблицы транспортных средств
        dpg.delete_item("vehicle_form")  # Закрытие формы
    else:
        dpg.set_value("status", "Ошибка: Проверьте введённые данные!")


def show_authorized_clients():
    
    # Проверка существования окна
    if dpg.does_item_exist("clients_window"):
        return

    # Создаем окно с VIP клиентами
    with dpg.window(label="VIP клиенты", modal=True, width=600, height=400, tag="clients_window"):
        # Добавляем таблицу с данными
        with dpg.table(header_row=True):
            dpg.add_table_column(label="Имя клиента")
            dpg.add_table_column(label="Вес груза")
            dpg.add_table_column(label="VIP статус")

            for client in filter(lambda c: c.is_vip, company.clients):
                with dpg.table_row():
                    dpg.add_text(client.name)
                    dpg.add_text(str(client.cargo_weight))
                    dpg.add_text("Да")

        # Кнопка для закрытия окна
        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item("clients_window"))


def export_results():
    data = {
        "clients": [{"name": c.name, "cargo_weight": c.cargo_weight, "is_vip": c.is_vip} for c in company.clients],
        "vehicles": [
            {
                "vehicle_id": v.vehicle_id,
                "capacity": v.capacity,
                "current_load": v.current_load,
                "type": "Airplane" if isinstance(v, Airplane) else "Train" if isinstance(v, Train) else "Truck",
                "details": {
                    "max_altitude": getattr(v, 'max_altitude', None),
                    "number_of_cars": getattr(v, 'number_of_cars', None)
                }
            } for v in company.vehicles
        ]
    }
    with open("export.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    dpg.set_value("status", "Результаты экспортированы в файл export.json.")

def distribute_cargo():
    company.optimize_cargo_distribution()
    update_vehicles_table()
    dpg.set_value("status", "Грузы успешно распределены!")



def distribute_cargo_results():
    # Проверяем, существует ли уже окно с результатами распределения
    if dpg.does_item_exist("cargo_distribution_window"):
        return

    # Создаем окно для отображения результатов
    with dpg.window(label="Распределение груза", modal=True, width=600, height=400, tag="cargo_distribution_window"):
        # Создаем таблицу для отображения результатов
        with dpg.table(header_row=True):
            dpg.add_table_column(label="Транспортное средство")
            dpg.add_table_column(label="Грузоподъемность")
            dpg.add_table_column(label="Текущий груз")
            dpg.add_table_column(label="Распределенный груз")

            # Пример распределения груза: для каждого транспортного средства
            for vehicle in company.vehicles:
                # Пример распределения груза
                distributed_cargo = vehicle.current_load  # Здесь вы можете взять данные из своей логики распределения
                with dpg.table_row():
                    dpg.add_text(vehicle.vehicle_id)  # Идентификатор транспортного средства
                    dpg.add_text(str(vehicle.capacity))  # Грузоподъемность
                    dpg.add_text(str(vehicle.current_load))  # Текущий груз
                    dpg.add_text(str(distributed_cargo))  # Распределенный груз

        # Кнопка для закрытия окна
        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item("cargo_distribution_window"))


def show_about():
    if dpg.does_item_exist("about_window"):
        return

    with dpg.window(label="О программе", width=300, height=200, modal=True, tag="about_window"):
       
        dpg.add_text("Лабораторная работа номер 12")
        dpg.add_text("Вариант: 5")
        dpg.add_text("Разработчик: Шубников Святослав Эрнестович")
        dpg.add_text("Группа 81 ТП")
        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item("about_window"))

def setup_fonts():
    with dpg.font_registry():
        with dpg.font("C:/Windows/Fonts/Arial.ttf", 20) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
            dpg.bind_font(default_font)

def distribute_cargo():
    company.optimize_cargo_distribution()  # Вызываем метод для распределения грузов
    update_vehicles_table()  # Обновляем таблицу с транспортными средствами
    dpg.set_value("status", "Грузы успешно распределены!")


def setup_global_key_handlers():
    """
    Настройка глобальных обработчиков клавиш для всех окон.
    """
    def handle_escape():
        # Закрытие всех открытых окон
        open_windows = [
            "client_form",
            "vehicle_form",
            "clients_window",
            "all_vehicles_window",
            "about_window",
            "all_clients_window",
            "cargo_distribution_window",
            "cargo_distribution_window",
        ]
        for window in open_windows:
            if dpg.does_item_exist(window):
                dpg.delete_item(window)

    def handle_enter():
        # Сохранение данных в активной форме
        if dpg.does_item_exist("client_form"):
            save_client()
        elif dpg.does_item_exist("vehicle_form"):
            save_vehicle()

    # Глобальная регистрация обработчиков
    with dpg.handler_registry():
        # Escape: закрыть окна
        dpg.add_key_down_handler(key=dpg.mvKey_Escape, callback=lambda: handle_escape())
        # Enter: сохранить данные
        dpg.add_key_down_handler(key=dpg.mvKey_Return, callback=lambda: handle_enter())


def main_window():
    with dpg.window(label="Основное окно", width=800, height=600):
        dpg.add_button(label="О программе", callback=show_about)

        with dpg.group(horizontal=True):
            # Клиенты
            with dpg.group():
                dpg.add_text("Клиенты", tag="clients_text")
                with dpg.table(tag="clients_table", header_row=True):
                    dpg
                dpg.add_button(label="Добавить клиента", callback=show_client_form)
                dpg.add_button(label="Показать всех клиентов", callback=show_all_clients)
                dpg.add_button(label="Показать VIP клиентов", callback=show_authorized_clients)

            # Транспортные средства
            with dpg.group():
                dpg.add_text("Транспортные средства", tag="vehicles_text")
                with dpg.table(tag="vehicles_table", header_row=True):
                    dpg
                dpg.add_button(label="Добавить транспорт", callback=show_vehicle_form)
                dpg.add_button(label="Распределить грузы", callback=distribute_cargo)
                dpg.add_button(label="Показать все транспортные средства", callback=show_all_vehicles)
                dpg.add_button(label="Показать результат распределения", callback=distribute_cargo_results)
                dpg.add_button(label="Экспортировать результат", callback=export_results)

        dpg.add_text("", tag="status")

# Запуск приложения
dpg.create_context()
setup_fonts()
main_window()

# Настройка обработчиков клавиш
setup_global_key_handlers()

dpg.create_viewport(title="Transport company", width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()