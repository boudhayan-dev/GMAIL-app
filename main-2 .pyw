import os,subprocess
from tkinter import *

# process_status creates the loading screen used in between window switches .
def process_status():
    login_status=Tk()
    login_status.title(" ")
    login_status.geometry('{}x{}+{}+{}'.format(100,26, 578, 240))
    display=Label(login_status,text="Please wait ")
    display.grid()
    def test():
        current_status=display["text"]
        if current_status.endswith('. . .')==True:
            current_status='Please wait .'

        else:
            current_status+=' .'

        display['text']=current_status
        login_status.after(500,test)

    login_status.after(1,test)
    login_status.after(2500,lambda:login_status.destroy())
    login_status.mainloop()

process_status()
