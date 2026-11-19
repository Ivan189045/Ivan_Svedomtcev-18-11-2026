import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class SportsInventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Учёт спортивного инвентаря — Спринт 1")
        self.root.geometry("760x480")
        self.root.resizable(False, False)

        # Хранилище данных в оперативной памяти (список словарей)
        self.records = []
        self.next_id = 1

        self.create_widgets()

    def create_widgets(self):
        # --- Блок 1: Форма добавления записи ---
        form_frame = ttk.LabelFrame(self.root, text="Выдача инвентаря", padding=10)
        form_frame.pack(fill="x", padx=15, pady=10)

        # Название предмета
        ttk.Label(form_frame, text="Предмет:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.item_entry = ttk.Entry(form_frame, width=25)
        self.item_entry.grid(row=0, column=1, padx=5, pady=5)

        # Количество
        ttk.Label(form_frame, text="Количество:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.qty_entry = ttk.Entry(form_frame, width=10)
        self.qty_entry.insert(0, "1")  # Значение по умолчанию
        self.qty_entry.grid(row=0, column=3, padx=5, pady=5)

        # Получатель (студент)
        ttk.Label(form_frame, text="Получатель:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.student_entry = ttk.Entry(form_frame, width=25)
        self.student_entry.grid(row=1, column=1, padx=5, pady=5)

        # Дата выдачи
        ttk.Label(form_frame, text="Дата выдачи:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.date_entry = ttk.Entry(form_frame, width=15)
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))  # Текущая дата
        self.date_entry.grid(row=1, column=3, padx=5, pady=5)

        # Кнопка добавления
        add_btn = ttk.Button(form_frame, text="Выдать инвентарь", command=self.add_record)
        add_btn.grid(row=0, column=4, rowspan=2, padx=15, pady=5, ipady=10)

        # --- Блок 2: Таблица выданного инвентаря ---
        table_frame = ttk.LabelFrame(self.root, text="Журнал выдачи", padding=10)
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        columns = ("id", "item", "qty", "student", "date", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        self.tree.heading("id", text="№")
        self.tree.heading("item", text="Предмет")
        self.tree.heading("qty", text="Кол-во")
        self.tree.heading("student", text="Получатель")
        self.tree.heading("date", text="Дата выдачи")
        self.tree.heading("status", text="Статус")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("item", width=200)
        self.tree.column("qty", width=70, anchor="center")
        self.tree.column("student", width=180)
        self.tree.column("date", width=100, anchor="center")
        self.tree.column("status", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def add_record(self):
        item = self.item_entry.get().strip()
        qty_str = self.qty_entry.get().strip()
        student = self.student_entry.get().strip()
        issue_date = self.date_entry.get().strip()

        # Валидация пустых полей
        if not item or not qty_str or not student or not issue_date:
            messagebox.showwarning("Ошибка ввода", "Пожалуйста, заполните все поля!")
            return

        # Валидация количества (должно быть целым положительным числом)
        if not qty_str.isdigit() or int(qty_str) <= 0:
            messagebox.showwarning("Ошибка ввода", "Количество должно быть целым числом больше нуля!")
            return

        # Создаём запись
        record = {
            "id": self.next_id,
            "item": item,
            "qty": int(qty_str),
            "student": student,
            "date": issue_date,
            "status": "Выдан"
        }
        self.records.append(record)
        self.next_id += 1

        self.refresh_table()
        self.clear_inputs()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for rec in self.records:
            self.tree.insert(
                "",
                "end",
                values=(rec["id"], rec["item"], rec["qty"], rec["student"], rec["date"], rec["status"])
            )

    def clear_inputs(self):
        self.item_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)
        self.qty_entry.insert(0, "1")
        self.student_entry.delete(0, tk.END)
        self.item_entry.focus()


if __name__ == "__main__":
    root = tk.Tk()
    app = SportsInventoryApp(root)
    root.mainloop()
