import tkinter as tk
import MySQLdb
from tkinter import messagebox
from mainWindow import *

class singUpWindow():
	def __init__(self, window = None):
		self.window = tk.Toplevel(window)
		self.window.geometry('350x200')
		self.window.title('Sign Up Window')

		self.new_name = tk.StringVar()
		tk.Label(self.window, text='User name: ').place(x=10, y= 10)
		self.entry_new_name = tk.Entry(self.window, textvariable=self.new_name)
		self.entry_new_name.place(x=150, y=10)

		self.new_pwd = tk.StringVar()
		tk.Label(self.window, text='Password: ').place(x=10, y=50)
		self.entry_usr_pwd = tk.Entry(self.window, textvariable=self.new_pwd, show='*')
		self.entry_usr_pwd.place(x=150, y=50)

		self.new_pwd_confirm = tk.StringVar()
		tk.Label(self.window, text='Confirm password: ').place(x=10, y= 90)
		self.entry_usr_pwd_confirm = tk.Entry(self.window, textvariable=self.new_pwd_confirm, show='*')
		self.entry_usr_pwd_confirm.place(x=150, y=90)

		self.btn_comfirm_sign_up = tk.Button(self.window, text='Sign up', command=self.mysql_signup)
		self.btn_comfirm_sign_up.place(x=150, y=130)

	def mysql_signup(self):
		nn = self.new_name.get()
		np = self.new_pwd.get()
		npf = self.new_pwd_confirm.get()

		# connect to root user
		db = MySQLdb.connect(host="localhost", user="root", password="root", db="mysql")
		cursor = db.cursor()

		checkname = '''select * from user where User="''' + nn + '''";'''
		insertUser = ''' create user "''' + nn + '''"@'localhost' identified by "''' + np +'''";'''
		grantUser = '''grant all privileges on * . * to "''' + nn + '''"@'localhost';'''
		
		try:
			if(cursor.execute(checkname)==1):
				insert_check = 0
			else:
				insert_check = 1
		except:
			db.rollback()

		if np != npf:
			messagebox.showerror('Error', 'Password and confirm password must be the same!')
		elif not insert_check :
			messagebox.showerror('Error', 'The user has already signed up!')
			self.window.destroy()
		else:
			try:
				cursor.execute(insertUser)
				cursor.execute(grantUser)
				db.commit()
				if(cursor.execute(checkname)==1):
					messagebox.showinfo('Welcome', 'You have successfully signed up!')
				else:
					print("error!")
			except:
				db.rollback()
			finally:
				cursor.close()
				db.close()
				self.window.destroy()

class logInWindow():
	def __init__(self):
		self.window = tk.Tk()
		self.window.title('Web Crawler X MySQL')
		self.window.geometry('450x300+310+150')

		# TODO: welcome gif
		self.canvas = tk.Canvas(self.window, height=200, width=500)
		self.image_file = tk.PhotoImage(file='welcome.gif')
		self.image = self.canvas.create_image(0,0, anchor='nw', image=self.image_file)
		self.canvas.pack(side='top')

		# user information
		tk.Label(self.window, text='User name: ').place(x=50, y= 150)
		tk.Label(self.window, text='Password: ').place(x=50, y= 190)
		self.var_usr_name = tk.StringVar()
		self.entry_usr_name = tk.Entry(self.window, textvariable=self.var_usr_name)
		self.entry_usr_name.place(x=160, y=150)
		self.var_usr_pwd = tk.StringVar()
		self.entry_usr_pwd = tk.Entry(self.window, textvariable=self.var_usr_pwd, show='*')
		self.entry_usr_pwd.place(x=160, y=190)

		# login and sign up button
		self.btn_login = tk.Button(self.window, text='Login', command=self.usr_login)
		self.btn_login.place(x=170, y=230)
		self.btn_sign_up = tk.Button(self.window, text='Sign up', command=self.usr_signup)
		self.btn_sign_up.place(x=270, y=230)

		self.window.mainloop()

	def usr_login(self):
		usr_name = self.var_usr_name.get()
		usr_pwd = self.var_usr_pwd.get()

		try:
			global conn
			conn = MySQLdb.connect("localhost", usr_name, usr_pwd)
			cursor = conn.cursor()

			create_db = 'create database if not exists Final_' + usr_name
			use_db = 'use Final_' + usr_name
			cursor.execute(create_db)
			cursor.execute(use_db)
			conn.commit()
			cursor.close()
			# Test to check
			# try:
			# 	cur = conn.cursor()
			# 	cur.execute("Create Table yuting(name int);")
			# 	conn.commit()
			# except MySQLdb.OperationalError:
			# 	print("Update error")
			# else:
			# 	cur.close()
		except MySQLdb.OperationalError:
			messagebox.showerror(message='Error, the usrname or password is wrong, try again.')
			# print("connection error")
		else:
			self.window.destroy()

	def usr_signup(self):
		S = singUpWindow(self.window)

	def destroy_window(self):
		self.window.destroy()

if __name__ == '__main__':
	# global parameters for connection
	global conn
	conn = None

	# login window
	L = logInWindow()

	if not conn == None:
		main_window = mainWindow(conn)
		main_window.run()
		conn.close()

	# Here is for testing
	# try:
	# 	cur = conn.cursor()
	# 	cur.execute("Create Table yuting(name int);")
	# 	conn.commit()
	# except MySQLdb.OperationalError:
	# 	print("Update error")
	# else:
	# 	cur.close()