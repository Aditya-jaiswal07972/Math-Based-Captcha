import random
from tkinter import *
from tkinter.ttk import *
import random
import string
from tkinter import Tk, Label, Entry, Button, END
from PIL import ImageTk, Image
from captcha.image import ImageCaptcha


class MathCaptcha:
    def __init__(self):
        root = Tk() #root Tkinter
        self.actual = str(random.randint(0, 9)) + \
            self.randOps()+str(random.randint(0, 9))
        print(self.actual)
  #For generating random string of mathmatical expression 
        image = ImageCaptcha(fonts=['captcha.ttf'])
  #Font for captcha
        data = image.generate(self.actual) 
        image.write(self.actual, "out.png")
  #Output image of captcha
        photo = PhotoImage(file=r"out.png")
        Button(root, text="Submit", image=photo).pack(side=TOP)
 #Putting image of captcha in tkinter 
        Label(root, text="Enter the captcha:").pack(side=TOP)
        self.captchaInput = Entry(root)
        self.captchaInput.pack(side=TOP)
        Button(root, text="Submit", command=self.submit).pack(side=TOP)
        mainloop()

    def randOps(self):
        ops = ('+', '-', '*', '/')
        return random.choice(ops) #For choosingrandom operator the list as String 

    def submit(self):
        if(int(self.captchaInput.get()) == eval(self.actual)): 
  #eval() converts returns the output of mathematical expression  
            print("Captcha Verified")
        else:
            print("Incorrect Captcha")
