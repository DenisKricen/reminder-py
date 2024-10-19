from tkinter import *
import sqlite3
from datetime import *
from tkcalendar import Calendar
import plyer

conn=sqlite3.connect('reminder/reminder_db.sql')
cursor=conn.cursor()

def check_events():
    for event_date,eve_n in (cursor.execute('SELECT date,event_name FROM events').fetchall()):
        my_date=datetime.strptime(str(event_date),'%d.%m.%Y')
        if my_date.strftime('%Y-%m-%d')==str(date.today()):
            print('SUCCSESS')
            plyer.notification.notify(
                message="Don't forgive about your event!",
                title=f'{eve_n}')

check_events()

def window():   

    def create_new_event():

        def submit():
            try:
                if not(fould_name.get() and cal_date):   #choose_date.get()
                    raise NameError
                cursor=conn.cursor()

                cursor.execute(f"INSERT INTO events VALUES( '{fould_name.get()}', '{cal_date}', '{var.get()}' )")  #choose_date.get()
                ev=cursor.execute('SELECT * FROM events')
                print(ev.fetchall())
                
                conn.commit()
                #conn.close()

                suc=Label(event_menu,text='COMPLITED',bg='green')
                suc.place(x=(300-170)/2,y=110,width=170,height=40)

            except sqlite3.IntegrityError:
                err=Label(event_menu,text='THIS NAME IS ALREADY TAKEN',bg='red')
                err.place(x=(300-170)/2,y=110,width=170,height=40)
            except sqlite3.Error as error:
                err=Label(event_menu,text='ERROR',bg='red')
                err.place(x=(300-170)/2,y=110,width=170,height=40)
            except NameError:
                err=Label(event_menu,text='FOULDERS MUST BE ENTIRED',bg='red')
                err.place(x=(300-170)/2,y=110,width=170,height=40)

            fould_name.delete(0,END)
            #choose_date.delete(0,END)

        def calendar():
            def inst_date():
                global cal_date
                cal_date=cal.get_date()
                root.destroy()
            root=Toplevel()
            root.title('Calendar')
            #root.resizable(False,False)

            cal=Calendar(root,selectmode='day')
            sub=Button(root,text='OK',command=inst_date)

            cal.pack()
            sub.pack()

        event_menu=Toplevel()
        event_menu.title('Create New Event')
        event_menu.geometry('300x180+200+70')
        event_menu.resizable(False,False)

        event_menu.image=PhotoImage(file=r'reminder\images\bd_300x180.png')

        event_fon=Label(event_menu,image=event_menu.image)
        event_fon.place(x=0,y=0)

        var=StringVar()
        var.set('medium')

        lab_name=Label(event_menu,text='NAME: ')
        lab_date=Label(event_menu,text='DATE: ')
        lab_importance=Label(event_menu,text='IMPORTANCE: ')

        radio_butts=Frame(event_menu,bg='red')
        fould_name=Entry(event_menu)
        choose_date=Button(event_menu,text='Choose date',command=calendar,width=17)
        rbutt_low=Radiobutton(radio_butts,text='heigh',variable=var,value='heigh')
        rbutt_medium=Radiobutton(radio_butts,text='medium',variable=var,value='medium')
        rbutt_heigh=Radiobutton(radio_butts,text='low',variable=var,value='low')
        create_butt=Button(event_menu,text='Create',command=submit,width=20)

        lab_name.grid()
        lab_date.grid()
        lab_importance.grid()
        fould_name.grid(row=0,column=1)
        choose_date.grid(row=1,column=1)
        rbutt_low.grid(row=0,column=0)
        rbutt_medium.grid(row=0,column=1)
        rbutt_heigh.grid(row=0,column=2)
        radio_butts.grid(row=2,column=1)
        create_butt.place(x=(300-170)/2,y=70,width=170,height=40)

    def del_event():
        del_menu=Toplevel()
        del_menu.title('Delete Event')
        del_menu.geometry('300x180+200+370')
        del_menu.resizable(False,False)
        del_menu.image=PhotoImage(file=r'reminder\images\bd_300x180.png')

        del_fon=Label(del_menu,image=del_menu.image)
        del_fon.place(x=0,y=0)

        def del_event():
            try:
                if not (fould_name.get()):
                    raise NameError
                
                cursor=conn.cursor()
                if not (cursor.execute(f"SELECT * FROM events WHERE event_name = '{fould_name.get()}'").fetchall()):
                    raise TypeError
                cursor.execute(f"DELETE FROM events WHERE event_name = '{fould_name.get()}'")
                ev=cursor.execute('SELECT * FROM events')
                print(ev.fetchall())
                
                conn.commit()
                #conn.close()

                suc=Label(del_menu,text='COMPLITED',bg='green')
                suc.place(x=(300-170)/2,y=110,width=170,height=40)

            except sqlite3.Error as error:
                err=Label(del_menu,text='ERROR',bg='red')
                err.place(x=(300-170)/2,y=110,width=170,height=40)
            except NameError:
                err=Label(del_menu,text='FOULDER MUST BE ENTIRED',bg='red')
                err.place(x=(300-170)/2,y=110,width=170,height=40)
            except TypeError:
                err=Label(del_menu,text='NO SUCH EVENT IN DIARY',bg='red')
                err.place(x=(300-170)/2,y=110,width=170,height=40)

        def del_all_events():
            try:
                cursor=conn.cursor()
                if not (cursor.execute(f"SELECT * FROM events").fetchall()):
                    raise TypeError
                cursor.execute(f"DELETE FROM events;")
                ev=cursor.execute('SELECT * FROM events;')
                print(ev.fetchall())
                
                conn.commit()
                #conn.close()

                suc=Label(del_menu,text='COMPLITED',bg='green')
                suc.place(x=(300-170)/2,y=110,width=170,height=40)

            # except sqlite3.Error as error:
            #     err=Label(del_menu,text='ERROR',bg='red')
            #     err.place(x=(300-170)/2,y=110,width=170,height=40)
            except TypeError:
                err=Label(del_menu,text='DIARY IS ALREADY EMPTY',bg='red')
                err.place(x=(300-170)/2,y=110,width=170,height=40)

        fould_name=Entry(del_menu)
        del_butt=Button(del_menu,text='Delete event',command=del_event)
        del_all_butt=Button(del_menu,text='Delete all events',command=del_all_events)

        fould_name.grid()
        del_butt.grid()
        del_all_butt.grid()

    def check_events():
        cursor=conn.cursor()
        
        ev=cursor.execute('SELECT * FROM events')
        event_list=StringVar(value=ev.fetchall())
        my_events=Listbox(listvariable=event_list,selectmode=SINGLE)
        scroll_bar_y=Scrollbar(command=my_events.yview)
        scroll_bar_x=Scrollbar(command=my_events.xview,orient=HORIZONTAL)
        my_events.configure(yscrollcommand=scroll_bar_y.set,xscrollcommand=scroll_bar_x.set)
        
        conn.commit()

        my_events.place(x=90,y=200,width=220,height=250)
        scroll_bar_y.place(x=300,y=200,height=250)
        scroll_bar_x.place(x=90,y=185,width=220)
        #conn.close()

    butt_width= 120
    butt_height=20

    root=Tk()
    root.title('Reminder')
    root.geometry('400x600+600+70')
    root.resizable(False,False)
    root.image=PhotoImage(file=r'reminder\images\bd_400x600.png')
    
    fon=Label(root,image=root.image)
    create_event=Button(text='Create new event',command=create_new_event)
    delete_event=Button(text='Delete event',command=del_event)
    check_all_events=Button(text='Check my events',command=check_events)

    fon.grid()
    create_event.place(x=(400-butt_width)/2,y=20,width=butt_width,height=butt_height)
    delete_event.place(x=(400-butt_width)/2,y=50,width=butt_width,height=butt_height)
    check_all_events.place(x=(400-butt_width)/2,y=80,width=butt_width,height=butt_height)

    root.mainloop()

window()

