from tkinter import *
from PIL import ImageTk, Image
import smtplib,sys,time,os
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox,filedialog
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import subprocess

smtpObj=""
window2=""
attachments=[]#attachment list1
index=""#attchment index
emailLogin=""
emailPass=""

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

'''sendMail() is used to send the email.
Multipart is used to create an email object with attachments and other relevant parts .
"attachments" contains the list of attachments with their absolute path.'''

def SendMail():
    try:
        subprocess.Popen(['pythonw.exe',resource_path("backend.pyw")])

        msg = MIMEMultipart()
        msg['Subject'] = subject_var.get()
        msg['From'] = emailLogin
        msg['To'] = to_var.get()
        print("to ",msg['To'])
        text=(e3.get(1.0,END)).strip()

        text = MIMEText(text)
        msg.attach(text)
        for attachment in attachments:
            attachment=attachment.split('/')
            attachment='//'.join(attachment)
            img_data = open(attachment , 'rb').read()
            image = MIMEApplication(img_data, Name=os.path.basename(attachment))
            image['Content-Disposition']='attachment; filename="%s"' % os.path.basename(attachment)
            msg.attach(image)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(emailLogin , emailPass)
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        s.quit()

        window3.after(4000,lambda:window3.destroy())
        send_success=Tk()
        send_success.title(" ")    
        send_success.attributes("-toolwindow",1)
        send_success.geometry('{}x{}+{}+{}'.format(300,30, 578, 210))
        lab=Label(send_success,text="Message sent successfully.").pack()
        send_success.after(4000,lambda:send_success.destroy())
        send_success.mainloop()
    except:
        send_fail=Tk()
        send_fail.title(" ")
        send_fail.attributes("-toolwindow",1)
        send_fail.geometry('{}x{}+{}+{}'.format(300,30, 578, 210))
        lab=Label(send_fail,text="Message failed to send.Please try again.").pack()
        send_fail.after(4000,lambda:send_fail.destroy())
        send_fail.mainloop()

'''login() is used to validate the login details entered.
based on the correctness of the login details provided , respective message are displayed.
If incorrect , the program requests for another try. If succeeded , it progresses to the next window.'''

def login():
    global smtpObj
    try:
        subprocess.Popen(['pythonw.exe',resource_path("backend.pyw")])

        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(login_text.get(), password_text.get())
        global emailLogin
        emailLogin=login_text.get()
        global emailPass
        emailPass=password_text.get()
        window.after(2000,lambda:window.destroy())
        
        login_success=Tk()
        login_success.title(" ")
        login_success.geometry('{}x{}+{}+{}'.format(30,30, 578, 240))
        l5=Label(login_success,text="LOGIN Successful")
        l5.grid(row=0,column=3)
        login_success.after(3000,lambda:login_success.destroy())
        login_success.mainloop()

    except:
        login_fail=Tk()
        login_fail.title(" ")
        login_fail.geometry('{}x{}+{}+{}'.format(30,30, 578, 240))
        l5=Label(login_fail,text="LOGIN failed.")
        l5.grid(row=0,column=3)
        login_fail.after(3000,lambda:login_fail.destroy())
        login_fail.mainloop()

#on_closing() is just a minute modification to the tkinter window .
#It just allows the user to reconsider before force closing the window.
def on_closing():
     if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit()

#validate() is used to permit/reject the possible attachments to be added.
def validate(string):
    accepted_extensions=["jpg","png","bmp","py","mp3","wmv","mp4","avi","flv","txt","pdf"]
    for extensions in accepted_extensions:
        if (string.lower()).endswith(extensions):
            return(1)

#browsefunc() is used to update the list of valid attachments and display on the listbox provided.
def browsefunc():
    flag=0
    filename = filedialog.askopenfilename()
    flag=validate(filename)
    if flag==1:
        attachments.append(filename)
        list1.insert(END,str(os.path.basename(filename)+'\n'))

#delete_attach() is used to delete an attachment by the user from the already added list.
def delete_attach():
    rowVal=list1.get(index)
    list1.delete(index)
    for i in attachments:
        if os.path.basename(i).strip()==rowVal.strip():
            attachments.remove(i)
    list1.update_idletasks()


def get_index(event):
    global index
    index=list1.curselection()[0]

def repeat():
    choice.destroy()

def terminate():
    choice.destroy()
    sys.exit()

#greet_window creates the WELCOME screen on startup.
greet_window=Tk()
greet_window.overrideredirect(1)
greet_window.geometry('{}x{}+{}+{}'.format(350, 300, 520, 210))

img=Image.open("TROPICANA.jpg")
img= img.resize((350,300), Image.ANTIALIAS)
img= ImageTk.PhotoImage(img)
back_ground=Label(greet_window,image=img,width=350,height=300)
back_ground.grid(row=0,column=0,columnspan=6,rowspan=9)

