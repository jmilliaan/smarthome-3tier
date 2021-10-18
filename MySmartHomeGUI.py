import time
from tkinter import *
import MySmartHomeService as ShService
from threading import Thread

root = Tk()
root.title("Mockup IEE2031 Joy & Victo")

try:  # Logo CIT untuk icon window
    logo_cit = PhotoImage(file="logoCIT_kecil.png")
    root.iconphoto(False, logo_cit)
except TclError:
    print("logoCIT_kecil.png is not found")

root.geometry("450x650")

toggle_count_auto_mode = 0
toggle_count_lampu = 0
toggle_count_guest = 0
toggle_count_AC = 0

service = ShService.MainService()
infrared = ShService.infrared
ldr = ShService.ldr
thermometer = ShService.thermometer


def retrieve_mode():
    mode = var_auto.get()
    if mode == 1:
        return "automatic"
    elif mode == 2:
        return "manual"


def disable_all():
    ruangan_menu.configure(state="disabled")
    temperatur_spinbox.configure(state="disabled")
    kipas_spinbox.configure(state="disabled")
    onoff_lampu.configure(state="disabled")
    onoff_AC.configure(state="disabled")
    playlist_entry.configure(state="disabled")
    music_player_menu.configure(state="disabled")
    playbutton.configure(state="disabled")
    service.log(sensor="NULL",
                actuator="NULL",
                details="Disabled All Features")


def enable_all():
    ruangan_menu.configure(state="normal")
    temperatur_spinbox.configure(state="normal")
    kipas_spinbox.configure(state="normal")
    onoff_lampu.configure(state="normal")
    onoff_AC.configure(state="normal")
    playlist_entry.configure(state="normal")
    music_player_menu.configure(state="normal")
    playbutton.configure(state="normal")
    service.log(sensor="NULL",
                actuator="NULL",
                details="Enabled All Features")


def login_success():
    username = username_entry.get()
    password = password_entry.get()
    print(f"Login Attempt\nUsername: {username}\nPassword:{password}")
    if service.check_user_in_db(username, password):
        user_type = service.active_user_type
        login_success_text.config(text=f"Login Successfull as {user_type}")
        service.active_user = username
        enable_all()
        logout.config(state="normal")
        service.log(sensor="NULL",
                    actuator="NULL",
                    details="User Logged In")
        if str(user_type).lower() == "admin":
            user_is_admin()
        if str(user_type).lower() == "parent":
            guest_button.config(state="normal")
    else:
        login_success_text.config(text="Login Failed")
        service.log(sensor="NULL",
                    actuator="NULL",
                    details=f"User Failed to Log In. username: {username}, password: {password}")


def user_is_admin():
    disable_all()
    admin_area.config(state="normal")
    admin_add_username_entry.config(state="normal")
    admin_add_password_entry.config(state="normal")
    admin_new_user_type.config(state="normal")
    admin_add_type_choose.config(state="normal")
    admin_add_user_button.config(state="normal")


def disable_admin_control():
    admin_area.config(state="disabled")
    admin_add_username_entry.config(state="disabled")
    admin_add_password_entry.config(state="disabled")
    admin_new_user_type.config(state="disabled")
    admin_add_type_choose.config(state="disabled")
    admin_add_user_button.config(state="disabled")


def show_new_user_type(type):
    print(type)
    service.new_user_type = str(type).lower()


def admin_add_user():
    new_user_type = service.new_user_type
    new_username = admin_add_username_entry.get()
    new_password = admin_add_password_entry.get()
    print(new_user_type)
    if new_user_type == "parent":
        parent_to_add = ShService.Parent(username=new_username, password=new_password)
        service.add_parent(parent_to_add)
    elif new_user_type == "child":
        child_to_add = ShService.Child(username=new_username, password=new_password)
        service.add_child(child_to_add)
    elif new_user_type == "admin":
        admin_to_add = ShService.Admin(username=new_username, password=new_password)
        service.add_child(admin_to_add)
    else:
        guest_to_add = ShService.Guest(username=new_username, password=new_password)
        service.add_child(guest_to_add)
    service.log(sensor="NULL", actuator="NULL", details=f"Admin added new user: {new_username}")


