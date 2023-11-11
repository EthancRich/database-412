import dearpygui.dearpygui as dpg

def main():
    dpg.create_context()
    create_login_window()
    dpg.create_viewport(title='Custom Title', width=600, height=400)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

### MAIN WINDOW ###
def create_main_window():
    '''Create a primary window that houses the main menu for the application.'''
    with dpg.window(label="Application", tag="main_window"):
        pass
    dpg.set_primary_window("main_window", True)

### LOGIN WINDOW ###
def create_login_window():
    '''Create a primary window that houses the login menu before using the application.'''
    with dpg.window(label="Application", tag="login_window"):
        dpg.add_input_text(label="Username", tag="username_field")
        dpg.add_input_text(label="Password", tag="password_field")
        dpg.add_button(label="Login", callback=login_button_callback)
    dpg.set_primary_window("login_window", True)

def login_button_callback():
    if dpg.get_value("username_field") == "ecrich1" and dpg.get_value("password_field") == "fish":
        print("Access Granted!")
        dpg.set_value("username_field", "")
        dpg.set_value("password_field", "")
        dpg.delete_item("login_window")
        create_main_window()
    else:
        print("Invalid login!")

### MAIN ###
if __name__ == '__main__':
    main()

