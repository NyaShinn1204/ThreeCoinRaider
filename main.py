import data.icon as get_icon
import tkinter as tk 
root = tk.Tk() 
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(data=get_icon.get_window_icon()))
root.mainloop()
