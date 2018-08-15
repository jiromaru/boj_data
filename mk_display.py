##############################データ選択画面の作成##############################

from tkinter import *
from tkinter import ttk

def mk_display(dict):

    param_list=[]
    select_list=[]

    def show_selection():
        for i in lb.curselection():
            select_list.append(lb.get(i).replace("\\u",""))
        print("選択項目 : ")
        if len(select_list)!=0:
            print(select_list)
        root.destroy()

    root = Tk()
    root.title('Scrollbar')

    # Frame
    frame1 = ttk.Frame(root, padding=10)
    frame1.grid()

    # Listbox
    lb = Listbox(frame1,selectmode=EXTENDED,height=20,width=170)
    lb.grid(row=0, column=0)
    for key in dict.keys():
        lb.insert(END, key)

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame1,orient=VERTICAL,command=lb.yview)
    lb['yscrollcommand'] = scrollbar.set
    scrollbar.grid(row=0,column=1,sticky=(N,S))

    #Button
    button1 = ttk.Button(frame1, text='OK', command=show_selection)
    button1.grid(row=1, column=0, columnspan=2)

    root.mainloop()

    for selected in select_list:
        param_list.append(dict[selected])

    return param_list
