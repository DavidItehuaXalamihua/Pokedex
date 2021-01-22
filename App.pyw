import tkinter as tk
import defs
import MainFrame

defs.textPrettier()

root = tk.Tk()
App = MainFrame.Aplicacion(root)
root.mainloop()