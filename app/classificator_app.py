import ttk
import math
import matplotlib
from sklearn.linear_model import LogisticRegression
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Tkinter import *
import Tkinter as tk


LARGE_FONT= ("Verdana", 12)


class ClassificatorApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Login/Password Classificator")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.login = ""
        self.canvas_log = 0
        self.canvas_pass = 0
        self.model_array = []
        self.model_array_log = []
        self.model_array_pass = []
        self.model = LogisticRegression()
        with open('data', 'r') as f:
            self.data_array = f.read().split('\n')
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        login_list = self.data_array_init(self.data_array, 'login')
        self.login_time = self.data_array_init(self.data_array, 'logTimeArray')
        self.login_time = self.data_array_init(self.data_array, 'passTimeArray')
        self.text_login = ttk.Combobox(self, values=login_list)
        button = ttk.Button(self, text="Build Graphs",
                            command=lambda: self.button_onclick())
        button_check = ttk.Button(self, text="Check pair",
                            command=lambda: self.button_check_onclick())
        self.label_var = StringVar()
        label_check = tk.Label(self, textvariable=self.label_var, font=LARGE_FONT)
        label_check.pack()
        button.pack()
        button_check.pack()
        self.text_login.pack()

    def button_onclick(self):
        login = self.text_login.get()
        t = [-3, -2, -1, 0, 1, 2, 3]
        buf_x_login = []
        buf_x_pass = []
        buf_t = []
        for data in self.data_array:
            try:
                data_dict = eval(data)
                if data_dict['login'] == login:
                    buf_login = self.andrews_plot(data_dict['logTimeArray'], t)
                    buf_pass = self.andrews_plot(data_dict['passTimeArray'], t)
                    buf_x_login.append(buf_login)
                    buf_x_pass.append(buf_pass)
                    buf_t.append(t)
                    self.model_array.append([self.make_class_array(buf_login), self.make_class_array(buf_pass)])
            except Exception:
                print('done')
        print self.model_array
        self.plot(buf_t, buf_x_login, 0)
        self.plot(buf_t, buf_x_pass, 1)

    def button_check_onclick(self):
        y = [1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1]
        self.model.fit(self.model_array[0:15], y)
        expected = [0, 0, 1]
        predicted = self.model.predict(self.model_array[15:19])
        buf_str = ""
        for i in predicted:
            if i == 1:
                buf_str += "y"
            else:
                buf_str += "n"
        self.label_var.set(buf_str)

    def data_array_init(self, data_dict, key):
        buf_list = []
        for data in data_dict:
            try:
                if eval(data)[key] not in buf_list:
                    buf_list.append(eval(data)[key])
            except Exception:
                print('done')
        return buf_list

    def plot(self, x, t, plot):
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        length = len(x)
        i = 0
        while i != length:
            a.plot(x[i], t[i])
            i += 1
        if self.canvas_log == 0 and plot == 0:
            self.canvas_log = FigureCanvasTkAgg(f, self)
            self.canvas_log.show()
            self.canvas_log.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            self.canvas_log._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        elif plot == 0:
            self.canvas_log.get_tk_widget().destroy()
            self.canvas_log = 0
            self.plot(x, t, plot)

        if self.canvas_pass == 0 and plot == 1:
            self.canvas_pass = FigureCanvasTkAgg(f, self)
            self.canvas_pass.show()
            self.canvas_pass.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            self.canvas_pass._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        elif plot == 1:
            self.canvas_pass.get_tk_widget().destroy()
            self.canvas_pass = 0
            self.plot(x, t, plot)

    def andrews_plot(self, x, t):
        curve = []
        for i in t:
            flag_sin_cos = 1
            count_sin_cos = 1
            point = x[0] + math.sqrt(2)
            for j in x:
                if flag_sin_cos:
                    flag_sin_cos = 0
                    point += j * math.sin(count_sin_cos * i)
                else:
                    flag_sin_cos = 1
                    point += j * math.cos(count_sin_cos * i)
                    count_sin_cos += 1
            curve.append(point)
        return curve

    def get_answer(self):
        return "coincidence"

    def make_class_array(self, in_array):
        length = len(in_array)
        out = 0
        i = 0
        while i < (length-1):
            out += math.fabs(in_array[i+1]-in_array[i])
            i += 1
        return out


app = ClassificatorApp()
app.mainloop()
