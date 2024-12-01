import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import Error
from tkinter import simpledialog



class ClinicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Поликлиника")
        self.connection = self.connect_db()
        self.user_role = None
        self.create_user_selection()
        self.additional_fields_frame = None

    def connect_db(self):
        try:
            connection = psycopg2.connect(
                user="postgres",
                password="1210",
                host="127.0.0.1",
                port="5432",
                database="postgres_db"
            )
            return connection
        except Error as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения к базе данных: {e}")
            return None

    def execute_query(self, query, values=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            self.connection.commit()
            return None
        except Error as e:
            messagebox.showerror("Ошибка", f"Ошибка выполнения запроса: {e}")
        finally:
            cursor.close()

    def create_user_selection(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack()

        tk.Label(frame, text="Выберите роль пользователя", font=("Arial", 14)).pack(pady=10)

        tk.Button(
            frame, text="Работник регистратуры", width=20, command=lambda: self.set_role("registrar")
        ).pack(pady=5)

        tk.Button(
            frame, text="Администратор", width=20, command=lambda: self.set_role("admin")
        ).pack(pady=5)

    def set_role(self, role):
        self.user_role = role
        self.create_gui()

    def create_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        user_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Пользователь", menu=user_menu)
        user_menu.add_command(label="Выход", command=self.create_user_selection)

        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack()

        title = "Регистратура поликлиники" if self.user_role == "registrar" else "Администрирование поликлиники"
        tk.Label(frame, text=title, font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Выберите действие:", font=("Arial", 12)).grid(row=1, column=0, pady=10, sticky="w")
        self.action_combo = ttk.Combobox(frame, state="readonly", width=50)
        self.action_combo.grid(row=2, column=0, columnspan=2, pady=5)

        if self.user_role == "registrar":
            self.action_combo["values"] = [
                "Показать адрес, дату заболевания, диагноз больного",
                "Показать ФИО лечащего врача больного",
                "Показать кабинет и расписание врача",
                "Показать всех больных врача",
                "Показать симптомы болезни и рекомендованное лекарство",
                "Выдать справку о болезни"
            ]
        elif self.user_role == "admin":
            self.action_combo["values"] = [
                "Добавить нового больного",
                "Удалить больного",
                "Уволить врача",
                "Изменить диагноз",
                "Добавить нового врача",
                "Отчет о работе поликлиники"
            ]
        self.action_combo.current(0)
        self.action_combo.bind("<<ComboboxSelected>>", self.display_action_fields)

        tk.Button(frame, text="Выполнить", command=self.perform_action).grid(row=4, column=0, columnspan=2, pady=10)

        self.result_text = tk.Text(frame, height=15, width=70)
        self.result_text.grid(row=5, column=0, columnspan=2, pady=10)

        self.additional_fields_frame = tk.Frame(frame)
        self.additional_fields_frame.grid(row=3, column=0, columnspan=2, pady=10)

    def display_action_fields(self, event=None):
        action = self.action_combo.get()
        for widget in self.additional_fields_frame.winfo_children():
            widget.destroy()

        if action == "Добавить нового больного":
            self.create_add_patient_fields()
        elif action == "Удалить больного":
            self.create_delete_patient_fields()
        elif action == "Добавить нового врача":
            self.create_add_doctor_fields()
        elif action == "Уволить врача":
            self.create_remove_doctor_fields()
        elif action == "Показать адрес, дату заболевания, диагноз больного":
            self.create_patient_search_field()
        elif action == "Показать кабинет и расписание врача":
            self.create_doctor_search_field()
        elif action == "Изменить диагноз":
            self.create_diagnosis_update_fields()

    def create_add_patient_fields(self):
        tk.Label(self.additional_fields_frame, text="ФИО:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.full_name_entry = tk.Entry(self.additional_fields_frame, width=40)
        self.full_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.additional_fields_frame, text="Адрес:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.address_entry = tk.Entry(self.additional_fields_frame, width=40)
        self.address_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.additional_fields_frame, text="Диагноз:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.diagnosis_entry = tk.Entry(self.additional_fields_frame, width=40)
        self.diagnosis_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.additional_fields_frame, text="Дата заболевания (YYYY-MM-DD):").grid(
            row=3, column=0, padx=5, pady=5, sticky="e"
        )
        self.disease_date_entry = tk.Entry(self.additional_fields_frame, width=40)
        self.disease_date_entry.grid(row=3, column=1, padx=5, pady=5)

    def create_add_doctor_fields(self):
        tk.Label(self.additional_fields_frame, text="ФИО:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.doctor_name_entry = tk.Entry(self.additional_fields_frame, width=40)
        self.doctor_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.additional_fields_frame, text="Номер кабинета:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.room_number_entry = tk.Entry(self.additional_fields_frame, width=40)
        self.room_number_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.additional_fields_frame, text="Номер участка:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.section_number_entry = tk.Entry(self.additional_fields_frame, width=40)
        self.section_number_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.additional_fields_frame, text="Расписание приема:").grid(row=3, column=0, padx=5, pady=5,
                                                                               sticky="w")

        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        self.schedule_days = {}
        for i, day in enumerate(days):
            var = tk.BooleanVar()
            entry = tk.Entry(self.additional_fields_frame, width=20)
            tk.Checkbutton(self.additional_fields_frame, text=day, variable=var).grid(row=4 + i, column=0, sticky="w")
            entry.grid(row=4 + i, column=1, padx=5, pady=2)
            self.schedule_days[day] = (var, entry)

    def create_remove_doctor_fields(self):
        tk.Label(self.additional_fields_frame, text="ФИО врача для удаления:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.remove_doctor_entry = tk.Entry(self.additional_fields_frame, width=40)
        self.remove_doctor_entry.grid(row=0, column=1, padx=5, pady=5)

    def create_delete_patient_fields(self):
        tk.Label(self.additional_fields_frame, text="Введите ФИО больного:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.patient_name_entry = tk.Entry(self.additional_fields_frame, width=40)
        self.patient_name_entry.grid(row=0, column=1, padx=5, pady=5)

    def create_patient_search_field(self):
        tk.Label(self.additional_fields_frame, text="Введите ФИО больного:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.patient_name_entry = tk.Entry(self.additional_fields_frame, width=40)
        self.patient_name_entry.grid(row=0, column=1, padx=5, pady=5)

    def create_doctor_search_field(self):
        tk.Label(self.additional_fields_frame, text="Введите ФИО врача:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.doctor_name_entry = tk.Entry(self.additional_fields_frame, width=40)
        self.doctor_name_entry.grid(row=0, column=1, padx=5, pady=5)

    def create_diagnosis_update_fields(self):
        tk.Label(self.additional_fields_frame, text="Введите ФИО больного:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.patient_name_entry = tk.Entry(self.additional_fields_frame, width=40)
        self.patient_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.additional_fields_frame, text="Введите новый диагноз:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.new_diagnosis_entry = tk.Entry(self.additional_fields_frame, width=40)
        self.new_diagnosis_entry.grid(row=1, column=1, padx=5, pady=5)

    def perform_action(self):
        action = self.action_combo.get()
        self.result_text.delete("1.0", tk.END)

        if action == "Добавить нового больного":
            self.add_new_patient()
        elif action == "Удалить больного":
            self.delete_patient()
        elif action == "Добавить нового врача":
            self.add_new_doctor()
        elif action == "Уволить врача":
            self.remove_doctor()
        elif action == "Показать адрес, дату заболевания, диагноз больного":
            self.show_patient_details()
        elif action == "Показать кабинет и расписание врача":
            self.show_doctor_schedule()
        elif action == "Изменить диагноз":
            self.update_patient_diagnosis()

    def add_new_patient(self):
        full_name = self.full_name_entry.get().strip()
        address = self.address_entry.get().strip()
        diagnosis = self.diagnosis_entry.get().strip()
        disease_date = self.disease_date_entry.get().strip()

        if not (full_name and address and diagnosis and disease_date):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        query = """
            INSERT INTO Patients (full_name, address, diagnosis, disease_date)
            VALUES (%s, %s, %s, %s);
        """
        try:
            self.execute_query(query, (full_name, address, diagnosis, disease_date))
            messagebox.showinfo("Успех", "Новый больной добавлен.")
            self.result_text.insert("1.0", f"Добавлен новый больной: {full_name}")
        except Error as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить больного: {e}")

    def show_patient_details(self):
        patient_name = self.patient_name_entry.get().strip()
        if not patient_name:
            messagebox.showerror("Ошибка", "Введите ФИО больного!")
            return

        query = """
            SELECT address, disease_date, diagnosis
            FROM Patients
            WHERE full_name = %s;
        """
        result = self.execute_query(query, (patient_name,))
        if result:
            address, disease_date, diagnosis = result[0]
            self.result_text.insert(
                "1.0",
                f"Больной: {patient_name}\nАдрес: {address}\nДата заболевания: {disease_date}\nДиагноз: {diagnosis}"
            )
        else:
            messagebox.showerror("Ошибка", f"Пациент с ФИО '{patient_name}' не найден.")

    def show_doctor_schedule(self):
        doctor_name = self.doctor_name_entry.get().strip()
        if not doctor_name:
            messagebox.showerror("Ошибка", "Введите ФИО врача!")
            return

        query = """
            SELECT room_number, schedule
            FROM Doctors
            WHERE full_name = %s;
        """
        result = self.execute_query(query, (doctor_name,))
        if result:
            room_number, schedule = result[0]
            self.result_text.insert(
                "1.0",
                f"Врач: {doctor_name}\nКабинет: {room_number}\nРасписание: {schedule}"
            )
        else:
            messagebox.showerror("Ошибка", f"Врач с ФИО '{doctor_name}' не найден.")

    def add_new_doctor(self):
        full_name = self.doctor_name_entry.get().strip()
        room_number = self.room_number_entry.get().strip()
        section_number = self.section_number_entry.get().strip()

        if not (full_name and room_number and section_number):
            messagebox.showerror("Ошибка", "Все поля (ФИО, номер кабинета, номер участка) должны быть заполнены!")
            return

        schedule = []
        for day, (var, entry) in self.schedule_days.items():
            if var.get():
                hours = entry.get().strip()
                if not hours:
                    messagebox.showerror("Ошибка", f"Не указаны часы работы для {day}!")
                    return
                schedule.append(f"{day}: {hours}")
        schedule_text = "; ".join(schedule)

        if not schedule_text:
            messagebox.showerror("Ошибка", "Расписание должно быть указано хотя бы для одного дня!")
            return

        query = """
            INSERT INTO Doctors (full_name, room_number, section_number, schedule)
            VALUES (%s, %s, %s, %s);
        """
        try:
            self.execute_query(query, (full_name, room_number, section_number, schedule_text))
            messagebox.showinfo("Успех", "Новый врач добавлен.")
            self.result_text.insert("1.0", f"Добавлен новый врач:\nФИО: {full_name}\n"
                                           f"Кабинет: {room_number}\n"
                                           f"Участок: {section_number}\n"
                                           f"Расписание: {schedule_text}")
        except Error as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить врача: {e}")

    def remove_doctor(self):
        full_name = self.remove_doctor_entry.get().strip()

        if not full_name:
            messagebox.showerror("Ошибка", "Необходимо указать ФИО врача для удаления!")
            return

        query = "DELETE FROM Doctors WHERE full_name = %s;"
        try:
            self.execute_query(query, (full_name,))
            messagebox.showinfo("Успех", "Врач успешно удален.")
            self.result_text.insert("1.0", f"Врач удален: {full_name}")
        except Error as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить врача: {e}")

    def delete_patient(self):
        patient_name = self.patient_name_entry.get().strip()

        if not patient_name:
            messagebox.showerror("Ошибка", "Поле 'ФИО больного' не должно быть пустым!")
            return

        query = "DELETE FROM Patients WHERE full_name = %s;"
        result = self.execute_query(query, (patient_name,))
        print(result)
        if result is None:  # Если запрос выполнен успешно
            messagebox.showinfo("Успех", f"Пациент '{patient_name}' успешно удалён.")
            self.result_text.insert("1.0", f"Удалён больной: {patient_name}")
        else:
            messagebox.showerror("Ошибка", f"Не удалось удалить пациента '{patient_name}'. Возможно, он не существует.")

    def update_patient_diagnosis(self):
        patient_name = self.patient_name_entry.get().strip()
        new_diagnosis = self.new_diagnosis_entry.get().strip()

        if not (patient_name and new_diagnosis):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        query = """
            UPDATE Patients
            SET diagnosis = %s
            WHERE full_name = %s;
        """
        result = self.execute_query(query, (new_diagnosis, patient_name))

        if result is None:  # Проверка на успешность выполнения запроса
            messagebox.showinfo("Успех", f"Диагноз для '{patient_name}' успешно обновлён.")
            self.result_text.insert("1.0", f"Пациент: {patient_name}\nНовый диагноз: {new_diagnosis}")
        else:
            messagebox.showerror("Ошибка", f"Не удалось обновить диагноз для '{patient_name}'.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicApp(root)
    root.mainloop()
