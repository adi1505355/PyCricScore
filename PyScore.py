import sys
import time
from tkinter import *
import bs4 as bs
import urllib.request
from threading import Thread
from win10toast import ToastNotifier #here i had to pip win10toast

toaster = ToastNotifier()
root = Tk()

root.title("PyScore-Get it Live")
root.geometry("600x600")
root.configure(background="#a1dbcd")

theLabel=Label(root,text="Enter the match name",font=("consolas", 20))
theLabel.pack()

theLabe2=Label(root,text="Enter teams name in X vs Y where first letters of X and Y format are Uppercase",font=("consolas", 20))
theLabe2.pack(padx=10,pady=10)

fr1=Frame(root,bd=5,relief=SUNKEN)
fr1.pack(padx=10,pady=10)

M=Text(fr1, height=10, width=40)
M.pack(fill=X, side="left",ipady=5)

button1=Button(fr1, text="Get Score" ,fg="red" , font=15)
button1.pack(side="right", padx=20)



txt = Frame( width=70, height=115)
txt.pack(pady=25)


txt.grid_rowconfigure(0, weight=1)
txt.grid_columnconfigure(0, weight=1)


T = Text(txt, borderwidth=3, relief="sunken")
T.config(font=("consolas", 12), wrap='word')
T.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)





def getstr():
    T.config(state=NORMAL)
    T.delete("1.0",END)
    T.insert(END, "Connecting to ESPN Cricinfo Servers.... ")
    T.config(state=DISABLED)
    s = M.get("1.0",'end-1c')

    s=s.split()
    ge=0

    while(1):

        sauce=urllib.request.urlopen('http://www.espncricinfo.com/ci/engine/match/index.html?view=live').read()
        soup=bs.BeautifulSoup(sauce,'lxml')
        for divy in soup.find_all('section',class_="default-match-block"):
            a1=divy.a
            a2=a1['href']

            a2=a2.split('/')
            a3=a2[-2]
            a3=a3.split('-')

            ct=0
            for i in s:
                if i in a3:
                    ct=ct+1
            if(ct!=(len(s))):
                ge=1
            else:

                button1.config(text="Exit")

                T.config(state=NORMAL)
                T.delete("1.0",END)
                T.config(state=DISABLED)

                T.config(state=NORMAL)
                T.insert(END, 'For Match :')
                T.insert(END, s)
                T.insert(END, '\n')
                T.yview(END)
                T.config(state=DISABLED)


                di=divy.find('div',class_="innings-info-1")
                T.config(state=NORMAL)
                T.insert(END, di.text)
                T.yview(END)
                st=di.text

                di2=divy.find('div',class_="innings-info-2")
                T.config(state=NORMAL)
                T.insert(END, di2.text)
                T.yview(END)
                T.config(state=DISABLED)
                st=st+di2.text


                di3=divy.find('div',class_="match-status")
                T.config(state=NORMAL)
                T.insert(END, di3.text)
                T.yview(END)
                T.config(state=DISABLED)

                def dispscore(ok,st):
                    toaster.show_toast("Score is",st,duration=5)
                by="temp"
                t2=Thread(target=dispscore, args=(by,st))
                t2.start()
                ge=0
                break
        def abc():
            break
        button1.config(command=abc)


        if(ge==1):
            button1.config(text="Exit")
            button1.config(command=root.quit)
            T.config(state=NORMAL)
            T.delete("1.0",END)
            T.insert(END, 'Match Not Found, kindly restart app and try again')
            T.yview(END)
            T.config(state=DISABLED)
            break
        time.sleep(30)


def getstr_while():
        t3=Thread(target=getstr, args=())
        t3.daemon = True
        t3.start()


def getscore():
    button1.config(command=getstr_while)

t1=Thread(target=getscore, args=())
t1.start()

root.mainloop()
