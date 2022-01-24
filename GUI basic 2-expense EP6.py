from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย  by Puyeyh')
GUI.geometry('700x700+200+0')

# B1 = Button(GUI,text='Hello')
# B1.pack(ipadx=20,ipady=20)   

##############MENU######################
menubar = Menu(GUI)
GUI.config(menu=menubar)

# file menu
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')

# help
def About():
    messagebox.showinfo('About','สีจร้ากูว่าแล้วมึงต้องอ่าน\nอิอิอิอิอิอิอิ')

helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)
# Donate
donatemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu)




##########################################



Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1)

icon_t1 = PhotoImage(file='t1_expense.png')
icon_t2 = PhotoImage(file='t2_expenselist.png')


Tab.add(T1, text=f'{"ค่าใช้จ่าย":^{30}}',image=icon_t1,compound='top')
Tab.add(T2, text=f'{"ค่าใช้จ่ายทั้งหมด":^{30}}',image=icon_t2,compound='top')

F1 = Frame(T1)
F1.pack()

days = {'Mon':'จันทร์',
        'Tue':'อังคาร',
        'Med':'พุธ',
        'Thu':'พฤหัสบดี',
        'Fri':'ศุกร์',
        'Sat':'เสาร์',
        'Sun':'อาทิตย์'}

def Save(event=None):
    expense = v_expense.get()
    price = v_price.get()
    quantity = v_quantity.get()

    if expense == '':
        print('No Data')
        messagebox.showwarning('Error','กรุณากรอกข้อมูลค่าใช้จ่าบ')
        return
    elif price == '':    
        messagebox.showwarning('Error','กรุณากรอกราคา')
        return
    elif quantity == '':
         messagebox.showwarning('Error','กรุณากรอกจำนวน')  
         return  


    #total = float(price) * float(quantity)
    try:
        total = float(price) * float(quantity)
        print('รายการ: {} ราคา: {}'.format(expense,price))
        print('จำนวน: {} รวมทั้งหมด: {} บาท' .format(quantity,total))
        text = 'รายการ: {} ราคา: {} บาท \n'.format(expense,price)
        text = text + 'จำนวน: {} รวมทั้งหมด: {} บาท'.format(quantity,total)
        v_result.set(text)
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')

        today = datetime.now().strftime('%a') # days['Mon'] = 'จันทร์'
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dt = days[today] + '-' + dt
        with open('savedata.csv','a',encoding='utf-8',newline='') as f:
                  # with คือการเปิดไฟล์แล้วปิด auto
                  # 'a' การบันทึกเรื่อยๆ เพิ่อ ข้อมูล
                  fw = csv.writer(f)#สร้างฟังชั่นสำหรับเขียนข้อมูล
                  data = [dt,expense,price,quantity,total]
                  fw.writerow(data)
        E1.focus()
        update_table()      
    except:
         print('ERROR')
         messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')    
         v_expense.set('')
         v_price.set('')
         v_quantity.set('')


GUI.bind ('<Return>',Save)              

FONT1 = (None,20) # None เปลี่ยนเป็น 'Angsana New'

#------image-----

main_icon = PhotoImage(file='icon_money.png')

Mainicon = Label(F1,image=main_icon)
Mainicon.pack()


#text1
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1).pack()
v_expense = StringVar()
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()             

#text2
L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1).pack()
v_price = StringVar()
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()

#text3
L = ttk.Label(F1,text='จำนวน (ชิ้น)',font=FONT1).pack()
v_quantity = StringVar()
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1)
E3.pack()

icon_b1 = PhotoImage(file='b_save.png')

B2 = ttk.Button(F1,text='Save',image=icon_b1,compound='left',command=Save)
B2.pack(ipadx=50,ipady=20,pady=20)

v_result = StringVar()
v_result.set('-----ผลลัพธ์------')
result = ttk.Label(F1, textvariable=v_result,font=FONT1,foreground='green')
result.pack(pady=20)

#################TAB2########################

def read_csv():
    with open('savedata.csv',newline='',encoding='utf-8') as f:
        fr = csv.reader(f)
        data = list(fr)
    return data     
        # print(data)
        # print('---------------------')
        # print(data[0])

#table
L = ttk.Label(T2,text='ตารางแสดงผลลัพท์ทั้งหมด',font=FONT1).pack(pady=20)

header = ['วัน-เวลา','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=20)
resulttable.pack()


for h in header:
    resulttable.heading(h,text=h)

headerwidth = [150,170,80,80]        
for h,w in zip(header,headerwidth):
    resulttable.column(h,width=w)

def update_table():
    # for c in resulttable.get_children():
    #     resulttable.delete(c)
    resulttable.delete(*resulttable.get_children())
    data = read_csv()
    for d in data:
        resulttable.insert('',0,value=d)

update_table()
print('GET CHILD:',resulttable.get_children())


GUI.bind('<Tab>',lambda x: E2.focus())
GUI.mainloop()
