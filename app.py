from tkinter import *
import tkinter.font as font
from tkinter import messagebox
import backend
import socket

#Gui programming starts here
splash = Tk()
splash.title("WELCOME")
splash.geometry("550x500+650+250")
splash.call('wm', 'iconphoto', splash._w, PhotoImage(file = 'hello.png'))
arial = font.Font(family = 'Arial', size = 16, weight = 'bold')
ariel = font.Font(family = 'Arial', size = 26, weight = 'bold')

try:
	socket.create_connection(("www.google.com",80))
	lblqotd = Label(text = "QOTD", font = arial)
	lblqotd.pack(fill = X)

	quote = backend.qotd()
	txtqotd = Text(splash, wrap = WORD, height = 10, font = arial)
	txtqotd.pack(fill = X, ipady = 10)
	txtqotd.insert(END, quote)

	lblcity = Label(text = "City Name", font = arial)
	lblcity.pack(fill = X)

	city_name = backend.city()
	txtcity = Text(splash, wrap = WORD, height = 1, font = arial)
	txtcity.tag_configure("center", justify='center')
	txtcity.pack(fill = X, ipady = 10)
	txtcity.insert(END, city_name)
	txtcity.tag_add("center", "1.0", "end")

	lbltemp = Label(text = "Temperature (in Celsius)", font = arial)
	lbltemp.pack(fill = X)
	temperature = str(backend.temp())
	if temperature.isdigit():
		h = 1
	else:
		h = 2
	txttemp = Text(splash, wrap = WORD, height = h, font = arial)
	txttemp.tag_configure("center", justify='center')
	txttemp.pack(fill = X, ipady = 10)
	txttemp.insert(END, temperature)
	txttemp.tag_add("center", "1.0", "end")
except OSError:
	txtcity = Text(splash, wrap = WORD, font = ariel)
	txtcity.tag_configure("center", justify='center')
	txtcity.pack(fill = X)
	txtcity.insert(END, "\n\n\n\n\nNo Internet Connection")
	txtcity.tag_add("center", "1.0", "end")

splash.after(5000, splash.destroy)
splash.mainloop()

root = Tk()
root.geometry("400x412+750+350")
root.title("Menu")
root.call('wm', 'iconphoto', root._w, PhotoImage(file = 'icon.png'))
arial = font.Font(family = 'Arial', size = 16, weight = 'bold')


def add_window():
	add = Toplevel(root)
	add.title("ADD")
	add.geometry("400x350+750+350")

	def add_command():
		rno_add_string = rno_add.get()
		name_add_string = name_add.get()
		if rno_add_string.isdigit() and all(x.isalpha() or x.isspace() for x in name_add_string):
			backend.insert(rno_add.get(), name_add.get())
			messagebox.showinfo("DONE","Entry Added")

			entrno.delete(0, END)
			entname.delete(0, END)
		else:
			if not rno_add_string.isdigit():
				messagebox.showerror("Invalid Input", "Roll No. should only contain poitive numbers")
			if not all(x.isalpha() or x.isspace() for x in name_add_string):
				messagebox.showerror("Invalid Input", "Name should only conatin Alphabets")	

	lblrno = Label(add, text = "Roll No.", font = arial)
	lblrno.pack(ipady = 16)

	rno_add = StringVar()
	entrno = Entry(add, textvariable = rno_add, font = arial, bd = 6)
	entrno.pack()

	lblname = Label(add, text = 'Name', font = arial)
	lblname.pack(ipady = 16)

	name_add = StringVar()
	entname = Entry(add, textvariable = name_add, font = arial, bd = 6)
	entname.pack()

	btnsave = Button(add, text = "Save", width = 16, font = arial, command = add_command)
	btnsave.pack(pady = (26,0))

	btnback = Button(add, text = "Back", width = 16, font = arial, command = lambda:add.withdraw())
	btnback.pack()


def view_window():
	view = Toplevel(root)
	view.title("VIEW")
	view.geometry("515x650+750+250")

	liststudents = Listbox(view, width = 40, height = 100, font = arial)
	liststudents.pack(side = LEFT)

	sbstudents = Scrollbar(view)
	sbstudents.pack(side = LEFT, ipadx = 10,fill = 'y')

	liststudents.configure(yscrollcommand = sbstudents.set)
	sbstudents.configure(command = liststudents.yview)

	liststudents.delete(0, END)
	student_view = []
	for row in backend.view():
		student_view.append([row[0], row[1]])

	student_view.sort(key = lambda x: x[0])

	liststudents.insert(END, ' Roll No.      Name')
	for i in student_view:
		liststudents.insert(END, i[0] + "    " + i[1])


