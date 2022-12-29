
import sys
import tkinter
import tkinter.filedialog
import os
from PIL import ImageGrab,Image
from time import sleep
import os



class ScreenShot:

    def __init__(self):
        self.flag = True
        self.root = tkinter.Tk()

    def start(self):

        tmp_file_name = 'tmp.png'

        # full screen
        im = ImageGrab.grab()
        # im.show()
        im.save(tmp_file_name)
        im.close()

        # self.root = tkinter.Tk()

        # minimize tk window
        self.root.state('icon')
        self._doStart(tmp_file_name)
        os.remove(tmp_file_name)
        self.root.mainloop()

    def _doStart(self, tmp_file_name):

        # record mouse's coordinates

        self.X = tkinter.IntVar(value=0)

        self.Y = tkinter.IntVar(value=0)


        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()

        self.top = tkinter.Toplevel(self.root, width=screenWidth, height=screenHeight)
        self.top.overrideredirect(True)
        self.top.lift()
        self.top.attributes('-topmost', True)
        self.top.attributes('-topmost', False)
        self.canvas = tkinter.Canvas(self.top, bg='white', width=screenWidth, height=screenHeight)

        self.image = tkinter.PhotoImage(file=tmp_file_name)
        self.canvas.create_image(screenWidth // 2, screenHeight // 2, image=self.image)

        # when left button is hold pressed
        def _onLeftButtonDown(event):
            self.X.set(event.x)
            self.Y.set(event.y)
            # start screenshot
            if self.flag:
                self.sel = True

        self.canvas.bind('<Button-1>', _onLeftButtonDown)

        # hold left mouse button to show the captured area
        def _onLeftButtonMove(event):

            if not self.sel or not self.flag:
                return

            global lastDraw
            try:

                # delete the image
                self.canvas.delete(lastDraw)

            except Exception:
                pass

            lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='black',width=1.5,fill='')

        self.canvas.bind('<B1-Motion>', _onLeftButtonMove)

        # left mouse button releases
        def _onLeftButtonUp(event):
            def save():
                self.sel = False
                try:
                    # hide the button
                    yes_btn.destroy()
                    no_btn.destroy()
                    self.canvas.delete(lastDraw)
                except:
                    pass

                left, right = sorted([self.X.get(), event.x])
                top, bottom = sorted([self.Y.get(), event.y])
                pic = ImageGrab.grab((left + 1, top + 1, right, bottom))
                # saving window pops
                fileName = tkinter.filedialog.asksaveasfilename(title='save screenshot',
                                                                filetypes=[('image', '*.jpg *.png')])
                if fileName:
                    pic.save(fileName)
                # shut down window
                self.top.destroy()
                self.root.destroy()
                self.flag=True

            if self.flag:
                self.flag=False
                yes_btn = tkinter.Button(self.canvas, text='✔', width=1, height=1,command=save)
                yes_btn.place(x=(self.X.get() + event.x) / 2, y=event.y)
                # if click no button, shut down the window
                no_btn = tkinter.Button(self.canvas, text='✖', width=1, height=1,command=_quit)
                no_btn.place(x=(self.X.get() + event.x) / 2+17,y=event.y)

        def _quit():
            self.sel = False
            self.top.destroy()
            self.root.destroy()
            try:
                self.canvas.delete(lastDraw)
            except:
                pass
            self.flag=True

        self.canvas.bind('<ButtonRelease-1>', _onLeftButtonUp)

        # canvas fills the window with adaptive size
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)



