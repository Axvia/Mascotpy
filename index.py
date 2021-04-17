import tkinter as tk
from tkinter import PhotoImage, Canvas, Label, Menu
from PIL import ImageTk, ImageSequence, Image
import os, sys
import mouse
global x, y


# Moving bordeless window
def standard_bind():
   app.bind('<B1-Motion>', lambda e: event(e, Mode=True))

def event(widget, Mode=False):
    global x, y
    if Mode:
        x = widget.x
        y = widget.y
    app.bind('<B1-Motion>', lambda e: event(e))
    app.geometry('+%d+%d' % (mouse.get_position()[0]-x, mouse.get_position()[1]-y))


# Provide relative path to file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
# End


# Window
app = tk.Tk()
app.attributes('-topmost', True)
app.overrideredirect(True)
app.wm_attributes('-transparentcolor','black')
app.resizable(width=False, height=False)
app.config(highlightbackground='black')
# End



# # Function Animation
# def animate(counter):
#     canvas.itemconfig(image, image=sequence[counter])
#     app.after(50, lambda: animate((counter+1) % len(sequence)))
# # End

# # Animate
# canvas = Canvas(app, bd=0, highlightthickness=0)
# canvas.grid(row=1,column=2)
# sequence = [ImageTk.PhotoImage(img)
#                     for img in ImageSequence.Iterator(
#                         Image.open(resource_path("paimon.gif")))]
# img = Image.open(resource_path("paimon.gif"))
# width, height = img.size
# canvas.config(width=width, height=height)
# image = canvas.create_image(width/2, height/2, image=sequence[0])
# animate(1)
# # End


class MyLabel(Label):
    def __init__(self, master, filename):
        im = Image.open(filename)
        seq =  []
        try:
            while 1:
                seq.append(im.copy())
                im.seek(len(seq)) # skip to next frame
        except EOFError:
            pass # we're done

        try:
            self.delay = im.info['duration']
        except KeyError:
            self.delay = 100

        first = seq[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]

        Label.__init__(self, master, image=self.frames[0])

        lut = [1] * 256
        lut[im.info["transparency"]] = 0

        temp = seq[0]
        for image in seq[1:]:
            mask = image.point(lut, "1")
            temp.paste(image, None, mask) #paste with mask
            frame = temp.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))

        self.idx = 0
        self.cancel = self.after(1000, self.play)

    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)   

anim = MyLabel(app, resource_path("paimon.gif"))
anim.pack()

app.geometry('199x233')
app.bind('<B1-Motion>', lambda e: event(e, Mode=True))
app.bind('<ButtonRelease-1>', lambda e: standard_bind())

# Right click menu
def exitApp():
	sys.exit(1)
def my_popup(e):
	my_menu.tk_popup(e.x_root, e.y_root)
my_menu = Menu(app, tearoff=False)
my_menu.add_command(label="exit", command=exitApp)
app.bind("<Button-3>", my_popup)

# Window
app.mainloop()
# End