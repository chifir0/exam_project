import tkinter as tk
from tkinter import ttk
from simulate_trajectory import calculate_trajectory, create_plot
import webbrowser

class TrajectoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Моделирование траектории снаряда")
        self.setup_ui()
        
    def setup_ui(self):
        frame_params = ttk.LabelFrame(self.root, text="Параметры", padding=10)
        frame_params.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        self.entries = {} # сюда все параметры
        params = [
            ('v0', 'Начальная скорость (м/с):', '50'),
            ('theta', 'Угол θ (°):', '45'),
            ('phi', 'Угол φ (°):', '0'),
            ('wind_speed', 'Скорость ветра (м/с):', '10'),
            ('wind_dir', 'Направление ветра (°):', '90'),
            ('mass', 'Масса снаряда (кг):', '1.0'),
            ('diameter', 'Диаметр снаряда (м):', '0.1'),
            ('air_density', 'Плотность воздуха (кг/м³):', '1.2'),
            ('gravity', 'Гравитация (м/с²):', '9.81')
        ]
        
        for i, (name, label, default) in enumerate(params):
            ttk.Label(frame_params, text=label).grid(row=i, column=0, sticky="w")
            entry = ttk.Entry(frame_params)
            entry.grid(row=i, column=1, pady=5)
            entry.insert(0, default)
            self.entries[name] = entry
        
        btn_calculate = ttk.Button(frame_params, 
                                text="Рассчитать траекторию", 
                                command=self.on_calculate)
        btn_calculate.grid(row=len(params), column=0, columnspan=2, pady=10)
    
    def on_calculate(self):
        try:
            params = {
                'v0': float(self.entries['v0'].get()),
                'theta': float(self.entries['theta'].get()),
                'phi': float(self.entries['phi'].get()),
                'wind_speed': float(self.entries['wind_speed'].get()),
                'wind_direction': float(self.entries['wind_dir'].get()),
                'mass': float(self.entries['mass'].get()),
                'diameter': float(self.entries['diameter'].get()),
                'air_density': float(self.entries['air_density'].get()),
                'gravity': float(self.entries['gravity'].get())
            }
            
            x, y, z = calculate_trajectory(**params)
            fig = create_plot(x, y, z, params)
            
            if fig:
                html_file = "trajectory_plot.html"
                fig.write_html(html_file)
                webbrowser.open(html_file)
                
        except Exception as e:
            print(f"Ошибка ввода данных: {e}") # ЧТО-ТО ВЫВЕСТИ

if __name__ == "__main__":
    root = tk.Tk()
    app = TrajectoryApp(root)
    root.mainloop()
