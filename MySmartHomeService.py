import time
import random
import configparser
import MySmartHomeDBStore

shdb = MySmartHomeDBStore.MySmartHomeDB()
config = configparser.ConfigParser()
config.read("config.ini")


class MainService:
    def __init__(self):
        self.parents = {}
        self.parent_count = 0

        self.guests = {}
        self.guest_count = 0

        self.children = {}
        self.child_count = 0

        self.admins = {}
        self.admin_count = 0
        self.admin_is_using = False

        self.active_user = ""
        self.active_user_type = ""

        self.room = ""
        self.music_player = ""

        self.automatic_mode = False
        self.guest_mode = True

        self.new_user_type = ""

    def add_parent(self, parent):
        self.parent_count += 1
        self.parents[self.parent_count] = parent
        shdb.insert_parent(username=parent.username, password=parent.password, type_id=self.parent_count)

    def add_admin(self, admin):
        self.admin_count += 1
        self.admins[self.admin_count] = admin
        shdb.insert_admin(username=admin.username, password=admin.password, type_id=self.admin_count)

    def add_guest(self, guest):
        if self.guest_mode:
            self.guest_count += 1
            self.guests[self.guest_count] = guest
            shdb.insert_guest(username=guest.username, password=guest.password, type_id=self.guest_count)
        else:
            print("Guest Mode is OFF")
            return

    def add_child(self, child):
        self.child_count += 1
        self.children[self.child_count] = child
        shdb.insert_child(username=child.username, password=child.password, type_id=self.child_count)

    def remove_parent(self, identification):
        self.parents.pop(identification - 1)

    def remove_guest(self, identification):
        self.guests.pop(identification - 1)

    def remove_admin(self, identification):
        self.admins.pop(identification - 1)

    def remove_child(self, identification):
        self.children.pop(identification - 1)

    def check_user_in_db(self, username, password):
        shdb.c("USE smarthome_db")
        shdb.c("SELECT * FROM users")
        users = shdb.printcursor()
        for i in users:
            # print(username, password, ":", i[1], i[2], i[3])
            if username == i[1]:
                if password == i[2]:
                    print(f"{username} is registered")
                    self.active_user_type = i[3]
                    return True
                else:
                    print("Wrong Password")
                    return "Wrong Password"
        print("Login Failed")
        return False

    def log(self, sensor, actuator, details):
        current_time = str(time.strftime("%H:%M:%S"))
        current_date = str(time.strftime("%d %b %Y"))
        shdb.c("USE smarthome_db")
        shdb.c(f"INSERT INTO "
               f"main_log(time, date, room, sensor, actuator, related_user, details) "
               f"VALUES('{current_time}', '{current_date}', "
               f"'{self.room}', '"
               f"{sensor}', '{actuator}', "
               f"'{self.active_user}', "
               f"'{details}')")

        shdb.commit()
        return (sensor, actuator, details)

    def monitoring(self):
        rooms = []
        for room in config["ROOMS"]:
            rooms.append(str(room))


class User:

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Parent(User):
    @staticmethod
    def allow_guest():
        global guest_mode
        guest_mode = True


class Child(User):
    pass


class Guest(User):

    def is_allowed(self):
        pass


class Admin(User):

    def change_login(self, email, username, old_password, new_password):
        pass

    def remove_device(self, device_id):
        pass


class Room:
    def __init__(self):
        self.list_of_sensors = []
        self.list_of_actuators = []
        self.room_id = None
        self.room_name = None
        self.length = None
        self.width = None
        self.height = None

    def add_sensor(self, sensor_id, sensor_type, room_id):
        self.list_of_sensors.append((sensor_id, sensor_type, room_id))
        return self.list_of_sensors

    def add_actuator(self, actuator_id, actuator_type, room_id):
        self.list_of_actuators.append((actuator_id, actuator_type, room_id))
        return self.list_of_actuators


class RuangTamu(Room):
    pass


class KamarTidur(Room):
    @staticmethod
    def get_time():
        return time.time()


class Dapur(Room):
    pass


class KamarMandi(Room):
    pass


class SensorService:
    def __init__(self):
        self.sensor_id = None
        self.sensor_type = None
        self.sensor_location = None
        self.time = None

    def get_time(self):
        self.time = time.time()


class Infrared(SensorService):
    def __init__(self):
        super().__init__()
        self.number_of_people = 0
        self.body_temperature = 35

    def capture(self):
        pass

    def find_heat_signature(self):
        config.read("config.ini")
        new_data = config["SENSORS"]["infrared"]
        self.number_of_people = new_data
        return self.number_of_people


class LDR(SensorService):
    def __init__(self):
        super().__init__()
        self.light_intensity = 0
        self.reference_light_intensity = 250

    def get_light_intensity(self):
        config.read("config.ini")
        new_data = config["SENSORS"]["ldr"]
        self.light_intensity = new_data
        return self.light_intensity


class Thermometer(SensorService):
    def __init__(self):
        super().__init__()
        self.current_temperature = None
        self.reference_temperature = 24

    def get_temperature(self):
        config.read("config.ini")
        new_data = config["SENSORS"]["thermometer"]
        self.current_temperature = new_data
        return self.current_temperature


class Actuator:
    def __init__(self):
        self.actuator_id = None
        self.actuator_type = None
        self.actuator_location = None


class AirConditioner(Actuator):
    def __init__(self):
        super().__init__()
        self.actuator_type = "Air Conditioner"
        self.temperature = 25  # 16 - 28
        self.fan = 1  # 1 - 5
        self.mode = "Cool"  # Cool, Fan, Wet
        self.swing = "1"  # 1, 2, 3
        self.conditions = f"Temperature: {self.temperature}*C, " \
                          f"Fan: {self.fan}, " \
                          f"Mode: {self.mode}, " \
                          f"Swing: {self.swing}"

    def set_temp(self, temperature):
        self.temperature = temperature

    def set_fan(self, fan):
        self.fan = fan

    def set_swing(self, mode):
        self.swing = mode

    def set_mode(self, mode):
        self.mode = mode


class Lampu(Actuator):
    def __init__(self):
        super().__init__()
        self.actuator_type = "Lampu"
        self.color = "#FFFFFF"
        self.brightness = 33  # 0 - 100
        self.conditions = f"Brightness: {self.brightness}, " \
                          f"Color: {self.color}"

    def set_color(self, color_hex):
        self.color = color_hex

    def set_brightness(self, brightness):
        self.brightness = brightness


class Speaker(Actuator):
    def __init__(self):
        super().__init__()
        self.actuator_type = "Speaker"
        self.volume = 25
        self.playlist = "Playlist1"
        self.app = "Spotify"
        self.condition = f"Playlist: {self.playlist}, " \
                         f"App: {self.app}, " \
                         f"Volume: {self.volume}"

    def choose_playlist(self, app, playlist_name):
        self.app = app
        self.playlist = playlist_name

    def set_volume(self, vol):
        self.volume = vol


ldr = LDR()
thermometer = Thermometer()
infrared = Infrared()
