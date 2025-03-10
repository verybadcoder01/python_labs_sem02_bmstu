import tkinter as tk
from tkinter import messagebox, ttk, Image

from calc_back import NewtonMethodErrors, NewtonRootFinder, GraphBuilder, Function

from PIL import Image, ImageTk


def format_results(results):
    formatted_strings = []

    for result in results:
        root_number, left_border, right_border, root, function_value, iterations, error_code = result
        formatted_root_number = f"{root_number:>3}"
        formatted_left_border = f"{left_border:.4f}"
        formatted_right_border = f"{right_border:.4f}"
        if isinstance(root, float):
            formatted_root = f"{root:.4f}"
        else:
            formatted_root = "-"
        if isinstance(function_value, float):
            formatted_function_value = f"{function_value:.1e}"
        else:
            formatted_function_value = "-"
        formatted_iterations = f"{iterations:>5}"
        if error_code == NewtonMethodErrors.ZERO_DF:
            error_representation = "Derivative of the function is zero somewhere on this segment"
        else:
            error_representation = f"{error_code}"
        formatted_string = [
            f"{formatted_root_number}",
            f"{formatted_left_border}, {formatted_right_border}",
            f"{formatted_root}",
            f"{formatted_function_value}",
            f"{formatted_iterations}",
            f"{error_representation}"
        ]
        formatted_strings.append(formatted_string)

    return formatted_strings


class FunctionRootCalculator:
    def __init__(self, master):
        self.func_field = tk.StringVar()
        self.segment_ends = [tk.DoubleVar() for _ in range(2)]
        self.step = tk.DoubleVar()
        self.max_iterations = tk.IntVar()
        self.precision = tk.DoubleVar()

        input_fields = [self.func_field, self.segment_ends[0], self.segment_ends[1], self.step, self.max_iterations,
                        self.precision]
        input_labels = ["Function", "Left segment end", "Right segment end", "Division step", "Max iterations",
                        "Required precision"]

        self.__root = master

        for i in range(6):
            master.grid_rowconfigure(i, weight=1)
        master.grid_rowconfigure(6, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

        for i in range(6):
            label = tk.Label(master, text=input_labels[i])
            label.grid(row=i, column=0, padx=10, pady=5)

            entry = tk.Entry(master, textvariable=input_fields[i])
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="snew")

        compute_button = tk.Button(master, text="Compute", command=self.compute)
        compute_button.grid(row=6, column=0, padx=10, pady=10, sticky="snew")

        info_button = tk.Button(master, text="Info", command=self.show_info)
        info_button.grid(row=6, column=1, padx=10, pady=10, sticky="snew")

    def create_table(self, data, photo):
        window = tk.Toplevel(master=self.__root)
        window.title("Roots table")

        col_names = ["col1", "col2", "col3", "col4", "col5", "col6"]
        col_texts = ["Root#", "[x_i, x_i+1]", "x'", "f(x')", "Кол-во итераций", "Код ошибки"]
        widths = [100, 300, 200, 200, 100, 100]

        tree = ttk.Treeview(window, columns=col_names, show='headings', height=50)

        for i in range(len(col_names)):
            tree.heading(col_names[i], text=col_texts[i])
            tree.column(col_names[i], width=widths[i], minwidth=widths[i])

        for row in data:
            tree.insert("", "end", values=row)

        scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure("Treeview", rowheight=50)

        img_label = tk.Label(window, image=photo)
        img_label.image = photo
        img_label.grid(row=0, column=7, rowspan=5, columnspan=3)

    def compute(self):
        func = Function(self.func_field.get())
        root_finder = NewtonRootFinder(func, 0, self.segment_ends[0].get(), self.segment_ends[1].get(), self.step.get(),
                                       self.precision.get(), self.max_iterations.get())
        try:
            roots = root_finder.function_roots()
        except Exception as e:
            messagebox.showinfo("Error", f"Critical error while finding roots: {e}")
            return
        plotter = GraphBuilder(self.func_field.get(), self.segment_ends[0].get(), self.segment_ends[1].get(),
                               self.precision.get())
        file = plotter.plot([[i[3], i[4]] for i in roots if i[-1] == 0])
        image = Image.open(file)
        resized_image = image.resize((1000, 700))
        photo = ImageTk.PhotoImage(resized_image)
        self.create_table(format_results(roots), photo)

    @staticmethod
    def show_info():
        messagebox.showinfo("Info",
                            "Программа для вычисления корней функции на отрезке методом Ньютона.\nВсем функциям необходимо ставить скобки, степень обозначается ^, запись 3х не допускается (нужно писать 3*x).\nМодули программой не обрабатываются.\nАвтор Янбухтин Даниил ИУ7-22Б")


def main():
    root = tk.Tk()
    root.title("Function root calculator")
    _ = FunctionRootCalculator(root)
    root.mainloop()


if __name__ == '__main__':
    main()
