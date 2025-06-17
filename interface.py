import tkinter as tk
from tkinter import ttk, messagebox
from simulate_trajectory import calculate_trajectory, create_plot
import webbrowser
from presets import save_preset
import os

class trajectory:
    def __init__(self, root):
        self.params = [
            ('v0', 'Начальная скорость (м/с):'), 
            ('theta', 'Угол θ (°):'),
            ('phi', 'Угол φ (°):'),
            ('wind_speed', 'Скорость ветра (м/с):'),
            ('wind_dir', 'Направление ветра (°):'),
            ('mass', 'Масса снаряда (кг):'),
            ('diameter', 'Диаметр снаряда (см):'),
            ('air_density', 'Плотность воздуха (кг/м³):'),
            ('gravity', 'Гравитация (м/с²):'),
            ('dt_param', 'Частота дискредитации точек графика\n' \
            '(0 для авто)')
        ]
        self.root = root
        self.root.title("Моделирование траектории снаряда")
        self.setup_ui()

    def get_params_dict(self):
        try:
            params_dict = {
                'v0': float(self.entries['v0'].get()),
                'theta': float(self.entries['theta'].get()),
                'phi': float(self.entries['phi'].get()),
                'wind_speed': float(self.entries['wind_speed'].get()),
                'wind_direction': float(self.entries['wind_dir'].get()),
                'mass': float(self.entries['mass'].get()),
                'diameter': float(self.entries['diameter'].get()),
                'air_density': float(self.entries['air_density'].get()),
                'gravity': float(self.entries['gravity'].get()),
                'dt_param':float(self.entries['dt_param'].get())
            }
        except Exception:
                messagebox.showerror("Ошибка", "Проверьте правильность введенных данных")
        return params_dict
    
    def load_preset(self, i):
        try:
            file_path = os.path.join(os.path.dirname(__file__), "preset_data.txt")
            
            with open(file_path, 'r') as f:
                lines = f.readlines()

                values = list(map(float, lines[i].split()))
                
                param_names = [
                    'v0', 'theta', 'phi', 'wind_speed', 
                    'wind_dir', 'mass', 'diameter', 
                    'air_density', 'gravity', 'dt_param'
                ]

                for name, value in zip(param_names, values):
                    self.entries[name].delete(0, tk.END)
                    self.entries[name].insert(0, str(value))
                              
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить пресет:\n{str(e)}")
    
    def create_buttons(self, i, frame_presets):

        ttk.Label(frame_presets, text = f'Пресет {i-1}').grid(row = i, column=0, sticky='w')
        button_save = ttk.Button(frame_presets, text = "Сохранить", command = lambda: save_preset(i, **self.get_params_dict()))
        button_save.grid(row = i, column = 1, pady = 5)
        button_load = ttk.Button(frame_presets, text = "Загрузить", command = lambda: self.load_preset(i))
        button_load.grid(row = i, column = 2, pady = 5)
            

    def help_window(self):

        messagebox.showinfo("Информация", "Краткое руководство пользования.\n\n" \
        "Программа предназначена для построения траектории полета тела при произвольно заданных условиях.\n" \
        "Используется физическая сферическая система координат, соответственно: \n\nУгол θ (°) - угол между вектором скорости и осью Z\n" \
        "Угол φ (°) - угол между вектором скорости и осью X\nНаправление ветра - угол φ (°), задающий направление ветра, если он есть.\n\n" \
        "Частота дискредитации точек - частота, с которой проставляются точки на графике. Большие значения приводят к большей точности, " \
        "но требуют больше ресурсов компьютера (использовать осторожно).\n\n" \
        "Дополнение о точности:\nПри скорости ветра >100 м/с траектория отображается неверно из-за действия закона Бернулли," \
        " которое программой не учитывается.\n\n" \
        "Допустимые значения:\nСкорость > 0 \nУгол θ [0,90) \nУгол φ произовольный \nНаправление ветра произвольно \nСкорость ветра произвольно" \
        "\nМасса > 0 \nДиаметр [0.01, 100] \nСопротивление воздуха > 0 \nУскорение свободного падения (гравитация) > 0 " \
        "\nЧастота дискредитации - на сколько хватит смелости")
        
    def setup_ui(self):

        frame_params = ttk.LabelFrame(self.root, text="Параметры", padding=10)
        frame_params.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        frame_presets = ttk.LabelFrame(self.root, text = "Пресеты", padding = 10)
        frame_presets.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady = 5)
        
        self.entries = {} # сюда все параметры

        
        for j, (name, label) in enumerate(self.params):
            ttk.Label(frame_params, text=label).grid(row=j, column=0, sticky="w")
            entry = ttk.Entry(frame_params)
            entry.grid(row=j, column=1, pady=5)
            entry.insert(0, 10)
            self.entries[name] = entry
        
        btn_calculate = ttk.Button(frame_params, text="Рассчитать траекторию", 
                                command=self.on_calculate)
        btn_calculate.grid(row=len(self.params), column=0, columnspan=2, pady=10)
       
        for j in range(5):
            self.create_buttons(j, frame_presets)

        help_button = ttk.Button(frame_presets, text = 'HELP', command=self.help_window)
        help_button.grid(row = 10, column = 2, pady = 50)


    
    def on_calculate(self):
        try:
            params_dict = self.get_params_dict()
            
            x, y, z = calculate_trajectory(**params_dict)
            fig = create_plot(x, y, z)
            
            if fig:
                html_file = "trajectory_plot.html"
                fig.write_html(html_file)
                webbrowser.open(html_file)
                
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте правильность введенных данных")

if __name__ == "__main__":
    root = tk.Tk()
    app = trajectory(root)
    root.mainloop()