greet_window.after(3000,lambda:greet_window.destroy())
greet_window.mainloop()

#window creates the LOGIN screen.
window=Tk()
window.title("LOGIN")
window.attributes("-toolwindow",1)
window.geometry('{}x{}+{}+{}'.format(250, 200, 520, 210))
window.protocol("WM_DELETE_WINDOW", on_closing)

img0=Image.open("back.JPG")
img0= img0.resize((250,200), Image.ANTIALIAS)
img0= ImageTk.PhotoImage(img0)
back_ground=Label(window,image=img0,width=250,height=200)
back_ground.grid(row=0,column=0,columnspan=6,rowspan=9)

l2=Label(window,text="LOGIN:",width=9,height=1,anchor="w",bg="Yellow",fg="Black")
l2.grid(row=2,column=0)

login_text=StringVar()
e1=Entry(window,textvariable=login_text,width=29)
e1.grid(row=2,column=1,columnspan=2)

l3=Label(window,text="PASSWORD:",width=9,height=1,anchor="w",bg="Yellow",fg="Black")
l3.grid(row=4,column=0)

password_text=StringVar()
e2=Entry(window,show="*",textvariable=password_text,width=29)
e2.grid(row=4,column=1,columnspan=2)

l4=Button(window,text="SUBMIT",command=login,anchor="w",bg="Yellow",fg="Black")
l4.grid(row=8,column=1)
# On clicking the SUBMIT button , the 'login()' function is accessed.

window.mainloop()

'''The following code creates the email typing space .
It also allows the user to type in multiple e-mails consecutively by asking for user's permission after sending each mails.'''
while True:
    window3=Tk()
    window3.title("COMPOSE")
    window3.attributes("-toolwindow",1)
    window3.geometry('{}x{}+{}+{}'.format(300, 400, 578, 138))
    window3.protocol("WM_DELETE_WINDOW", on_closing)

    img0=Image.open("back.JPG")
    img0= img0.resize((300,400), Image.ANTIALIAS)
    img0= ImageTk.PhotoImage(img0)
    back_ground=Label(window3,image=img0,width=300,height=400)
    back_ground.grid(row=0,column=0,columnspan=8,rowspan=15)

    l1=Label(window3,text="To:",anchor='w',width=7,bg="Yellow",fg="Black")
    l1.grid(row=1,column=0)

    to_var=StringVar()
    e1=Entry(window3,width=35,textvariable=to_var)
    e1.grid(row=1,column=1,columnspan=5)

    l3=Label(window3,text="Subject:",anchor='w',width=7,bg="Yellow",fg="Black")
    l3.grid(row=3,column=0)

    subject_var=StringVar()
    e2=Entry(window3,width=35,textvariable=subject_var)
    e2.grid(row=3,column=1,columnspan=5)

    l5=Label(window3,text="Body:",anchor='w',width=7,bg="Yellow",fg="Black")
    l5.grid(row=5,column=0)

    e3=ScrolledText(window3,width=24,height=13)
    e3.grid(row=5,column=1,rowspan=6,columnspan=4)

    b1=Button(window3,text="Attach",anchor="w",command=browsefunc,bg="yellow")
    b1.grid(row=10,column=0)

    list1=Listbox(window3,width=13,height=6)
    list1.grid(row=11,column=0,columnspan=1)
    list1.bind("<<ListboxSelect>>",get_index)

    sb1=Scrollbar(window3)
    sb1.grid(row=11,column=1,sticky=W)
    list1.configure(yscrollcommand=sb1.set)
    sb1.configure(command=list1.yview)

    img2=Image.open("send.JPG")
    img2 = img2.resize((50,30), Image.ANTIALIAS)
    img2= ImageTk.PhotoImage(img2)

    e4=Button(window3,image=img2,command=SendMail)
    e4.grid(row=11,column=4,columnspan=2)

    b1=Button(window3,text="Delete",anchor="w",command=delete_attach,bg="yellow")
    b1.grid(row=12,column=0)

    window3.mainloop()
    
    # choice window determines whether to exit or continue with another mail.
    choice=Tk()
    choice.title(" ")
    choice.geometry('{}x{}+{}+{}'.format(205, 55, 578, 138))
    l1=Label(choice,text="Do you want to send another e-mail ?")
    l1.grid(row=0,column=0,columnspan=2)
    b1=Button(choice,text="YES",width=10,command=repeat)
    b1.grid(row=1,column=0)
    b2=Button(choice,text="NO",width=10,command=terminate)
    b2.grid(row=1,column=1)
    choice.mainloop()
