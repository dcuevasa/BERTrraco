import tkinter as tk
from tkinter import scrolledtext
import queue
import threading
import time

from ..app_logic import chat_loop, audio_loop
from .face_canvas import FaceCanvas

class App(tk.Tk):
    def __init__(self, title="Asistente", send_queue_max_size=10):
        super().__init__()
        self.title(title)

        self.message_queue = queue.Queue(maxsize=send_queue_max_size)
        self.audio_queue = queue.Queue()

        # --- UI Setup ---
        self.face_canvas = FaceCanvas(self)
        self.face_canvas.pack()

        self.chat_display = scrolledtext.ScrolledText(self, state='disabled', height=8, width=50, wrap=tk.WORD)
        self.chat_display.pack(padx=10, pady=5, fill="both", expand=True)

        input_frame = tk.Frame(self)
        input_frame.pack(padx=10, pady=5, fill="x")
        self.input_entry = tk.Entry(input_frame, width=40)
        self.input_entry.pack(side=tk.LEFT, fill="x", expand=True)
        self.input_entry.bind("<Return>", self.send_message)
        send_button = tk.Button(input_frame, text="Enviar", command=self.send_message)
        send_button.pack(side=tk.RIGHT)
        
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._start_threads()

    def send_message(self, event=None):
        msg = self.input_entry.get()
        if msg.strip():
            self.message_queue.put(msg)
            self._display_message("Tú", msg)
            self.input_entry.delete(0, tk.END)

    def _display_message(self, sender, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)

    def start_assistant_message(self):
        self.after(0, self._insert_text, "Asistente: ")

    def append_assistant_message(self, chunk):
        self.after(0, self._insert_text, chunk)

    def end_assistant_message(self):
        self.after(0, self._insert_text, "\n")

    def _insert_text(self, text):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, text)
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)

    def wake_up(self):
        self.face_canvas.wake_up()

    def start_speaking(self):
        self.face_canvas.start_speaking()

    def stop_speaking(self):
        self.face_canvas.stop_speaking()

    def start_waiting(self):
        self.face_canvas.start_waiting()

    def stop_waiting(self):
        self.face_canvas.stop_waiting()

    def _start_threads(self):
        threading.Thread(target=chat_loop, args=(self, self.message_queue, self.audio_queue), daemon=True).start()
        threading.Thread(target=audio_loop, args=(self.audio_queue,), daemon=True).start()

    def _on_closing(self):
        self.message_queue.put(None)
        self.destroy()