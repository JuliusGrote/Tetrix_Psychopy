import tkinter as tk

root = tk.Tk()
root.withdraw()

# create a simple class that gets all screen size parameters and calculates important scale factors based on it
class Scale:
	
	def __init__(self):
		self.screen_w, self.screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
		self.scale_factor = round((root.winfo_screenheight() / 600 - 0.1), 1)
		self.scale_font = round(46 * self.scale_factor)
		self.x_displacement = (self.screen_w -(13/15 * self.screen_h + 5)) / 2
# create a new meth
        

