from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import requests
import geocoder
import bs4
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

root = Tk()
root.title('Student Management System')
root.geometry('750x550+280+50')
root.resizable(False, False)

def checkIfNum(ifNum):
	try:
		if type(int(ifNum)) == int:
			return true
		else:
			return false
	except Exception:
		return false


#main window button functions
def f1():
	root.withdraw()
	add.deiconify()

def backf1():
	add.withdraw()
	root.deiconify()

def savef1():
	try:
		if add_entRno.get().isdigit() == False:
			showerror('Invalid Entry', 'Roll number must be numbers')
			return
		elif int(add_entRno.get()) < 0:
			showerror('Invalid Entry', 'Roll number cannot be less than 0')
			return 
	except Exception:
		showerror('Invalid Entry', 'Please check Roll Number entered')
		return

	try:
		if add_entName.get().isalpha() == False:
			raise TypeError("Name must be characters")
			return
		elif len(add_entName.get()) < 2:
			showerror('Invalid Entry', 'Name cannot be less than two characters')
			return
	except TypeError as errorMsg:
		showerror('Invalid Entry', errorMsg)
		return
	except Exception:
		showerror('Invalid Entry', 'Please check name entered')
		return

	try:
		if add_entMarks.get().isdigit() == False:
			showerror('Invalid Entry', 'Marks have to be numbers only')
			return
		elif int(add_entMarks.get()) < 0 or int(add_entMarks.get()) > 100:
			showerror('Invalid Entry', 'Marks range out of bound')
			return
	except Exception:
		showerror('Invalid Entry', 'Please check marks entered')
		return

	conn = None
	try:
		conn = connect('student_manage.db')
		c = conn.cursor()
		a_rno = int(add_entRno.get())
		a_name = add_entName.get()
		a_marks = int(add_entMarks.get())
		args = (a_rno, a_name, a_marks)
		c.execute("INSERT INTO records VALUES ('%d', '%s', '%d')" %args)
		conn.commit()
		showinfo('Successfull', 'Record Inserted')
		add_entRno.delete(0, END)
		add_entName.delete(0, END)
		add_entMarks.delete(0, END)
		add_entRno.focus()

	except ValueError as ve:
		conn.rollback()
		showinfo('Issue', ve)
	except TypeError as te:
		conn.rollback()
		showinfo('Issue', te)
	except Exception as e:
		conn.rollback()
		showerror('Issue', 'Please re-check all values')
	finally:
		if conn is not None:
			conn.close()

def f2():
	root.withdraw()
	view.deiconify()
	view_scroll.delete(1.0, END)
	conn = None
	try:
		conn = connect('student_manage.db')
		c = conn.cursor()
		c.execute("SELECT * from records")
		student_data = c.fetchall()
		view_info = ""
		for d in student_data:
			view_info += " Roll: " + str(d[0]) + "    |" +"    Name: " + str(d[1]) + "    |" + "    Marks: " + str(d[2]) + "\n"
		view_scroll.insert(INSERT, view_info)
	except Exception as e:
		conn.rollback()
		showerror('Issue:', e)
	finally:
		if conn is not None:
			conn.close()

def backf2():
	view.withdraw()
	root.deiconify()

def f3():
	root.withdraw()
	update.deiconify()

def backf3():
	update.withdraw()
	root.deiconify()

