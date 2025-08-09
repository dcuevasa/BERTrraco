from src.ui.main_window import App
from src.config import APP_CONFIG

if __name__ == "__main__":
    app = App(
        title=APP_CONFIG["title"],
        send_queue_max_size=APP_CONFIG["queue_max_size"]
    )
    app.mainloop()