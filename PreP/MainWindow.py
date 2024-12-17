import json
import tkinter as tk
from collections import defaultdict
from tkinter import ttk, Menu, filedialog

import numpy as np

from PreP import InputValidator, ConstructionDraw
from PostP import TablesCalc, SectionCalc, FileCalc
from Proc import Porcessor

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class StructuralApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Structural Analysis")

        self.npn = (self.root.register(InputValidator.npn_checker), '%P')
        self.rpn = (self.root.register(InputValidator.rpn_checker), '%P')
        self.rn = (self.root.register(InputValidator.rn_checker), '%P')

        self.all_data = defaultdict(list)
        self.rows = []


        self.create_menu()
        self.create_main_layout()
        self.root.geometry("770x750")
        self.root.resizable(False, False)



    def create_menu(self):


        menu_bar = Menu(self.root)


        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_command(label="Добавить", command=self.open_file)
        file_menu.add_command(label="Создать отчет", command=self.create_report)
        file_menu.add_command(label="Сбросить ввод", command=self.reset_input)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        calc_menu = Menu(menu_bar, tearoff=0)
        calc_menu.add_command(label="Расчет сечения", command=self.section_calculation)
        calc_menu.add_command(label="Общий расчет", command=self.general_calculation)
        menu_bar.add_cascade(label="Расчеты", menu=calc_menu)

        epure_menu = Menu(menu_bar, tearoff=0)
        epure_menu.add_command(label="Эпюры", command=self.show_epura_interface)
        menu_bar.add_cascade(label="Эпюры", menu=epure_menu)

        self.root.config(menu=menu_bar)

    def create_main_layout(self):
        self.main_pane = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.stiff_pane = ttk.Labelframe(self.main_pane, text="Стержни")


        self.canvas = tk.Canvas(self.stiff_pane, height=150)
        self.scrollbar = ttk.Scrollbar(self.stiff_pane, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        ttk.Button(self.scrollable_frame, text="Создать", command=self.create_element).grid(row=0, column=0,
                                                                                                 padx=5, pady=5)
        labels = ["Нач. узел, F", "Кон. узел, F", "A, м^2", "L, м", "E, Па", "[σ], Па", "q, Н/м"]
        for i, text in enumerate(labels, start=1):
            ttk.Label(self.scrollable_frame, text=text).grid(row=0, column=i, padx=5, pady=5)

        a = ttk.Label(self.scrollable_frame, text="Стержень 1")
        a.grid(row=1, column=0, padx=5, pady=5)


        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.stiff_pane.pack(fill=tk.X, expand=False, ipadx=5, ipady=5)
        self.stiff_pane.config(height=200)
        self.main_pane.add(self.stiff_pane, weight=0)

        self.scheme_pane = ttk.Labelframe(self.main_pane, text="Схема конструкции")
        self.scheme_pane.pack_propagate(False)

        self.display_button = ttk.Button(self.scheme_pane, text="Отобразить конструкцию", command=self.drawing)
        self.display_button.pack(pady=5)


        self.canvas_scheme = tk.Canvas(self.scheme_pane, bg="white")
        self.canvas_scheme.pack(fill=tk.BOTH, expand=True)

        self.main_pane.add(self.scheme_pane, weight=1)

        support_pane = ttk.Labelframe(self.main_pane, text="Опоры конструкции")
        self.support_var = tk.StringVar(value="Опора слева")
        options = ["Опора слева", "Опора справа", "2 опоры"]
        for i, option in enumerate(options):
            ttk.Radiobutton(support_pane, text=option, variable=self.support_var, value=option).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
        self.main_pane.add(support_pane, weight=0)

        row_widgets = []
        row_widgets.append(a)
        for i in range(1, 8):
            match i:
                case 1:
                    entry = ttk.Entry(self.scrollable_frame, width=10, validate="all", validatecommand=self.rn)
                    entry.grid(row=1, column=i, padx=5, pady=5)
                    entry.insert(0, '0')
                case 2:
                    entry = ttk.Entry(self.scrollable_frame, width=10, validate="all", validatecommand=self.rn)
                    entry.grid(row=1, column=i, padx=5, pady=5)
                    entry.insert(0, '0')
                case 3:
                    entry = ttk.Entry(self.scrollable_frame, width=10, validate="all", validatecommand=self.rpn)
                    entry.grid(row=1, column=i, padx=5, pady=5)
                case 4:
                    entry = ttk.Entry(self.scrollable_frame, width=10, validate="all", validatecommand=self.rpn)
                    entry.grid(row=1, column=i, padx=5, pady=5)
                case 5:
                    entry = ttk.Entry(self.scrollable_frame, width=10, validate="all", validatecommand=self.rpn)
                    entry.grid(row=1, column=i, padx=5, pady=5)
                case 6:
                    entry = ttk.Entry(self.scrollable_frame, width=10, validate="all", validatecommand=self.rpn)
                    entry.grid(row=1, column=i, padx=5, pady=5)
                case 7:
                    entry = ttk.Entry(self.scrollable_frame, width=10, validate="all", validatecommand=self.rn)
                    entry.grid(row=1, column=i, padx=5, pady=5)
                    entry.insert(0, '0')
            row_widgets.append(entry)
        self.rows.append(row_widgets)

    def add_element(self):
        idx = len(self.rows) + 1
        row_widgets = []

        label = ttk.Label(self.scrollable_frame, text=f"Стержень {idx}")
        label.grid(row=idx, column=0, padx=5, pady=5)
        row_widgets.append(label)

        for i in range(1, 8):
            match i:
                case 1:
                    entry = ttk.Entry(self.scrollable_frame, width=10, validate="all", validatecommand=self.rn)
                    entry.grid(row=1, column=i, padx=5, pady=5)
                    entry.insert(0, '0')
                case 2:
                    entry = ttk.Entry(self.scrollable_frame, width=10, validate="all", validatecommand=self.rn)
                    entry.grid(row=1, column=i, padx=5, pady=5)
                    entry.insert(0, '0')
                case 3:
                    entry = ttk.Entry(self.scrollable_frame, width=10, validate="all", validatecommand=self.rpn)
                    entry.grid(row=1, column=i, padx=5, pady=5)
                case 4:
                    entry = ttk.Entry(self.scrollable_frame, width=10, validate="all", validatecommand=self.rpn)
                    entry.grid(row=1, column=i, padx=5, pady=5)
                case 5:
                    entry = ttk.Entry(self.scrollable_frame, width=10, validate="all", validatecommand=self.rpn)
                    entry.grid(row=1, column=i, padx=5, pady=5)
                case 6:
                    entry = ttk.Entry(self.scrollable_frame, width=10, validate="all", validatecommand=self.rpn)
                    entry.grid(row=1, column=i, padx=5, pady=5)
                case 7:
                    entry = ttk.Entry(self.scrollable_frame, width=10, validate="all", validatecommand=self.rn)
                    entry.grid(row=1, column=i, padx=5, pady=5)
                    entry.insert(0, '0')
            entry.grid(row=idx, column=i, padx=5, pady=5)
            row_widgets.append(entry)

        delete_btn = ttk.Button(self.scrollable_frame, text="Стереть", command=lambda: self.delete_row(row_widgets))
        delete_btn.grid(row=idx, column=8, padx=5, pady=5)
        row_widgets.append(delete_btn)

        self.rows.append(row_widgets)

        self.update_indices()

    def delete_row(self, row_widgets):
        for widget in row_widgets:
            widget.destroy()

        self.rows.remove(row_widgets)

        self.update_indices()

    def update_indices(self):
        for idx, row_widgets in enumerate(self.rows, start=1):
            label = row_widgets[0]
            label.config(text=f"Стержень {idx}")

            for widget in row_widgets:
                widget.grid_configure(row=idx)

    def save_file(self):
        self.collect_data()
        data = self.all_data
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".json",
                                               filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                self.reset_input()

                for i in range(len(data['f1'])):

                    self.rows[i][1].delete(0, tk.END)
                    self.rows[i][2].delete(0, tk.END)
                    self.rows[i][7].delete(0, tk.END)

                    self.rows[i][1].insert(0, data['f1'][i])
                    self.rows[i][2].insert(0, data['f2'][i])
                    self.rows[i][3].insert(0, data['A'][i])
                    self.rows[i][4].insert(0, data['L'][i])
                    self.rows[i][5].insert(0, data['E'][i])
                    self.rows[i][6].insert(0, data['sigma'][i])
                    self.rows[i][7].insert(0, data['q'][i])
                    if i != len(data['f1']) - 1:
                        self.add_element()

                op_map = {
                    1: "Опора слева",
                    2: "Опора справа",
                    3: "2 опоры"
                }
                op = op_map[data['op']]
                self.support_var.set(op)
            self.drawing()



    def collect_data(self):
        self.all_data.clear()

        data = self.all_data

        for row in self.rows:
            data['f1'].append(row[1].get())
            data['f2'].append(row[2].get())
            data['A'].append(row[3].get())
            data['L'] .append(row[4].get())
            data['E'].append(row[5].get())
            data['sigma'].append(row[6].get())
            data['q'].append(row[7].get())

        op_map = {
            "Опора слева": 1,
            "Опора справа": 2,
            "2 опоры": 3
        }
        op = self.support_var.get()

        data['op'] = op_map[op]

    def drawing(self):
        self.collect_data()
        if 1: # поменяй на проверку ввода
            self.all_data["L"] = ConstructionDraw.change_scale(self.all_data["L"], 10)
            ls = [float(val) for val in self.all_data["L"]]

            hs = [float(val) for val in self.all_data['A']]
            hs = ConstructionDraw.change_scale(hs, 10)

            conc_loads = []
            ar1 = self.all_data["f1"]
            ar2 = self.all_data["f2"]

            conc_loads.append(ar1[0])
            for i in range(1, min(len(ar1), len(ar2))):
                conc_loads.append(float(ar1[i]) + float(ar2[i - 1]))
            conc_loads.append(ar2[-1])

            dist_loads = self.all_data["q"]

            left_z = [self.all_data["op"] == 1 or self.all_data["op"] == 3]
            right_z = [self.all_data["op"] == 2 or self.all_data["op"] == 3]

            self.scheme = ConstructionDraw.display_scheme(self.canvas_scheme, ls, hs, conc_loads, dist_loads, left_z,
                                               right_z)



    def create_report(self):
        self.collect_data()

        if 1:
            self.show_epura_interface(for_file=True)
            us_t, calc_t = FileCalc.prepare_data(self.all_data)

            FileCalc.create_word_report(us_t, calc_t, self.scheme, self.fig_n, self.fig_sigma, self.fig_u)


    def show_epura_interface(self, for_file=False):
        self.collect_data()

        if 1:

            l1, l2, l3 = Porcessor.find_coordinates(self.all_data)

            def create_figure_epura_n_sigma(x_coords, y_coords, epur_type):
                fig = Figure(figsize=(6, 4), dpi=100)
                ax = fig.add_subplot(111)
                size = len(y_coords)
                main_lne = [0] * size

                ax.plot(x_coords, main_lne, color='black')
                ax.plot(x_coords, y_coords, color='black')
                ax.fill_between(x_coords, main_lne, y_coords, color='grey')
                ax.set_title(f"Эпюра {epur_type}(x)")
                return fig

            def create_figure_epura_u(data):
                t = 0
                fig = Figure(figsize=(6, 4), dpi=100)
                ax = fig.add_subplot(111)

                f1 = data['f1']
                f2 = data['f2']
                A = data['A']
                L = data['L']
                E = data['E']
                sigma = data['sigma']
                q = data['q']

                for i, bar in enumerate(zip(f1, f2, A, L, E, sigma, q)):
                    l, e, a, q = float(bar[3]), float(bar[4]), float(bar[2]), float(bar[-1])
                    delta_0, delta_l = Porcessor.find_deltas(data)[i], Porcessor.find_deltas(data)[i + 1]

                    x = np.linspace(0, l, 10000)
                    y = [Porcessor.find_u(xi, delta_0, delta_l, l, q, e, a) for xi in x]

                    ax.plot(x + t, y, color='black')
                    ax.fill_between(x + t, [0] * len(x), y, color='grey')

                    t += l

                ax.set_title("Эпюра U(x)")
                return fig

            new_window = tk.Toplevel()
            new_window.title("Просмотр Эпюр")
            new_window.geometry("600x900")
            new_window.resizable(False, False)

            self.fig_n = create_figure_epura_n_sigma(l1, l2, "N")
            self.fig_sigma = create_figure_epura_n_sigma(l1, l3, "σ")
            self.fig_u = create_figure_epura_u(self.all_data)

            def display_figure(parent, figure, row):
                canvas = FigureCanvasTkAgg(figure, master=parent)
                canvas.draw()
                canvas.get_tk_widget().grid(row=row, column=0, padx=10, pady=10, sticky="nsew")

            new_window.rowconfigure(0, weight=1)
            new_window.rowconfigure(1, weight=1)
            new_window.rowconfigure(2, weight=1)
            new_window.columnconfigure(0, weight=1)

            display_figure(new_window, self.fig_n, row=0)
            display_figure(new_window, self.fig_sigma, row=1)
            display_figure(new_window, self.fig_u, row=2)

            if for_file:
                new_window.destroy()


    def reset_input(self):
        for widgets in self.rows[1:]:
            self.delete_row(widgets)
        for i, entry in enumerate(self.rows[0][1:]):
            entry.delete(0, tk.END)
            if i in (0, 1, 6):
                entry.insert(0, '0')
        self.canvas_scheme.delete('all')


    def create_element(self):
        self.add_element()

    def section_calculation(self):
        self.collect_data()

        if 1:
            SectionCalc.create_section_window(self.all_data)

    def general_calculation(self):
        self.collect_data()

        if 1:
            tables = TablesCalc.prepare_tables(self.all_data, 10)
            TablesCalc.create_notebook_with_tables(tables)