def savef3():
	try:
		if update_entRno.get().isdigit() == False:
			showerror('Invalid Entry', 'Roll number has to be a number')
			return
		elif int(update_entRno.get()) < 0:
			showerror('Invalid Entry', 'Roll number has to be greater than 0')
			return
	except Exception:
		showerror("Issue", "Please check roll number entered")
		return

	try:
		if update_entName.get().isalpha() == False:
			showerror('Invalid Entry','Name must be characters')
			return
		elif len(update_entName.get()) < 2:
			showerror('Invalid Entry', 'Name cannot be less than two characters')
			return
	except Exception:
		showerror('Invalid Entry', 'Please check name entered')
		return
	
	try:
		if update_entMarks.get().isdigit() == False:
			showerror('Invalid Entry', 'Marks must be numbers')
			return
		elif int(update_entMarks.get()) < 0 or int(update_entMarks.get()) > 100:
			showerror('Invalid Entry', 'Marks range out of bound')
			return
	except Exception:
		showerror('Invalid Entry', 'Please check marks entered')
		return

	conn = None
	try:
		conn = connect('student_manage.db')
		c = conn.cursor()
		#c.execute("CREATE TABLE records (rno int primary key, name text, marks int)")
		u_rno = int(update_entRno.get())
		u_name = update_entName.get()
		u_marks = int(update_entMarks.get())

		args1 = (u_name, u_rno)
		args2 = (u_marks, u_rno)
		c.execute("UPDATE records SET name = '%s' WHERE rno = '%r'" %args1)
		c.execute("UPDATE records SET marks = '%d' WHERE rno = '%r'" %args2)
		if c.rowcount >= 1:
			conn.commit()
			showinfo('Successfull', 'Record Updated.')
		else:
			showerror('Invalid','Roll Number not found.')
		update_entRno.delete(0, END)
		update_entName.delete(0, END)
		update_entMarks.delete(0, END)
	except Exception as e:
		conn.rollback()
		showinfo('Issue', e)
	finally:
		if conn is not None:
			conn.close()

def f4():
	root.withdraw()
	delete.deiconify()

def backf4():
	delete.withdraw()
	root.deiconify()

def savef4():
	try:
		if delete_entRno.get().isdigit() == False:
			showerror('Invalid Entry', 'Please enter a valid roll number')
			return
	except:
		showerror('Invalid Entry', 'Please check roll number entered')

	conn = None
	try:
		conn = connect('student_manage.db')
		c = conn.cursor()
		d_rno = int(delete_entRno.get())
		args = (d_rno)
		c.execute("DELETE FROM records where rno = '%r' " %args)
		if c.rowcount >= 1:
			conn.commit()
			showinfo('Successfull', 'Record Deleted.')
		else:
			showerror('Invalid', 'Record does not exist.')
		delete_entRno.delete(0, END)
	except Exception as e:
		conn.rollback()
	finally:
		if c is not None:
			conn.close()

#charts
def f5():
	root.withdraw()
	charts.deiconify()
	global name
	global marks
	global roll
	roll, name, marks = [], [], []
	conn = None
	try:
		conn = connect('student_manage.db')
		c = conn.cursor()
		c.execute("SELECT * from records")
		global student_data
		student_data = []
		student_data = c.fetchall()
		for d in student_data:
			roll.append(d[0])
			name.append(d[1])
			marks.append(d[2])
	except Exception as e:
		conn.rollback()
		showerror('Issue:', e)
	finally:
		if conn is not None:
			conn.close()

def backf5():
	charts.withdraw()
	root.deiconify()

def stat_all():
	student_sort_data = []
	student_sort_data = sorted(student_data, key = lambda x: x[2])
	sort_roll, sort_name, sort_marks = [], [], []
	for d in student_sort_data:
		sort_roll.append(d[0])
		sort_name.append(d[1])
		sort_marks.append(d[2])

	x = np.arange(len(name))
	plt.bar(x, marks, label = 'Marks', width=0.30)
	plt.title('Roll wise student statistics')
	plt.xticks(x, name)
	plt.xlabel('Names(Roll No. wise)')
	plt.ylabel('Marks')
	plt.grid()
	plt.show()

def stat_marks():
	student_sort_data = []
	student_sort_data = sorted(student_data, key = lambda x: x[2])
	sort_roll, sort_name, sort_marks = [], [], []
	for d in student_sort_data:
		sort_roll.append(d[0])
		sort_name.append(d[1])
		sort_marks.append(d[2])

	x = np.arange(len(sort_name))
	plt.bar(x, sort_marks, label = 'Marks', width=0.30)
	plt.title('Marks wise student statistics')
	plt.xticks(x, sort_name)
	plt.xlabel('Names')
	plt.ylabel('Marks')
	plt.grid()
	plt.show()

def stat_top5():
	student_sort_data = []
	student_sort_data = sorted(student_data, key = lambda x: x[2])
	sort_roll, sort_name, sort_marks = [], [], []
	for d in student_sort_data:
		sort_roll.append(d[0])
		sort_name.append(d[1])
		sort_marks.append(d[2])

	x = np.arange(len(sort_name[:6:-1]))
	plt.bar(x, sort_marks[:6:-1], label = 'Marks', width=0.30)
	plt.title('Marks wise student statistics')
	plt.xticks(x, sort_name[:6:-1])
	plt.xlabel('Names')
	plt.ylabel('Marks')
	plt.grid()
	plt.show()

