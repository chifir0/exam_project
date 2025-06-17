import os

def save_preset(i, v0, theta, phi, wind_speed, wind_direction,
                        mass, diameter, air_density, gravity, dt_param):
    
    file_path = os.path.join(os.path.dirname(__file__), "preset_data.txt")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    new_preset = f'{v0} {theta} {phi} {wind_speed} {wind_direction} {mass} {diameter} {air_density} {gravity} {dt_param}'   
    lines[i] = new_preset.rstrip('\n') + '\n'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

