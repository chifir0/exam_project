import tkinter as tk
from tkinter import ttk
from simulate_trajectory import calculate_trajectory, create_plot
import webbrowser
from tkinter import messagebox
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
            ('diameter', 'Диаметр снаряда (м):'),
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
        print('loading...')
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
            print(f'string number is {i}')
            print('file closed')           
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить пресет:\n{str(e)}")
            

    def help_window(): # ДОДЕЛАЮ
        ...
        
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
       
        ttk.Label(frame_presets, text = f'Пресет 1').grid(row = 0, column=0, sticky='w') # КОПИПАСТА ОСМЫСЛЕННАЯ И БЕСПОЩАДНАЯ
        button_save = ttk.Button(frame_presets, text = "Сохранить", command = lambda: save_preset(0, **self.get_params_dict()))
        button_save.grid(row = 0, column = 1, pady = 5)
        button_load = ttk.Button(frame_presets, text = "Загрузить", command = lambda: self.load_preset(0))
        button_load.grid(row = 0, column = 2, pady = 5)

        ttk.Label(frame_presets, text = f'Пресет 2').grid(row = 1, column=0, sticky='w')
        button_save = ttk.Button(frame_presets, text = "Сохранить", command = lambda: save_preset(1, **self.get_params_dict()))
        button_save.grid(row = 1, column = 1, pady = 5)
        button_load = ttk.Button(frame_presets, text = "Загрузить", command = lambda: self.load_preset(1))
        button_load.grid(row = 1, column = 2, pady = 5)

        ttk.Label(frame_presets, text = f'Пресет 3').grid(row = 2, column=0, sticky='w')
        button_save = ttk.Button(frame_presets, text = "Сохранить", command = lambda: save_preset(2, **self.get_params_dict()))
        button_save.grid(row = 2, column = 1, pady = 5)
        button_load = ttk.Button(frame_presets, text = "Загрузить", command = lambda: self.load_preset(2))
        button_load.grid(row = 2, column = 2, pady = 5)

        ttk.Label(frame_presets, text = f'Пресет 4').grid(row = 3, column=0, sticky='w')
        button_save = ttk.Button(frame_presets, text = "Сохранить", command = lambda: save_preset(3, **self.get_params_dict()))
        button_save.grid(row = 3, column = 1, pady = 5)
        button_load = ttk.Button(frame_presets, text = "Загрузить", command = lambda: self.load_preset(3))
        button_load.grid(row = 3, column = 2, pady = 5)

        ttk.Label(frame_presets, text = f'Пресет 5').grid(row = 4, column=0, sticky='w')
        button_save = ttk.Button(frame_presets, text = "Сохранить", command = lambda: save_preset(4, **self.get_params_dict()))
        button_save.grid(row = 4, column = 1, pady = 5)
        button_load = ttk.Button(frame_presets, text = "Загрузить", command = lambda: self.load_preset(4))
        button_load.grid(row = 4, column = 2, pady = 5)

        help_button = ttk.Button(frame_presets, text = 'HELP', command=self.help_window)
        help_button.grid(row = 10, column = 2, pady = 50)


    
    def on_calculate(self):
        try:
            params_dict = self.get_params_dict()
            
            x, y, z = calculate_trajectory(**params_dict)
            fig = create_plot(x, y, z, params_dict)
            
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
