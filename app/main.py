import tkinter as tk
from typing import List

import customtkinter as ctk

from app.db.db import session
from app.models.models import Employee
from app.utils import change_appearance_mode

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class MainApp(ctk.CTk):
    WIDTH = 1366
    HEIGHT = 768

    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        self.title("Employee days off")
        self.geometry(f"{MainApp.WIDTH}x{MainApp.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F, geometry in zip(
            (EmployeeView, VacationView), (f"{MainApp.WIDTH}x{MainApp.HEIGHT}", f"{MainApp.WIDTH}x{MainApp.HEIGHT}")
        ):
            page_name = F.__name__
            frame = F(parent=container, controller=self)

            self.frames[page_name] = (frame, geometry)

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("EmployeeView")

    def show_frame(self, page_name):
        frame, geometry = self.frames[page_name]
        self.update_idletasks()
        self.geometry(geometry)
        frame.tkraise()

    def on_closing(self):
        self.destroy()

    def refresh(self):
        self.destroy()
        self.__init__()


def button_event(controller):
    # MainApp.destroy()
    MainApp.destroy(controller)
    # MainApp()


class EmployeeView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        # ============ create two frames ============
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_menu = ctk.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="nswe")

        self.frame_right = ctk.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_menu ============
        self.frame_menu.grid_rowconfigure(0, minsize=10)
        self.frame_menu.grid_rowconfigure(5, weight=1)
        self.frame_menu.grid_rowconfigure(8, minsize=20)
        self.frame_menu.grid_rowconfigure(11, minsize=10)

        self.label_menu = ctk.CTkLabel(master=self.frame_menu, text="Menu", text_font=("Roboto Medium", -16))
        self.label_menu.grid(row=1, column=0, pady=10, padx=10)

        self.button_add_employee = ctk.CTkButton(
            master=self.frame_menu, text="Add employee", command=self.create_employee_form
        )
        self.button_add_employee.grid(row=2, column=0, pady=10, padx=20)

        self.button_add_vacation = ctk.CTkButton(master=self.frame_menu, text="Add vacation", command=button_event)
        self.button_add_vacation.grid(row=3, column=0, pady=10, padx=20)

        self.button_vacations = ctk.CTkButton(
            master=self.frame_menu, text="Vacations", command=lambda: controller.show_frame("VacationView")
        )
        self.button_vacations.grid(row=4, column=0, pady=10, padx=20)

        self.appearance_mode = ctk.CTkLabel(master=self.frame_menu, text="Appearance Mode:")
        self.appearance_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.appearance_option_mode = ctk.CTkOptionMenu(
            master=self.frame_menu, values=["Light", "Dark", "System"], command=change_appearance_mode
        )
        self.appearance_option_mode.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============
        self.frame_right.rowconfigure((0, 1, 2, 3, 4), weight=0)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1, 2, 3, 4), weight=1)

        # ============ table_headers ============
        self.label_info_ID = ctk.CTkLabel(
            master=self.frame_right, text="ID", height=50, width=10, fg_color=("white", "gray38"), justify=tk.LEFT
        )
        self.label_info_ID.grid(column=0, row=0, sticky="nwe", padx=(15, 1), pady=(15, 1))
        self.label_info_first_name = ctk.CTkLabel(
            master=self.frame_right, text="First name", height=50, fg_color=("white", "gray38"), justify=tk.LEFT
        )
        self.label_info_first_name.grid(column=1, row=0, sticky="nwe", padx=(1, 1), pady=(15, 1))
        self.label_info_last_name = ctk.CTkLabel(
            master=self.frame_right, text="Last name", height=50, fg_color=("white", "gray38"), justify=tk.LEFT
        )
        self.label_info_last_name.grid(column=2, row=0, sticky="nwe", padx=(1, 1), pady=(15, 1))
        self.label_info_free_days = ctk.CTkLabel(
            master=self.frame_right,
            text="Free days",
            height=50,
            width=25,
            fg_color=("white", "gray38"),
            justify=tk.LEFT,
        )
        self.label_info_free_days.grid(column=3, row=0, sticky="nwe", padx=(1, 1), pady=(15, 1))
        self.label_info_on_demand = ctk.CTkLabel(
            master=self.frame_right,
            text="On demand",
            height=50,
            width=25,
            fg_color=("white", "gray38"),
            justify=tk.LEFT,
        )
        self.label_info_on_demand.grid(column=4, row=0, sticky="nwe", padx=(1, 15), pady=(15, 1))

        # ============ table_values ============
        employees: List[Employee] = session.query(Employee).all()
        i: int = 0
        for employee in employees:
            self.label_info_ID = ctk.CTkLabel(
                master=self.frame_right,
                text=f"{employee.id}",
                height=50,
                width=25,
                fg_color=("white", "gray38"),
                justify=tk.LEFT,
            )
            self.label_info_ID.grid(column=0, row=1 + i, sticky="nwe", padx=(15, 1), pady=(1, 1))
            self.label_info_first_name = ctk.CTkLabel(
                master=self.frame_right,
                text=f"{employee.first_name}",
                height=50,
                fg_color=("white", "gray38"),
                justify=tk.LEFT,
            )
            self.label_info_first_name.grid(column=1, row=1 + i, sticky="nwe", padx=(1, 1), pady=(1, 1))
            self.label_info_last_name = ctk.CTkLabel(
                master=self.frame_right,
                text=f"{employee.last_name}",
                height=50,
                fg_color=("white", "gray38"),
                justify=tk.LEFT,
            )
            self.label_info_last_name.grid(column=2, row=1 + i, sticky="nwe", padx=(1, 1), pady=(1, 1))
            self.label_info_free_days = ctk.CTkLabel(
                master=self.frame_right,
                text=f"{employee.free_days}",
                height=50,
                width=25,
                fg_color=("white", "gray38"),
                justify=tk.LEFT,
            )
            self.label_info_free_days.grid(column=3, row=1 + i, sticky="nwe", padx=(1, 1), pady=(1, 1))
            self.label_info_on_demand = ctk.CTkLabel(
                master=self.frame_right,
                text=f"{employee.on_demand}",
                height=50,
                width=25,
                fg_color=("white", "gray38"),
                justify=tk.LEFT,
            )
            self.label_info_on_demand.grid(column=4, row=1 + i, sticky="nwe", padx=(1, 15), pady=(1, 1))
            i += 1

        # ============ frame_right ============
        self.entry = ctk.CTkEntry(master=self.frame_right, width=120, placeholder_text="CTkEntry")
        self.entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_5 = ctk.CTkButton(
            master=self.frame_right,
            text="CTkButton",
            border_width=2,
            fg_color=None,
            command=lambda: button_event(controller),
        )
        self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        self.appearance_option_mode.set("System")

    def create_employee_form(self):
        window = ctk.CTkToplevel(self)
        window.title("Add employee")
        window.geometry("600x400")

        window.grid_rowconfigure(0, weight=0)
        window.grid_rowconfigure(9, weight=1)
        window.grid_columnconfigure((0, 1, 2), weight=1)

        label = ctk.CTkLabel(window, text="Add new employee", justify=tk.CENTER)
        label.grid(column=1, row=0, sticky="nswe", pady=(30, 15), padx=(30, 30))

        label_first_name = ctk.CTkLabel(window, text="Enter employee first name", justify=tk.LEFT)
        label_first_name.grid(column=1, row=1, sticky="nswe", pady=(1, 1), padx=(30, 30))
        entry_first_name = ctk.CTkEntry(window, placeholder_text="First name")
        entry_first_name.grid(column=1, row=2, pady=(1, 1), padx=(30, 30))

        label_last_name = ctk.CTkLabel(window, text="Enter employee last name", justify=tk.LEFT)
        label_last_name.grid(column=1, row=3, sticky="nswe", pady=(1, 1), padx=(30, 30))
        entry_last_name = ctk.CTkEntry(window, placeholder_text="Last name")
        entry_last_name.grid(column=1, row=4, pady=(1, 1), padx=(30, 30))

        label_free_days = ctk.CTkLabel(window, text="Enter employee free days", justify=tk.LEFT)
        label_free_days.grid(column=1, row=5, sticky="nswe", pady=(1, 1), padx=(30, 30))
        entry_free_days = ctk.CTkEntry(window, placeholder_text="Free days")
        entry_free_days.grid(column=1, row=6, pady=(1, 1), padx=(30, 30))

        label_on_demand = ctk.CTkLabel(window, text="Enter employee days on demand", justify=tk.LEFT)
        label_on_demand.grid(column=1, row=7, sticky="nswe", pady=(1, 1), padx=(30, 30))
        entry_on_demand = ctk.CTkEntry(window, placeholder_text="On demand", textvariable=tk.StringVar().set("4"))
        entry_on_demand.grid(column=1, row=8, pady=(1, 15), padx=(30, 30))

        button_save = ctk.CTkButton(
            window,
            text="Save",
            command=lambda: handle_employee_form(
                entry_first_name.get(), entry_last_name.get(), entry_free_days.get(), entry_on_demand.get()
            ),
        )
        button_save.grid(column=0, row=9, pady=(1, 30), padx=(30, 0))

        button_cancel = ctk.CTkButton(window, text="Cancel", command=window.destroy)
        button_cancel.grid(column=3, row=9, pady=(1, 30), padx=(0, 30))

        def handle_employee_form(first_name: str, last_name: str, free_days: str, on_demand: str):
            employee = Employee(first_name=first_name, last_name=last_name, free_days=free_days, on_demand=on_demand)
            session.add(employee)
            session.commit()
            window.destroy()

    def refresh(self):
        MainApp.destroy()
        MainApp()


