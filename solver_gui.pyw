import tkinter as tk
import solver
from tkinter import messagebox
from tkinter.ttk import *
import time
import threading
#pyinstaller --onefile solver_gui.pyw --name Sudoku_Solver --icon sudoku_icon.ico

grid=[
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
]
txtboxlist=[]

def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    return("break")

def movecell(event):
    if event.keysym=='Up':
        rind,dind=0,-1
    elif event.keysym=='Down':
        rind,dind=0,1
    elif event.keysym=='Right':
        rind,dind=1,0
    elif event.keysym=='Left':
        rind,dind=-1,0
    widget=main_window.focus_get()
    r,c='',''
    for i in range(11):
        for j in range(11):
            if txtboxlist[i][j]==widget:
                r,c=i,j
                break
        if r!='' and c!='':
            break
    r+=dind
    c+=rind
    if r in [3,7]:
        r+=dind
    if c in [3,7]:
        c+=rind
    while r<0:r+=11
    while r>10:r-=11
    while c<0:c+=11
    while c>10:c-=11
    new_widget=txtboxlist[r][c]
    new_widget.focus_set()

def chnge(a):
    if a in [4,8]:
        return None
    elif a>8:return a-3
    elif a>4:return a-2
    else:return a-1

def clr_grid():
    for i in range(1,12):
        for j in range(1,12):
            r,c=chnge(i),chnge(j)
            if r!=None and c!=None:
                txtbox=txtboxlist[i-1][j-1]
                txtbox['state']='normal'
                txtbox.delete(0,'end')
    sub_button['state']='active'
    sub_button['text']='Submit'
    sub_button['bg']='red'
    lb['text']='Fill up...'
    main_window.update_idletasks()
    main_window.update()

def sol(grid,ansl):
    ansl.append(solver.main(grid))
def exc(grid):
    show()
    t=time.perf_counter()
    for i in range(1,12):
        for j in range(1,12):
            txtbox=txtboxlist[i-1][j-1]
            txt=txtbox.get()
            r,c=chnge(i),chnge(j)
            if r!=None and c!=None and txt!='':
                grid[r][c]=int(txt)
    ansl=[]
    solt=threading.Thread(target=sol(grid,ansl))
    solt.start()
    solt.join()
    ans_grid=ansl[0]
    if ans_grid=='wrong':
        messagebox.showerror(title='ERROR !!',message='Sudoku Unsolvable !!\nTry Again >>',)
        ansl=['corr']
        clr_grid()
    else:
        for i in range(1,12):
            for j in range(1,12):
                r,c=chnge(i),chnge(j)
                if r!=None and c!=None:
                    ans=ans_grid[r][c]
                    txtbox=txtboxlist[i-1][j-1]
                    txtbox.delete(0)
                    txtbox.insert(1,string=str(ans))
                    txtbox['state']='disabled'
        showtime(t)
        sub_button['text']='Done'
        sub_button['bg']='LightGreen'
        sub_button['state']='disabled'

def show():
    lb['text']='Processing...'
    main_window.update_idletasks()
    main_window.update()

def showtime(t):
    tme=time.perf_counter()-t
    lb['text']='Processing_Time: '+str(int(tme))+' s'
    main_window.update_idletasks()
    main_window.update()

if __name__=='__main__':
    main_window=tk.Tk('Sudoku Solver')
    main_window.title('---SUDOKU SOLVER---')
    #clear button
    clr_button=tk.Button(
        main_window,
        text='Clear',
        font = ("Helvetica","20","bold"),
        height=1,
        width=6,
        bg='blue', 
        fg='white',
        justify='center',
        command=clr_grid
        )
    clr_button.grid(row=13,column=3,columnspan=8)

    #Submit Button
    sub_button=tk.Button(
        main_window,
        text='Submit',
        font = ("Helvetica","20","bold"),
        height=1,
        width=6,
        bg='red', 
        fg='white',
        justify='center',
        command=lambda : exc(grid)
        )
    sub_button.grid(row=13,column=8,columnspan=8)

    #gridtxtbox
    for i in range(1,12):
        txtboxlist.append([])
        for j in range(1,12):
            txtbox=tk.Entry(
                main_window, 
                width = 2,
                justify='center',
                font=("Helvetica","30","bold"),
                )
            #navigation
            txtbox.bind('<Tab>', focus_next_window)
            txtbox.bind('<Up>',movecell)
            txtbox.bind('<Down>',movecell)
            txtbox.bind('<Left>',movecell)
            txtbox.bind('<Right>',movecell)
            if j%4==0 :
                txtbox['width']=2
                txtbox['state']='disabled'
                txtbox.configure({"disabledbackground": "black"})
            if i%4==0:
                #txtbox['height']=1
                txtbox['width']=2
                txtbox['state']='disabled'
                txtbox.configure({"disabledbackground": "black"})
                
            txtbox.grid(row=i-1,column=j-1,padx=0,pady=0)
            txtboxlist[i-1].append(txtbox)
    lb=tk.Label(
        main_window,
        text='Fill up...',
        font=("Helvetica","18","bold"),
        justify='left')
    lb.grid(row=13,column=0,columnspan=6)
    main_window.mainloop()