def is_clicked_lampu():
    global toggle_count_lampu
    toggle_count_lampu += 1
    if toggle_count_lampu % 2 == 0:
        toggle_text_lampu.set("OFF")
        print("Lampu OFF")
        service.log(sensor="NULL",
                    actuator="Lampu",
                    details="Manual - OFF")
    else:
        toggle_text_lampu.set("ON")
        print("Lampu ON")
        service.log(sensor="NULL",
                    actuator="Lampu",
                    details="Manual - ON")


def is_clicked_guest():
    global toggle_count_guest
    toggle_count_guest += 1
    if toggle_count_guest % 2 == 0:
        service.guest_mode = False
        guest_text.set("OFF")
        print("Guest Mode OFF")
        service.log(sensor="NULL",
                    actuator="NULL",
                    details="Disabled Guest Mode")
    else:
        service.guest_mode = True
        guest_text.set("ON")
        print("Guest Mode ON")
        service.log(sensor="NULL",
                    actuator="NULL",
                    details="Enabled Guest Mode")


def is_clicked_ac():
    global toggle_count_AC
    toggle_count_AC += 1
    if toggle_count_AC % 2 == 0:
        toggle_air_con.set("OFF")
        print("AC OFF")
        service.log(sensor="NULL",
                    actuator="AC",
                    details="Turned OFF AC")
    else:
        toggle_air_con.set("ON")
        print("AC ON")
        service.log(sensor="NULL",
                    actuator="AC",
                    details="Turned ON AC")


def auto_mode():
    auto_thread = Thread(target=automatic_mode_process, name="auto thread", args=())
    manual_thread = Thread(target=switch_to_manual, name="manual thread", args=())
    if var_auto.get() == "ON":
        service.automatic_mode = True
        disable_all()
        service.log(sensor="NULL",
                    actuator="NULL",
                    details="Enabled Automatic Mode")

        auto_thread.start()
        # automatic_mode_process()
    elif var_auto.get() == "OFF":
        service.automatic_mode = False
        enable_all()
        service.log(sensor="NULL",
                    actuator="NULL",
                    details="Disabled Automatic Mode, Enabled Manual Mode")
        manual_thread.start()


def switch_to_manual(*args):
    service.automatic_mode = False


def automatic_mode_process(*args):
    rooms = []
    current_time = int(time.strftime("%H"))
    for room in ShService.config["ROOMS"]:
        rooms.append(str(room))
    while service.automatic_mode:
        print(service.automatic_mode)
        for each_room in rooms:
            light = float(ldr.get_light_intensity())
            people = float(infrared.find_heat_signature())
            temp = float(thermometer.get_temperature())
            service.room = str(ShService.config["ROOMS"][each_room])

            if current_time > 8 and current_time < 11:
                print(f"{time.strftime('%H:%M:%S')}: Turning on Speaker at all rooms")
                service.log(sensor="Clock", actuator="Speaker", details=f"ON")
            else:
                print(f"{time.strftime('%H:%M:%S')}: Turning off Speaker at all rooms")
                service.log(sensor="Clock", actuator="Speaker", details=f"OFF")

            if (22 < current_time < 24 or 0 < current_time < 6) and service.room == "Kamar Tidur":
                print(f"{time.strftime('%H:%M:%S')}: Turning off Bedroom Lamp")
                service.log(sensor="Clock", actuator="Lampu", details=f"OFF")
                print(f"{time.strftime('%H:%M:%S')}: Turning off Bedroom Speaker")
                service.log(sensor="Clock", actuator="Speaker", details=f"OFF")

            if light < ldr.reference_light_intensity and people >= 1:
                print(f"{time.strftime('%H:%M:%S')}: Turning on Lamp at {each_room}")
                service.log(sensor="LDR", actuator="Lampu", details=f"ON")
            else:
                print(f"{time.strftime('%H:%M:%S')}: Turning off Lamp at {each_room}")
                service.log(sensor="LDR", actuator="Lampu", details=f"OFF")

            if people >= 1:
                print(f"{time.strftime('%H:%M:%S')}: Turning on Speaker at {each_room}")
                service.log(sensor="Infrared", actuator="Speaker", details=f"ON")
            else:
                print(f"{time.strftime('%H:%M:%S')}: Turning off Speaker at {each_room}")
                service.log(sensor="Infrared", actuator="Speaker", details=f"OFF")

            if temp > thermometer.reference_temperature:
                print(f"{time.strftime('%H:%M:%S')}: Turning on AC at {each_room}")
                service.log(sensor="Thermometer", actuator="AC", details=f"ON")
            else:
                print(f"{time.strftime('%H:%M:%S')}: Turning off AC at {each_room}")
                service.log(sensor="Thermometer", actuator="AC", details=f"OFF")
            time.sleep(1)
        time.sleep(1)
        root.update()