#temperatute___________
try:
    res = requests.get('http://api.openweathermap.org/data/2.5/weather?units=metric&q=mumbai&appid=690fcb568a6b860f86779a36859e09ad')
    data = res.json()
    temp_data = data['main']
    temp_str = 'Temp: ' + str(temp_data['temp']) + '°C' + ',\n' + 'Pressure: ' + str(temp_data['pressure']) + ' millibars' + ',\n' + 'Humidity:' + str(temp_data['humidity']) + '%'

except OSError as e:
    print('Connection issue,',e)

#location__________
g = geocoder.ip('me')
current_lat = g.latlng[0]
current_lon = g.latlng[1]
try:
    coord = str(current_lat) + ',' + str(current_lon)
    a1 = 'http://open.mapquestapi.com/geocoding/v1/reverse?key=BzJD8BdYYiSfdYv4ePWAmdPYHB4Y8c8s&location='
    a2 = coord
    a3 = '&includeRoadMetadata=true&includeNearestIntersection=true'
    req = requests.get(a1 + a2 + a3)
#parameters --> street, adminArea5, adminArea3, adminArea1, postalCode
    data_rgeocode = req.json()
    results = data_rgeocode['results']
    result_dict = results[0]
    locations = result_dict['locations']
    locations_dict = locations[0]

    current_location = locations_dict['street'] + ',\n'+ locations_dict['adminArea5'] + ',\n' + locations_dict['adminArea3'] + ', ' + locations_dict['adminArea1'] + ',\n' + str(locations_dict['postalCode']) + '.'
except Exception as e:
    print('Error 404', 'Make sure you are connected to internet.')

#quote of the day starts__________
res = requests.get('https://www.brainyquote.com/quote_of_the_day')
soup = bs4.BeautifulSoup(res.text, 'lxml')
qotd_data = soup.find('img', {'class':'p-qotd'})
qotd_text = qotd_data['alt']


#main window_____GUI_____
btnAdd = Button(text='ADD', font=('britannicbold', 16, 'bold'), command=f1)
btnView = Button(text='VIEW', font=('britannicbold', 16, 'bold'), command=f2)
btnUpdate = Button(text='UPDATE', font=('britannicbold', 16, 'bold'), command=f3)
btnDelete = Button(text='DELETE', font=('britannicbold', 16, 'bold'), command=f4)
btnCharts = Button(text='CHARTS', font=('britannicbold', 16, 'bold'), command=f5)

btnAdd.config(width=10,)
btnView.config(width=10)
btnUpdate.config(width=10)
btnDelete.config(width=10)
btnCharts.config(width=10)

btnAdd.pack(pady=10)
btnView.pack(pady=10)
btnUpdate.pack(pady=10)
btnDelete.pack(pady=10)
btnCharts.pack(pady=10)

#location, temp and quote of the day
lblLoc = Label(root, text='LOCATION', font=('timesnewroman', 14, 'bold', 'underline'))
lblLoc.place(x='75', y='300')

loc_lbl = Label(root, text = current_location, font=('timesnewroman', 12))
loc_lbl.place(x='50', y='330')

lblTemp = Label(root, text='STATS', font=('timesnewroman', 14, 'bold', 'underline'))
lblTemp.place(x='570', y='300')

temp_lbl = Label(root, text=temp_str, font=('timesnewroman', 12))
temp_lbl.place(x='520', y='330')

lblQOTD = Label(root, text='Quote Of The Day', font=('impact', 16, 'underline'))
lblQOTD.place(x='300', y='460')

qotd_lbl = Label(root, text=qotd_text, font=('oldenglishtextmt', 12))
qotd_lbl.place(x='15', y='500')

#Add topLevel__________
add = Toplevel(root)
add.title('Add Student')
add.geometry('750x550+280+50')

