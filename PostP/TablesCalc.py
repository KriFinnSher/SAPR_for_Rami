from Proc import Porcessor
import tkinter as tk
from tkinter import ttk


def prepare_tables(input_data, divider):
    size = len(input_data['f1']) + 1
    tables = [[] for _ in range(size)]

    f1 = input_data['f1']
    f2 = input_data['f2']
    A = input_data['A']
    L = input_data['L']
    E = input_data['E']
    sigma = input_data['sigma']
    q = input_data['q']

    deltas = Porcessor.find_deltas(input_data)

    for i, bar in enumerate(zip(f1, f2, A, L, E, sigma, q)):
        delta_0, delta_l = deltas[i], deltas[i+1]
        for j in range(divider+1):
            x = round(float(bar[3]) / divider * j, 4)
            n = Porcessor.find_n(x, delta_0, delta_l, float(bar[3]), float(bar[6]), float(bar[4]), float(bar[2]))
            u = Porcessor.find_u(x, delta_0, delta_l, float(bar[3]), float(bar[6]), float(bar[4]), float(bar[2]))
            sig = Porcessor.find_sigma(n, float(bar[2]))

            tables[i+1].append((x, n, u, sig, float(bar[5])))

    del tables[0]

    return tables


def create_notebook_with_tables(data):
    def show_table(index):
        for i, frame in enumerate(table_frames):
            if i == index:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()

    window = tk.Tk()
    window.title("Расчетные таблицы")
    window.geometry("500x400")
    window.resizable(False, False)

    button_frame_container = tk.Frame(window)
    button_frame_container.pack(fill="x", pady=5)

    canvas = tk.Canvas(button_frame_container, height=40)
    scrollbar = ttk.Scrollbar(button_frame_container, orient="horizontal", command=canvas.xview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(xscrollcommand=scrollbar.set)

    canvas.pack(side="top", fill="x", expand=True)
    scrollbar.pack(side="bottom", fill="x")

    table_frames = []

    for index, table_data in enumerate(data):
        button = tk.Button(scrollable_frame, text=f"Таблица {index + 1}",
                           font=("Helvetica", 8), bg="black", fg="white",
                           command=lambda i=index: show_table(i))
        button.pack(side="left", padx=5, pady=5)

        table_frame = tk.Frame(window)
        table_frames.append(table_frame)

        title_label = tk.Label(table_frame, text=f"Таблица {index + 1}", font=("Helvetica", 10, "bold"),
                               fg="white", bg="black", anchor="center", height=2)
        title_label.pack(fill="x")

        treeview = ttk.Treeview(table_frame, columns=("x", "N(x)", "U(x)", "σ(x)", "[σ]"), show="headings", height=12)
        treeview.pack(expand=True, fill="both", padx=5, pady=5)

        treeview.column("x", width=85, anchor="center")
        treeview.column("N(x)", width=85, anchor="center")
        treeview.column("U(x)", width=85, anchor="center")
        treeview.column("σ(x)", width=85, anchor="center")
        treeview.column("[σ]", width=85, anchor="center")

        treeview.heading("x", text="x")
        treeview.heading("N(x)", text="N(x)")
        treeview.heading("U(x)", text="U(x)")
        treeview.heading("σ(x)", text="σ(x)")
        treeview.heading("[σ]", text="[σ]")

        treeview.tag_configure('red', foreground='red', font=("Arial", 9, "bold"))

        for row in table_data:
            if abs(row[-2]) > row[-1]:
                treeview.insert("", "end", values=row, tags=("red",))
            else:
                treeview.insert("", "end", values=row)

    show_table(0)