import mysql.connector


class MySmartHomeDB:
    def __init__(self):
        self.mydb = mysql.connector.connect(host="127.0.0.1",
                                            user="root",
                                            password="jmilliaan03")
        self.cursor = self.mydb.cursor()

    def c(self, query):
        self.cursor.execute(query)

    def printcursor(self):
        lst = []
        for x in self.cursor.fetchall():
            lst.append(x)
        return lst

    def commit(self):
        self.mydb.commit()

    def initialize_all(self):
        self.c("CREATE DATABASE IF NOT EXISTS smarthome_db")
        self.commit()
        self.c("USE smarthome_db")
        self.c("CREATE TABLE sensors("
               "sensor_id INT PRIMARY KEY AUTO_INCREMENT, "
               "sensor_type TEXT, "
               "sensor_location TEXT)")
        self.commit()
        self.c("CREATE TABLE actuators("
               "actuator_id INT PRIMARY KEY AUTO_INCREMENT, "
               "actuator_type TEXT, "
               "actuator_location TEXT)")
        self.commit()
        self.c("CREATE TABLE users("
               "user_id INT PRIMARY KEY AUTO_INCREMENT, "
               "username TEXT, "
               "password TEXT, "
               "type TEXT, "
               "type_id INT)")
        self.commit()
        self.c("CREATE TABLE main_log("
               "event_id INT PRIMARY KEY AUTO_INCREMENT, "
               "time TEXT, "
               "date TEXT, "
               "room TEXT, "
               "sensor TEXT, "
               "actuator TEXT, "
               "related_user TEXT, "
               "details TEXT)")
        self.commit()

    def insert_guest(self, username, password, type_id):
        self.c("USE smarthome_db")
        self.c(f"INSERT INTO users(username, password, type, type_id)"
               f"VALUES('{username}', '{password}', 'guest', {type_id})")
        self.commit()

    def insert_parent(self, username, password, type_id):
        self.c("USE smarthome_db")
        self.c(f"INSERT INTO users(username, password, type, type_id)"
               f"VALUES('{username}', '{password}', 'parent', {type_id})")
        self.commit()

    def insert_admin(self, username, password, type_id):
        self.c("USE smarthome_db")
        self.c(f"INSERT INTO users(username, password, type, type_id)"
               f"VALUES('{username}', '{password}', 'admin', {type_id})")
        self.commit()

    def insert_child(self, username, password, type_id):
        self.c("USE smarthome_db")
        self.c(f"INSERT INTO users(username, password, type, type_id)"
               f"VALUES('{username}', '{password}', 'child', {type_id})")
        self.commit()

    def new_event(self, event_id, time, date, room,
                  sensor, actuator, user, details):
        self.c("USE smarthome_db")
        self.c(f"INSERT INTO main_log("
               f"event_id, time, "
               f"date, room, "
               f"sensor, actuator, "
               f"user, details)"
               f"VALUES ("
               f"'{event_id}', '{time}', "
               f"'{date}', '{room}', "
               f"'{sensor}', '{actuator}', "
               f"'{user}', '{details}')")
        self.commit()

    def insert_sensor(self, sensor_type, sensor_location):
        self.c("USE smarthome_db")
        self.c(f"INSERT INTO sensors(sensor_type, sensor_location)"
               f"VALUES('{sensor_type}', '{sensor_location}')")
        self.commit()

    def insert_actuator(self, actuator_type, actuator_location):
        self.c("USE smarthome_db")
        self.c(f"INSERT INTO actuators(actuator_type, actuator_location)"
               f"VALUES('{actuator_type}', '{actuator_location}')")
        self.commit()

    def show_tables(self):
        self.c("USE smarthome_db")
        self.c("SHOW TABLES")
        self.printcursor()

    def describe_all_tables(self):
        self.c("USE smarthome_db")
        self.c("SHOW TABLES")
        tables = self.cursor.fetchall()
        for i in tables:
            self.c(f"DESCRIBE {i[0]}")
            self.printcursor()
            print()


if __name__ == '__main__':
    # smarthome_db = MySmartHomeDB()
    # smarthome_db.initialize_all()
    pass
