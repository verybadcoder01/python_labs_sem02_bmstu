import tkinter as tk

import matplotlib.pyplot as plt
from PIL import Image, ImageTk

from math import *

class FunctionCalculator:
    def __init__(self, master):
        self.__root = master
        self.ffunc = tk.StringVar()
        self.gfunc = tk.StringVar()
        self.seg_ends = [tk.DoubleVar() for _ in range(2)]
        self.__dx_step = 0.01
        self.__func_step = 0.01
        self.__precision = 1e-5

        input_fields = [self.ffunc, self.gfunc, self.seg_ends[0], self.seg_ends[1]]
        input_labels = ['f(x): ', 'g(x): ', 'Начало отрезка', 'Конец отрезка']

        for i in range(len(input_fields)):
            label = tk.Label(master, text=input_labels[i])
            label.grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(master, textvariable=input_fields[i])
            entry.grid(row=i, column=1, padx=10, pady=5)

        compute_button = tk.Button(master, text="Compute", command=self.plot)
        compute_button.grid(row=4, column=0, padx=10, pady=10)

    def func_at_point(self, x, func_name='f'):
        if func_name == 'f':
            ffunc = self.ffunc.get().replace('x', f"({x:.10f})")
            return eval(ffunc)
        gfunc = self.gfunc.get().replace('x', f"({x:.10f})")
        return eval(gfunc)

    def f_minus_g(self, x):
        return self.func_at_point(x, 'f') - self.func_at_point(x, 'g')

    def one_root_segment(self):
        x = self.seg_ends[0].get()
        while x <= self.seg_ends[1].get():
            fx = self.f_minus_g(x)
            fx_step = self.f_minus_g(x + self.__dx_step)
            if fx * fx_step < 0:
                yield x, x + self.__func_step
            elif abs(fx * fx_step) <= 1e-7:
                yield x + self.__func_step * 0.5, x + self.__func_step * 1.5
            x += self.__func_step
        return None

    def function_roots(self):
        result = []
        for seg in self.one_root_segment():
            if seg:
                cur_x = (seg[0] + seg[1]) / 2
            else:
                return result
            for it_cnt in range(100):
                cur_fx = self.f_minus_g(cur_x)
                cur_dfx = (self.f_minus_g(cur_x + self.__dx_step) - self.f_minus_g(cur_x)) / self.__dx_step
                if abs(cur_dfx) <= 1e-7:
                    break
                next_x = cur_x - cur_fx / cur_dfx
                if abs(self.f_minus_g(next_x)) <= self.__precision:
                    result.append([next_x, self.func_at_point(next_x)])
                    break
                cur_x = next_x
        return result

    def plot(self):
        plt.clf()
        roots = self.function_roots()
        cur_x = self.seg_ends[0].get()
        xs = []
        while cur_x <= self.seg_ends[1].get():
            xs.append(cur_x)
            cur_x += self.__func_step
        ys_f = [self.func_at_point(i, 'f') for i in xs]
        ys_g = [self.func_at_point(i, 'g') for i in xs]
        plt.plot(xs, ys_f, color='blue', label='f(x)')
        plt.plot(xs, ys_g, color='red', label='g(x)')
        plt.scatter(*zip(*roots), color='black', label='Корни')
        plt.fill_between(xs, ys_f, ys_g, where=[ys_f[i] < ys_g[i] for i in range(min(len(ys_f), len(ys_g)))], color='lightblue')
        plt.grid(True)
        plt.legend()
        plt.savefig('graph.png')
        image = Image.open('graph.png')
        resized_image = image.resize((1000, 700))
        photo = ImageTk.PhotoImage(resized_image)
        img_label = tk.Label(self.__root, image=photo)
        img_label.image = photo
        img_label.grid(row=0, column=2, rowspan=5, columnspan=3)

def main():
    root = tk.Tk()
    _ = FunctionCalculator(root)
    root.mainloop()

if __name__ == '__main__':
    main()