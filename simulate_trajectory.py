import numpy as np
import plotly.graph_objects as go
from tkinter import messagebox

def calculate_trajectory(v0, theta, phi, wind_speed, wind_direction,
                        mass, diameter, air_density, gravity):

    if theta < 0 or theta >= 90 or v0 <= 0 or v0 >= 3*10**8 or mass <= 0 or diameter <= 0 or air_density < 0 or gravity <= 0:
        messagebox.showerror("Ошибка", "Проверьте правильность введенных данных")
        return

    try:
        C_drag = 0.47
        S = np.pi * (diameter/2)**2
        
        theta_rad = np.radians(theta)
        phi_rad = np.radians(phi)
        wind_dir_rad = np.radians(wind_direction)
        
        vx = v0 * np.sin(theta_rad) * np.cos(phi_rad)
        vy = v0 * np.sin(theta_rad) * np.sin(phi_rad)
        vz = v0 * np.cos(theta_rad)        
        wind_x = wind_speed * np.cos(wind_dir_rad)
        wind_y = wind_speed * np.sin(wind_dir_rad)
        
        x, y, z = [0], [0], [0]
        t = 0
        if v0 <= 10000:
            dt = 1/v0
        else:
            dt = 1/10000
        
        while t < 30 and z[-1] >= 0:
            if x[-1] > 10**5 or y[-1] > 10**5 or z[-1] > 10**5:
                break
            v_rel_x = vx - wind_x
            v_rel_y = vy - wind_y
            v_rel_z = vz
            speed_rel = np.sqrt(v_rel_x**2 + v_rel_y**2 + v_rel_z**2)
            
            if speed_rel > 0:
                drag = 0.5 * air_density * C_drag * S * speed_rel**2
                ax = -drag * v_rel_x / (mass * speed_rel)
                ay = -drag * v_rel_y / (mass * speed_rel)
                az = -gravity - drag * v_rel_z / (mass * speed_rel)
            else:
                ax, ay, az = 0, 0, -gravity
            
            vx += ax * dt
            vy += ay * dt
            vz += az * dt
            
            x.append(round((x[-1] + vx * dt), 5))
            y.append(round((y[-1] + vy * dt), 5))
            z.append(round((z[-1] + vz * dt), 5))
            t += dt
        
        return x, y, z
        
    except Exception:
        messagebox.showerror("Ошибка", f"Произошла ошибка при рассчете траектории: {Exception}")
        return None, None, None

def create_plot(x, y, z, params):
    if None in (x, y, z):
        return None
        
    fig = go.Figure()
    
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(width=4, color='red'),
        name='Траектория'
    ))
    
    fig.add_trace(go.Surface(
        z=[[0, 0], [0, 0]],
        x=[[min(x), max(x)], [min(x), max(x)]],
        y=[[min(y), min(y)], [max(y), max(y)]],
        colorscale='Greens',
        opacity=0.5,
        showscale=False
    ))
    
    fig.update_layout(
        scene=dict(
            xaxis_title='X (м)',
            yaxis_title='Y (м)',
            zaxis_title='Z (м)',
            aspectmode='data'
        ),
        title=f"Траектория снаряда (v₀={params['v0']} м/с, θ={params['theta']}°)\nМаксимальная высота H = {max(z)}"
    )
    
    return fig







