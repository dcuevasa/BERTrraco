import random
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