def delete_window():
	delete = Toplevel(root)
	delete.title("DELETE")
	delete.geometry("515x650+750+250")

	def get_selected_row(event):
		try:
			global selected_row
			global selected_row_rno
			global selected_row_name
			index = liststudents.curselection()[0]
			selected_row = liststudents.get(index)
			selected_row_rno=""
			for i in range(len(selected_row)):
				if selected_row[i]!=" ":
					selected_row_rno = selected_row_rno+selected_row[i]
				else:
					break

			selected_row_name=selected_row[i+4:]
			#print(selected_row, selected_row_rno, selected_row_name)
			entrno.delete(0, END)
			entrno.insert(END, selected_row_rno)
		except IndexError:
			pass


	def delete_command():
		deletion = []
		for row in backend.view():
			deletion.append(row[0])

		if rno_delete.get() in deletion: 
			backend.delete(rno_delete.get())
			messagebox.showinfo("DONE","Entry Deleted")

			entrno.delete(0, END)
			liststudents.delete(0, END)
			student_view = []
			for row in backend.view():
				student_view.append([row[0], row[1]])

			student_view.sort(key = lambda x: x[0])

			liststudents.insert(END, ' Roll No.      Name')
			for i in student_view:
				liststudents.insert(END, i[0] + "    " + i[1])
		else:
			messagebox.showerror("Student not found","Please enter valid Roll No.")

	liststudents = Listbox(delete, width = 40, height = 16, font = arial)
	liststudents.grid(row = 0, column = 0)

	sbstudents = Scrollbar(delete)
	sbstudents.grid(row = 0, column = 1, ipady = 175, ipadx = 10)

	liststudents.configure(yscrollcommand = sbstudents.set)
	sbstudents.configure(command = liststudents.yview)

	liststudents.delete(0, END)
	student_view = []
	for row in backend.view():
		student_view.append([row[0], row[1]])

	student_view.sort(key = lambda x: x[0])

	liststudents.insert(END, ' Roll No.      Name')
	for i in student_view:
		liststudents.insert(END, i[0] + "    " + i[1])
	
	lblrno = Label(delete, text = "Roll No.", font = arial)
	lblrno.grid(ipady = 16)

	rno_delete = StringVar()
	entrno = Entry(delete, textvariable = rno_delete, font = arial, bd = 6)
	entrno.grid()

	btndelete = Button(delete, text = "Delete", width = 16, font = arial, command = delete_command)
	btndelete.grid(pady = (26,0))

	btnback = Button(delete, text = "Back", width = 16, font = arial, command = lambda: delete.withdraw())
	btnback.grid()

	liststudents.bind('<<ListboxSelect>>', get_selected_row)


def update_window():
	update = Toplevel(root)
	update.title("UPDATE")
	update.geometry("515x650+750+250")

	def get_selected_row(event):
		try:
			global selected_row
			global selected_row_rno
			global selected_row_name
			index = liststudents.curselection()[0]
			selected_row = liststudents.get(index)
			selected_row_rno=""
			for i in range(len(selected_row)):
				if selected_row[i]!=" ":
					selected_row_rno = selected_row_rno+selected_row[i]
				else:
					break

			selected_row_name=selected_row[i+4:]
			#print(selected_row, selected_row_rno, selected_row_name)
			entrno.delete(0, END)
			entrno.insert(END, selected_row_rno)
			entname.delete(0, END)
			entname.insert(END, selected_row_name)
		except IndexError:
			pass

	def update_command():
		rno_update_string = rno_update.get()
		name_update_string = name_update.get()
		updation_rno = []
		for row in backend.view():
			updation_rno.append(row[0])

		if rno_update.get() in updation_rno and rno_update_string.isdigit() and all(x.isalpha() or x.isspace() for x in name_update_string):
			backend.update(rno_update.get(), name_update.get())
			messagebox.showinfo("DONE","Entry Updated")

			entrno.delete(0, END)
			entname.delete(0, END)
			liststudents.delete(0, END)
			student_view = []
			for row in backend.view():
				student_view.append([row[0], row[1]])

			student_view.sort(key = lambda x: x[0])

			liststudents.insert(END, ' Roll No.      Name')
			for i in student_view:
				liststudents.insert(END, i[0] + "    " + i[1])
		else:
			if rno_update.get() not in updation_rno:
				messagebox.showerror("Student not found","Please enter valid details")
			if not rno_update_string.isdigit():
				messagebox.showerror("Invalid Input", "Roll No. should only contain poitive numbers")
			if not all(x.isalpha() or x.isspace() for x in name_update_string):
				messagebox.showerror("Invalid Input", "Name should only conatin Alphabets")	


	liststudents = Listbox(update, width = 40, height = 12, font = arial)
	liststudents.grid(row = 0, column = 0)

	sbstudents = Scrollbar(update)
	sbstudents.grid(row = 0, column = 1, ipady = 120, ipadx = 10)

	liststudents.configure(yscrollcommand = sbstudents.set)
	sbstudents.configure(command = liststudents.yview)

	liststudents.delete(0, END)
	student_view = []
	for row in backend.view():
		student_view.append([row[0], row[1]])

	student_view.sort(key = lambda x: x[0])

	liststudents.insert(END, ' Roll No.      Name')
	for i in student_view:
		liststudents.insert(END, i[0] + "    " + i[1])
	
	lblrno = Label(update, text = "Roll No.", font = arial)
	lblrno.grid(ipady = 16)

	rno_update = StringVar()
	entrno = Entry(update, textvariable = rno_update, font = arial, bd = 6)
	entrno.grid()

	lblname = Label(update, text = 'Name', font = arial)
	lblname.grid(ipady = 16)

	name_update = StringVar()
	entname = Entry(update, textvariable = name_update, font = arial, bd = 6)
	entname.grid()

	btnupdate = Button(update, text = "Update", width = 16, font = arial, command = update_command)
	btnupdate.grid(pady = (26,0))

	btnback = Button(update, text = "Back", width = 16, font = arial, command = lambda: update.withdraw())
	btnback.grid()

	liststudents.bind('<<ListboxSelect>>', get_selected_row)


btnadd = Button(root, text ="Add", width = 32, font = arial, command = add_window)
btnadd.pack(ipady = 32)

btnview = Button(root, text = 'View', width = 32, font = arial, command = view_window)
btnview.pack(ipady = 32)

btnupdate = Button(root, text = 'Update', width = 32, font = arial, command = update_window)
btnupdate.pack(ipady = 32)

btndelete = Button(root, text = 'Delete', width = 32, font = arial, command = delete_window)
btndelete.pack(ipady = 32)

root.mainloop()
