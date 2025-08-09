import tkinter as tk
import time
import random
from ..config import FACE_UI, ANIMATION_CONFIG
from .animations import run_idle_animation, animate_mouth_speak, animate_z_particles

class FaceCanvas(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, width=FACE_UI["canvas_width"], height=FACE_UI["canvas_height"], bg=FACE_UI["bg_color"])
        
        # Crear elementos visuales
        self.eye1 = self.create_oval(*FACE_UI["eye1_coords"], fill="white", outline="black", width=2)
        self.eye2 = self.create_oval(*FACE_UI["eye2_coords"], fill="white", outline="black", width=2)
        self.pupil1 = self.create_oval(*FACE_UI["pupil1_coords"], fill="black")
        self.pupil2 = self.create_oval(*FACE_UI["pupil2_coords"], fill="black")
        self.mouth = self.create_line(FACE_UI["mouth_x1"], FACE_UI["mouth_y"], FACE_UI["mouth_x2"], FACE_UI["mouth_y"], width=3)
        self.tongue = self.create_oval(*FACE_UI["tongue_coords"], fill="pink", outline="red", state='hidden')

        # Estado de la animación
        self.speaking = False
        self.sleeping = False
        self.z_particles = []
        self.last_activity_time = time.time()
        self.idle_delay = random.uniform(ANIMATION_CONFIG["idle_delay_min_s"], ANIMATION_CONFIG["idle_delay_max_s"])

        self._animation_loop()

    def _animation_loop(self):
        now = time.time()
        if self.speaking:
            self.last_activity_time = now
            animate_mouth_speak(self)
        elif self.sleeping:
            animate_z_particles(self)
        elif now - self.last_activity_time > ANIMATION_CONFIG["sleep_timeout_s"]:
            self.start_sleeping()
        elif now - self.last_activity_time > self.idle_delay:
            run_idle_animation(self)
            self.last_activity_time = now
            self.idle_delay = random.uniform(ANIMATION_CONFIG["idle_delay_min_s"], ANIMATION_CONFIG["idle_delay_max_s"])

        self.after(ANIMATION_CONFIG["interval_ms"], self._animation_loop)

    def wake_up(self):
        if self.sleeping:
            self.stop_sleeping()
        self.last_activity_time = time.time()

    def start_speaking(self):
        self.wake_up()
        self.speaking = True

    def stop_speaking(self):
        self.speaking = False
        self.last_activity_time = time.time()
        self.delete(self.mouth)
        self.mouth = self.create_line(FACE_UI["mouth_x1"], FACE_UI["mouth_y"], FACE_UI["mouth_x2"], FACE_UI["mouth_y"], width=3)
        self.reset_eyes()

    def start_sleeping(self):
        if self.speaking: return
        self.sleeping = True
        # Cerrar ojos
        self.itemconfig(self.pupil1, state='hidden')
        self.itemconfig(self.pupil2, state='hidden')
        self.coords(self.eye1, FACE_UI["eye1_coords"][0], FACE_UI["eye1_coords"][1] + 15, FACE_UI["eye1_coords"][2], FACE_UI["eye1_coords"][1] + 15)
        self.coords(self.eye2, FACE_UI["eye2_coords"][0], FACE_UI["eye2_coords"][1] + 15, FACE_UI["eye2_coords"][2], FACE_UI["eye2_coords"][1] + 15)

    def stop_sleeping(self):
        self.sleeping = False
        for z in self.z_particles: self.delete(z)
        self.z_particles = []
        self.reset_eyes()

    def reset_eyes(self):
        if self.sleeping: return
        self.coords(self.eye1, *FACE_UI["eye1_coords"])
        self.coords(self.eye2, *FACE_UI["eye2_coords"])
        self.coords(self.pupil1, *FACE_UI["pupil1_coords"])
        self.coords(self.pupil2, *FACE_UI["pupil2_coords"])
        self.itemconfig(self.pupil1, state='normal')
        self.itemconfig(self.pupil2, state='normal')