import random
import math
from ..config import FACE_UI

# --- Animaciones de Habla y Sueño ---
def animate_mouth_speak(face_canvas):
    offset = random.randint(-5, 5)
    if face_canvas.type(face_canvas.mouth) == 'line':
        face_canvas.delete(face_canvas.mouth)
        face_canvas.mouth = face_canvas.create_oval(
            FACE_UI["mouth_x1"] + offset, FACE_UI["mouth_y"],
            FACE_UI["mouth_x2"] - offset, FACE_UI["mouth_open_height"],
            fill="black"
        )
    else:
        face_canvas.delete(face_canvas.mouth)
        face_canvas.mouth = face_canvas.create_line(
            FACE_UI["mouth_x1"], FACE_UI["mouth_y"],
            FACE_UI["mouth_x2"], FACE_UI["mouth_y"], width=3
        )
        face_canvas.reset_eyes()

def animate_z_particles(face_canvas):
    if random.random() < 0.1:
        z_id = face_canvas.create_text(FACE_UI["canvas_width"] - 30, FACE_UI["mouth_y"] - 20, text="Z", font=("Arial", 12))
        face_canvas.z_particles.append(z_id)
    
    to_remove = [z for z in face_canvas.z_particles if face_canvas.coords(z)[1] < 0]
    for z in face_canvas.z_particles: face_canvas.move(z, -1, -2)
    for z in to_remove:
        face_canvas.delete(z)
        face_canvas.z_particles.remove(z)

# --- Animación de Espera (Tuerca) ---
def run_waiting_animation(face_canvas):
    """Anima una tuerca rotando sobre su propio eje cerca del centro."""
    if face_canvas.sleeping or not face_canvas.is_waiting: return

    # Parámetros de la tuerca
    center_x = FACE_UI["canvas_width"] / 2
    center_y = FACE_UI["canvas_height"] / 2 - 40 # Un poco arriba del centro
    radius = 20
    
    # Crear la tuerca (un hexágono)
    nut_id = face_canvas.create_polygon(
        _get_hexagon_points(center_x, center_y, radius),
        fill="gray", outline="black", width=2, tags="waiting_animation"
    )
    face_canvas.lift(nut_id) # Dibujar por encima de todo

    _animate_nut_step(face_canvas, nut_id, center_x, center_y, radius, 0)

# --- Animación de Puntos de Carga ---
def run_dots_animation(face_canvas):
    """Crea e inicia la animación de los puntos de carga."""
    if face_canvas.sleeping or not face_canvas.is_waiting: return

    center_x = FACE_UI["canvas_width"] / 2
    dot_y = FACE_UI["canvas_height"] / 2 # Debajo del centro de la tuerca
    
    dot_radius = 3
    dot_spacing = 15

    dot_ids = []
    for i in range(3):
        x = center_x + (i - 1) * dot_spacing
        dot_id = face_canvas.create_oval(
            x - dot_radius, dot_y - dot_radius,
            x + dot_radius, dot_y + dot_radius,
            fill="black", state='hidden', tags="waiting_animation"
        )
        dot_ids.append(dot_id)
    
    _animate_dots_step(face_canvas, dot_ids, 0)

def _animate_dots_step(face_canvas, dot_ids, step):
    """Gestiona un paso de la animación de los puntos."""
    if not face_canvas.is_waiting:
        return

    num_dots = len(dot_ids)
    state = step % (num_dots + 2) # 0,1,2=mostrar puntos; 3=pausa; 4=ocultar
    
    if state < num_dots:
        if face_canvas.exists(dot_ids[state]):
            face_canvas.itemconfig(dot_ids[state], state='normal')
        delay = 300
    elif state == num_dots:
        delay = 400 # Pausa con todos los puntos visibles
    else: # state == num_dots + 1
        for dot_id in dot_ids:
            if face_canvas.exists(dot_id):
                face_canvas.itemconfig(dot_id, state='hidden')
        delay = 400 # Pausa con todos los puntos ocultos

    face_canvas.after(delay, _animate_dots_step, face_canvas, dot_ids, step + 1)

def _get_hexagon_points(cx, cy, radius):
    """Calcula los 6 vértices de un hexágono centrado en (cx, cy)."""
    points = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.pi / 180 * angle_deg
        points.append((cx + radius * math.cos(angle_rad), cy + radius * math.sin(angle_rad)))
    return points

def _animate_nut_step(face_canvas, nut_id, cx, cy, radius, angle):
    """Rota la tuerca un paso sobre su eje."""
    if not face_canvas.is_waiting or not face_canvas.exists(nut_id):
        return

    # Rotar
    new_angle = angle - 15 

    # Calcular nuevos puntos y actualizar polígono
    # No es necesario recalcular los puntos base ya que no se mueve
    base_points = _get_hexagon_points(cx, cy, radius)
    rotated_points = _rotate_points(base_points, cx, cy, new_angle)
    
    face_canvas.coords(nut_id, *sum(rotated_points, ()))
    face_canvas.after(25, _animate_nut_step, face_canvas, nut_id, cx, cy, radius, new_angle)

def _rotate_points(points, cx, cy, angle_deg):
    """Rota una lista de puntos alrededor de un centro (cx, cy)."""
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    rotated = []
    for x, y in points:
        tx = x - cx
        ty = y - cy
        new_x = (tx * cos_a - ty * sin_a) + cx
        new_y = (tx * sin_a + ty * cos_a) + cy
        rotated.append((new_x, new_y))
    return rotated

# --- Animaciones de Ocio (Idle) ---
def _blink(face_canvas, duration=50):
    if face_canvas.sleeping: return
    face_canvas.itemconfig(face_canvas.pupil1, state='hidden')
    face_canvas.itemconfig(face_canvas.pupil2, state='hidden')
    face_canvas.coords(face_canvas.eye1, FACE_UI["eye1_coords"][0], FACE_UI["eye1_coords"][1] + 15, FACE_UI["eye1_coords"][2], FACE_UI["eye1_coords"][1] + 15)
    face_canvas.coords(face_canvas.eye2, FACE_UI["eye2_coords"][0], FACE_UI["eye2_coords"][1] + 15, FACE_UI["eye2_coords"][2], FACE_UI["eye2_coords"][1] + 15)
    face_canvas.after(duration, face_canvas.reset_eyes)

def _look_around(face_canvas):
    if face_canvas.sleeping: return
    dx, dy = random.randint(-10, 10), random.randint(-5, 5)
    face_canvas.move(face_canvas.pupil1, dx, dy)
    face_canvas.move(face_canvas.pupil2, dx, dy)
    face_canvas.after(random.randint(700, 1500), face_canvas.reset_eyes)

def run_idle_animation(face_canvas):
    """Elige y ejecuta una animación de ocio aleatoria."""
    animations = [_blink, _look_around]
    weights = [0.8, 0.2]
    chosen_animation = random.choices(animations, weights)[0]
    chosen_animation(face_canvas)