class VacationView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        # ============ create two frames ============
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_menu = ctk.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="nswe")

        self.frame_right = ctk.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_menu ============
        self.frame_menu.grid_rowconfigure(0, minsize=10)
        self.frame_menu.grid_rowconfigure(5, weight=1)
        self.frame_menu.grid_rowconfigure(8, minsize=20)
        self.frame_menu.grid_rowconfigure(11, minsize=10)

        self.label_menu = ctk.CTkLabel(master=self.frame_menu, text="Menu", text_font=("Roboto Medium", -16))
        self.label_menu.grid(row=1, column=0, pady=10, padx=10)

        self.button_add_employee = ctk.CTkButton(
            master=self.frame_menu, text="Add employee", command=self.create_employee_form
        )
        self.button_add_employee.grid(row=2, column=0, pady=10, padx=20)

        self.button_add_vacation = ctk.CTkButton(master=self.frame_menu, text="Add vacation", command=self.button_event)
        self.button_add_vacation.grid(row=3, column=0, pady=10, padx=20)

        self.button_vacations = ctk.CTkButton(
            master=self.frame_menu, text="Employees", command=lambda: controller.show_frame("EmployeeView")
        )
        self.button_vacations.grid(row=4, column=0, pady=10, padx=20)

        self.appearance_mode = ctk.CTkLabel(master=self.frame_menu, text="Appearance Mode:")
        self.appearance_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.appearance_option_mode = ctk.CTkOptionMenu(
            master=self.frame_menu, values=["Light", "Dark", "System"], command=change_appearance_mode
        )
        self.appearance_option_mode.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        self.appearance_option_mode.set("System")

    def button_event(self):
        print("Button pressed")

    def create_employee_form(self):
        window = ctk.CTkToplevel(self)
        window.title("Add employee")
        window.geometry("600x400")

        window.grid_rowconfigure(0, weight=0)
        window.grid_rowconfigure(9, weight=1)
        window.grid_columnconfigure((0, 1, 2), weight=1)

        label = ctk.CTkLabel(window, text="Add new employee", justify=tk.CENTER)
        label.grid(column=1, row=0, sticky="nswe", pady=(30, 15), padx=(30, 30))

        label_first_name = ctk.CTkLabel(window, text="Enter employee first name", justify=tk.LEFT)
        label_first_name.grid(column=1, row=1, sticky="nswe", pady=(1, 1), padx=(30, 30))
        entry_first_name = ctk.CTkEntry(window, placeholder_text="First name")
        entry_first_name.grid(column=1, row=2, pady=(1, 1), padx=(30, 30))

        label_last_name = ctk.CTkLabel(window, text="Enter employee last name", justify=tk.LEFT)
        label_last_name.grid(column=1, row=3, sticky="nswe", pady=(1, 1), padx=(30, 30))
        entry_last_name = ctk.CTkEntry(window, placeholder_text="Last name")
        entry_last_name.grid(column=1, row=4, pady=(1, 1), padx=(30, 30))

        label_free_days = ctk.CTkLabel(window, text="Enter employee free days", justify=tk.LEFT)
        label_free_days.grid(column=1, row=5, sticky="nswe", pady=(1, 1), padx=(30, 30))
        entry_free_days = ctk.CTkEntry(window, placeholder_text="Free days")
        entry_free_days.grid(column=1, row=6, pady=(1, 1), padx=(30, 30))

        label_on_demand = ctk.CTkLabel(window, text="Enter employee days on demand", justify=tk.LEFT)
        label_on_demand.grid(column=1, row=7, sticky="nswe", pady=(1, 1), padx=(30, 30))
        entry_on_demand = ctk.CTkEntry(window, placeholder_text="On demand", textvariable=tk.StringVar().set("4"))
        entry_on_demand.grid(column=1, row=8, pady=(1, 15), padx=(30, 30))

        button_save = ctk.CTkButton(
            window,
            text="Save",
            command=lambda: handle_employee_form(
                entry_first_name.get(), entry_last_name.get(), entry_free_days.get(), entry_on_demand.get()
            ),
        )
        button_save.grid(column=0, row=9, pady=(1, 30), padx=(30, 0))

        button_cancel = ctk.CTkButton(window, text="Cancel", command=window.destroy)
        button_cancel.grid(column=3, row=9, pady=(1, 30), padx=(0, 30))

        def handle_employee_form(first_name: str, last_name: str, free_days: str, on_demand: str):
            employee = Employee(first_name=first_name, last_name=last_name, free_days=free_days, on_demand=on_demand)
            session.add(employee)
            session.commit()
            window.destroy()
            self.refresh()

    def refresh(self):
        self.destroy()
        self.__init__()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
