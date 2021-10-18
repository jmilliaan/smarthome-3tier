import pytest
from MySmartHomeService import MainService
from MySmartHomeService import Room


test_service = MainService()
test_room = Room()


@pytest.mark.checkuser
def test_check_user_in_db_1():
    assert test_service.check_user_in_db(username="Johan", password="10102190103") is True


@pytest.mark.checkuser
def test_check_user_in_db_2():
    assert test_service.check_user_in_db(username="Johan", password="wrongpassword") == "Wrong Password"


@pytest.mark.checkuser
def test_check_user_in_db_3():
    assert test_service.check_user_in_db(username="Joy", password="notrelevantpassword") is False


@pytest.mark.log
def test_log_():
    assert test_service.log(sensor="LDR", actuator="Lampu", details="Turning on Lamp") == \
           ("LDR", "Lampu", "Turning on Lamp")


@pytest.mark.addsensor
def test_addsensor():
    test_room.add_sensor(1, "Infrared", 2)
    test_room.add_sensor(2, "Thermometer", 2)
    assert test_room.add_sensor(3, "LDR", 2) == [(1, "Infrared", 2),
                                                 (2, "Thermometer", 2),
                                                 (3, "LDR", 2)]


@pytest.mark.addactuator
def test_addactuator():
    test_room.add_actuator(1, "AC", 3)
    test_room.add_actuator(2, "Speaker", 3)
    assert test_room.add_actuator(3, "Lampu", 3) == [(1, "AC", 3),
                                                     (2, "Speaker", 3),
                                                     (3, "Lampu", 3)]
