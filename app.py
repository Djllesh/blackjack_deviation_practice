import tkinter as tk
from controller.controller import AppController
from ui.main_window import MainWindow

if __name__ == "__main__":
    root = tk.Tk()
    controller = AppController()
    main_window = MainWindow(root, controller)
    root.mainloop()