def play_music():
    music_text.config(text=f"Playing Music")
    musik = playlist_entry.get()
    print("musik: {} ".format(musik))
    service.log(sensor="NULL",
                actuator="Speaker",
                details="Playing Music")
    return musik


def print_value(val):
    print(val)


def disable_bathroom():
    onoff_AC.config(state="disabled")
    temperatur_spinbox.config(state="disabled")
    kipas_spinbox.config(state="disabled")


def enable_bathroom():
    onoff_AC.config(state="normal")
    temperatur_spinbox.config(state="normal")
    kipas_spinbox.config(state="normal")


def choose_room(selection):
    service.room = selection
    service.log(sensor="NULL",
                actuator="NULL",
                details=f"Chose Room {service.room}")
    if str(service.room) == "Kamar Mandi":
        disable_bathroom()
    else:
        enable_bathroom()
    print(service.room)


def choose_player(selection):
    service.music_player = selection
    service.log(sensor="NULL",
                actuator="Speaker",
                details=f"Chose Player {service.music_player}")
    print(service.music_player)


def log_out():
    service.log(sensor="NULL", actuator="NULL", details="User Logged Out")
    disable_all()
    disable_admin_control()


if __name__ == '__main__':
    username_label = Label(root, text="Username ", font=("Gotham Rounded Book", 9))
    username_entry = Entry(root, width=30)
    username_entry.insert(0, "Username")

    password_label = Label(root, text="Password ", font=("Gotham Rounded Book", 9))
    password_entry = Entry(root, width=30, show="*")
    password_entry.insert(0, "Password")

    login = Label(root, text="Login Info", font=("Gotham Rounded Bold", 14))
    login_success_text = Label(root, text="")
    login_button = Button(root, text="Login", command=login_success)

    admin_area = Label(root, text="Admin Area", font=("Gotham Rounded Book", 9), state="disabled")
    admin_add_username_entry = Entry(root, state="disabled")
    admin_add_username_entry.insert(0, "New Username")
    admin_add_password_entry = Entry(root, state="disabled")
    admin_add_password_entry.insert(0, "New Password")
    admin_new_user_type = Label(root, text="User Type", state="disabled")
    add_user_type = StringVar(root)
    add_user_type.set("Parent")
    admin_add_type_choose = OptionMenu(root, add_user_type, "Parent", "Child", "Guest", "Admin",
                                       command=show_new_user_type)
    admin_add_type_choose.config(state="disabled")
    admin_add_user_button = Button(root, text="Add User", command=admin_add_user, state="disabled")

    automatic_mode = Label(root, text="Automatic Mode", font=("Gotham Rounded Book", 10))
    var_auto = StringVar(value=1)
    auto_on = Radiobutton(root, text="Automatic", variable=var_auto, value="ON", command=auto_mode)
    auto_off = Radiobutton(root, text="Manual", variable=var_auto, value="OFF", command=auto_mode)

    guest_label = Label(root, text="Guest Mode", font=("Gotham Rounded Book", 10))
    guest_text = StringVar()
    guest_button = Button(root, textvariable=guest_text, command=is_clicked_guest)
    guest_button.config(state="disabled")
    guest_text.set("OFF")

    pilih_ruangan = Label(root, text="Pilih Ruangan", font=("Gotham Rounded Bold", 11))
    default_room = StringVar(root)
    default_room.set("Ruang Tamu")
    ruangan_menu = OptionMenu(root, default_room, "Ruang Tamu", "Kamar Tidur", "Dapur", "Kamar Mandi",
                              command=choose_room)

    air_con = Label(root, text="Air Conditioner", font=("Gotham Rounded Bold", 10))
    toggle_air_con = StringVar()
    onoff_AC = Button(root, textvariable=toggle_air_con, command=is_clicked_ac, bg="#DEDEDE")
    toggle_air_con.set("OFF")
    temperatur = Label(root, text="Temperatur")
    temperatur_spinbox = Spinbox(root, from_=16, to=30, wrap=True,
                                 command=lambda: print("temp", temperatur_spinbox.get()))
    kipas = Label(root, text="Kipas")
    kipas_spinbox = Scale(root, from_=1, to=5, orient='horizontal', command=print_value)

    lampu = Label(root, text="Lampu", font=("Gotham Rounded Bold", 10))
    toggle_text_lampu = StringVar()
    onoff_lampu = Button(root, textvariable=toggle_text_lampu, command=is_clicked_lampu, bg="#DEDEDE")
    toggle_text_lampu.set("OFF")

    speaker = Label(root, text="Speaker", font=("Gotham Rounded Bold", 10))
    playlist_entry = Entry(root, width=30)
    default_player = StringVar(root)
    default_player.set("Spotify")
    music_player_menu = OptionMenu(root, default_player, "Spotify", "iTunes", "YouTube", "Joox", command=choose_player)
    music_text = Label(root, text="")
    playbutton = Button(root, text="Play", command=play_music)

    logout = Button(root, text="LOG OUT", command=log_out)
    logout.config(state="disabled")

    kelompok = Label(root, text="Kelompok 1 IEE2031:\n"
                                "Joy Milliaan/10102190103\n"
                                "Victoriano Aribaldi/10102190236", justify="left")

    #### Loading GUI
    login.grid(column=0, row=0, sticky="w")
    username_label.grid(column=0, row=1, sticky="w")
    username_entry.grid(column=1, row=1, sticky="w", columnspan=2, padx=10)
    password_label.grid(column=0, row=2, sticky="w")
    password_entry.grid(column=1, row=2, sticky="w", columnspan=2, padx=10)

    admin_area.grid(column=1, row=4, sticky="w", padx=10, pady=10)
    admin_add_username_entry.grid(column=1, row=5, sticky="w", columnspan=2, padx=10)
    admin_add_password_entry.grid(column=1, row=6, sticky="w", columnspan=2, padx=10)
    admin_new_user_type.grid(column=1, row=7, sticky="w", padx=10)
    admin_add_type_choose.grid(column=2, row=7, sticky="w", padx=10)
    admin_add_user_button.grid(column=1, row=8, sticky="w", padx=10)

    login_button.grid(column=0, row=3, sticky="e")
    login_success_text.grid(column=1, row=3, sticky="w", padx=10)

    guest_label.grid(column=0, row=4, sticky="w")
    guest_button.grid(column=0, row=4, sticky="e")

    automatic_mode.grid(column=0, row=6, sticky="w")
    auto_on.grid(column=0, row=7, sticky="w")
    auto_off.grid(column=0, row=8, sticky="w")

    pilih_ruangan.grid(column=0, row=9, sticky="w")
    ruangan_menu.grid(column=0, row=10, sticky="w")

    air_con.grid(column=0, row=11, sticky="w")
    onoff_AC.grid(column=0, row=11, sticky="e")
    temperatur.grid(column=0, row=12, sticky="w")
    temperatur_spinbox.grid(column=0, row=13, sticky="w")
    kipas.grid(column=0, row=14, sticky="w")
    kipas_spinbox.grid(column=0, row=15, sticky="w")
    lampu.grid(column=0, row=16, sticky="w")
    onoff_lampu.grid(column=0, row=16, sticky="e")

    speaker.grid(column=0, row=17, sticky="w")
    music_player_menu.grid(column=0, row=18, sticky="w")
    playlist_entry.grid(column=0, row=19, sticky="w")
    music_text.grid(column=0, row=20, sticky="w")
    playbutton.grid(column=0, row=21, sticky="e")
    logout.grid(column=0, row=22, sticky="w", columnspan=2)

    kelompok.grid(column=0, row=23, sticky="w")
    disable_all()

    root.mainloop()