add_lblRno = Label(add, text='Enter Roll ', font=('britannicbold', 16, 'bold'))
add_entRno = Entry(add, font=('britannicbold', 16))
add_lblName = Label(add, text='Enter Name ', font=('britannicbold', 16, 'bold'))
add_entName = Entry(add, font=('britannicbold', 16))
add_lblMarks = Label(add, text='Enter Marks ', font=('britannicbold', 16, 'bold'))
add_entMarks = Entry(add, font=('britannicbold', 16))

add_lblRno.pack(pady=10)
add_entRno.pack(pady=10)
add_lblName.pack(pady=10)
add_entName.pack(pady=10)
add_lblMarks.pack(pady=10)
add_entMarks.pack(pady=10)

add_btnSave = Button(add, text='Save', font=('britannicbold', 16, 'bold'), command=savef1)
add_btnBack = Button(add, text='Back', font=('britannicbold', 16, 'bold'), command= backf1)

add_btnSave.pack(pady=10)
add_btnBack.pack(pady=10)

add.withdraw()

#View toplevel__________
view = Toplevel()
view.title('View Students Details')
view.geometry('750x550+280+50')

view_scroll = ScrolledText(view, width = 40, height= 10, font=('britannicbold', 14, 'bold'))
view_scroll.pack(pady = 10)

view_btnBack= Button(view, text='Back', font=('britannicbold', 16, 'bold'), command= backf2)
view_btnBack.pack(pady = 10)
view.withdraw()

#Update toplevel()__________
update = Toplevel()
update.title('Update Student Details')
update.geometry('750x550+280+50')

update_lblRno = Label(update, text='Enter Roll ', font=('britannicbold', 16, 'bold'))
update_entRno = Entry(update, font=('britannicbold', 16))
update_lblName = Label(update, text='Enter New Name ', font=('britannicbold', 16, 'bold'))
update_entName = Entry(update, font=('britannicbold', 16))
update_lblMarks = Label(update, text='Enter New Marks ', font=('britannicbold', 16, 'bold'))
update_entMarks = Entry(update, font=('britannicbold', 16))

update_lblRno.pack(pady=10)
update_entRno.pack(pady=10)
update_lblName.pack(pady=10)
update_entName.pack(pady=10)
update_lblMarks.pack(pady=10)
update_entMarks.pack(pady=10)

update_btnSave = Button(update, text='Save', font=('britannicbold', 16, 'bold'), command=savef3)
update_btnBack = Button(update, text='Back', font=('britannicbold', 16, 'bold'), command= backf3)

update_btnSave.pack(pady=10)
update_btnBack.pack(pady=10)
update.withdraw()

#Delete toplevel()__________
delete = Toplevel()
delete.title('Delete Student Details')
delete.geometry('750x550+280+50')

delete_lblRno = Label(delete, text='Enter Roll ', font=('britannicbold', 16, 'bold'))
delete_lblRno.pack(pady=10)

delete_entRno = Entry(delete, font=('britannicbold', 16))
delete_entRno.pack(pady=10)

delete_btnSave = Button(delete, text='Save', font=('britannicbold', 16, 'bold'), command=savef4)
delete_btnBack = Button(delete, text='Back', font=('britannicbold', 16, 'bold'), command= backf4)

delete_btnSave.pack(pady=10)
delete_btnBack.pack(pady=10)
delete.withdraw()

#charts toplevel__________
charts = Toplevel()
charts.title('Statistics')
charts.geometry('450x250+440+120')

charts_all = Button(charts, text='All Students', font=('britannicbold', 16), command=stat_all)
charts_marks = Button(charts, text='Marks wise', font=('britannicbold', 16), command= stat_marks)
charts_top5 = Button(charts, text='Top 5 Students', font=('britannicbold', 16), command= stat_top5)
charts_back = Button(charts, text='Back', font=('britannicbold', 16), command= backf5)

charts_all.config(width=13)
charts_marks.config(width=13)
charts_top5.config(width=13)

charts_all.pack(pady=10)
charts_marks.pack(pady=10)
charts_top5.pack(pady=10)
charts_back.pack(pady=10)

charts.withdraw()

current_time = dt.datetime.now()
hour = current_time.hour
if hour > 12 and hour < 17:
	showinfo('Greetings', 'Good Afternoon fellow user!')
elif hour >= 17:
	showinfo('Greetings', 'Good Evening fellow user!')
else:
	showinfo('Greetings', 'Good Morning fellow user!')

root.mainloop()