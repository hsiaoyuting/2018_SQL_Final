import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import requests
import MySQLdb
import webbrowser

class mainWindow(object):
	def __init__(self, conn=None):
		# connection
		self.conn = conn
		
		# web list
		self.web_list = self.get_web_list()

		# window parameters
		self.width = 1350
		self.height = 750

		# create window
		self.window = tk.Tk()
		self.window.title('mainWindow')
		self.window.geometry(str(self.width+250) + 'x' + str(self.height)+"+200+150")

		# create listbox to show web
		self.listbox_web = tk.Listbox(self.window, 
			listvariable=tk.StringVar(value=tuple(self.web_list)),
			width = int(self.width * 12 / 450), height= int(self.height * 18 / 300))

		# create button_show_history
		self.button_show_history = ttk.Button(self.window, text = 'History', command = self.show_history)
	
		# create button_show_like
		self.button_show_favorite = ttk.Button(self.window, text = 'Favorite', command = self.show_favorite)

		# create button_add_web
		self.button_add_web = ttk.Button(self.window, text = '+', command = self.add_web)

		# create button_sub_web
		self.button_sub_web = ttk.Button(self.window, text = '-', command = self.sub_web)

		# create button_crawl
		self.button_crawl = ttk.Button(self.window, text = 'Crawl', command = self.crawl)

		# create button_link
		self.button_link = ttk.Button(self.window, text = 'Link', command = self.link_out)

		# create button_like
		self.button_like = ttk.Button(self.window, text = 'Like', command = self.like)

		# create button_show_agian
		self.btn_show_again = ttk.Button(self.window, text="Back", command=self.show_again)

		# create button_exit
		self.button_exit = ttk.Button(self.window, text="Exit", command=self.exit)

		# create listbox to show title
		self.listbox_title = tk.Listbox(self.window, width = int(self.width * 20 / 450), height= int(self.height * 18 /300))
		
		self.listbox_author = tk.Listbox(self.window, width = int(self.width * 16 / 450), height= int(self.height * 18 /300))

		self.listbox_subject = tk.Listbox(self.window, width = int(self.width * 16 / 450), height= int(self.height * 18 /300))

		# grid here
		self.listbox_web.grid(row = 2, column = 0, rowspan = 2, columnspan = 3)
		self.button_crawl.grid(row = 4, column = 1, sticky= tk.E+tk.W)
		self.button_add_web.grid(row = 3, column = 2, sticky=tk.S+tk.E)
		self.button_sub_web.grid(row = 3, column = 1, sticky=tk.S+tk.E)

		self.empty = tk.Label(self.window, text="", width=2).grid(row=3, column=3)

		self.listbox_title.grid(row = 2, column = 4, rowspan = 2, columnspan=2)
		self.listbox_author.grid(row = 2, column = 6, rowspan = 2, columnspan=1)
		self.listbox_subject.grid(row = 2, column = 7, rowspan = 2, columnspan=1)

		self.btn_show_again.grid(row=0, column=4)
		self.button_show_history.grid(row = 0, column = 5)
		self.button_show_favorite.grid(row = 0, column = 6)

		self.button_link.grid(row = 4, column = 5)
		self.button_like.grid(row = 4, column = 6)
		self.button_exit.grid(row = 4, column = 7)

		self.label_for_web = ttk.Label(self.window, text="Your Websites").grid(row=1, column=1)

		self.label_for_title = ttk.Label(self.window, text="Title").grid(row=1, column=4, columnspan=2)

		self.label_for_auth = ttk.Label(self.window, text="Authors").grid(row=1, column=6)

		self.label_for_sub = ttk.Label(self.window, text="Categories").grid(row=1, column=7)

		self.create_info()

		self.data = []
		self.title_list = []
		# self.author_list = []
		# self.sub_list = []

	def get_web_list(self):
		with open('default_web_list.txt', 'r') as file:
			web_list = file.read().split('\n')
		return web_list
	
	def create_info(self):
		try:
			cur = self.conn.cursor()
			cur.execute("DROP TABLE IF EXISTS temp_table")
			self.conn.commit()
		except MySQLdb.OperationalError:
			print("delete table temp_table error")

		try:
			cur = self.conn.cursor()
			cur.execute("DROP TABLE IF EXISTS real_table")
			self.conn.commit()
		except MySQLdb.OperationalError:
			print("delete table real_table error")

		create_temp_table = """CREATE TABLE `temp_table`(
		id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
		title VARCHAR(200) NOT NULL,
		author VARCHAR(200) not null,
		link VARCHAR(200) not null, 
		subject VARCHAR(200) not null
		)"""

		create_real_table = """CREATE TABLE `real_table`(
		id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
		title VARCHAR(200) NOT NULL,
		author VARCHAR(200) not null,
		link VARCHAR(200) not null, 
		subject VARCHAR(200) not null,
		history int default 0,
		favorite int default 0
		)"""

		try:
			cur.execute(create_temp_table)
			cur.execute(create_real_table)
		except MySQLdb.OperationalError:
			print("Create Table temp_table & real_table error")
		else:
			cur.close()

	def crawl(self):
		# clear existed temp_table
		try:
			cur = self.conn.cursor()
			cur.execute("DELETE FROM temp_table")
			self.conn.commit()
		except MySQLdb.OperationalError:
			print("delete data from table temp_table error")

		# web crawler # get from a list of websites, return a list of paper(type: dictionary)
		for url in self.web_list:
			try:
				html = requests.get(url)
				soup = BeautifulSoup(html.content, "html.parser")

				# get titles
				titles = soup.find_all("div", "list-title")
				titles = [t.text for t in titles]
				titles = [t.replace("\n", "") for t in titles]
				titles = [t.replace("Title: ", "") for t in titles]
				# print(titles[0])

				# get authors
				authors = soup.find_all("div", "list-authors")
				authors = [a.text for a in authors]
				authors = [a.replace("\n", "") for a in authors]
				authors = [a.replace("Authors:", "") for a in authors]
				# print(authors[0])

				# get subjects
				subjects = soup.find_all("div", "list-subjects")
				subjects = [s.text for s in subjects]
				subjects = [s.replace("\n", "") for s in subjects]
				subjects = [s.replace("Subjects: ", "") for s in subjects]
				# print(subjects[0])

				# get links
				links = soup.find_all("span", "list-identifier")
				links = [l.find("a")["href"] for l in links]
				links = ['https://arxiv.org/' + l for l in links]
				# print(links[0])
			except:
				print("OMG!!! There's something wrong when crawling!!!\n")

			if len(titles) == len(authors) == len(subjects) == len(links):
				for idx in range(len(titles)):
					data_ = {}
					data_["Title"] = titles[idx]
					data_["Authors"] = authors[idx]
					data_["Subject"] = subjects[idx]
					data_["Link"] = links[idx]
					self.data.append(data_)
				# print(data[0])
			else:
				print("OMG!!! There's something wrong when making dictionary!!!\n")

		for i in self.data:
			# print(i)
			sql = "INSERT INTO `temp_table`(`title`,`author`,`link`,`subject`) VALUES(%s,%s,%s,%s)"
			try:
				cur = self.conn.cursor()
				cur.execute(sql, (i["Title"], i["Authors"], i["Link"], i["Subject"]))
				self.conn.commit()
			except MySQLdb.OperationalError:
				print("error when insert data")
			except UnicodeEncodeError:
				pass
			else:
				cur.close()

        # show it on list_Box
		self.listbox_title.delete(0, tk.END)
		self.listbox_author.delete(0, tk.END)
		self.listbox_subject.delete(0, tk.END)

		for i in self.data:
			new_paper = tk.StringVar()
			new_paper.set(i["Title"])
			self.listbox_title.insert(tk.END,new_paper.get())
			new_paper.set(i["Authors"])
			self.listbox_author.insert(tk.END,new_paper.get())
			new_paper.set(i["Subject"].split(";")[0])
			self.listbox_subject.insert(tk.END,new_paper.get())

			self.title_list.append(i["Title"])
			# self.author_list.append(i["Authors"])
			# self.sub_list.append(i["Subject"])

	def add_web(self):

		def close_add():
			self.web_list.append(new_web.get())
			self.listbox_web.insert(tk.END, new_web.get())
			# print(self.web_list)
			window_add.destroy()

		window_add = tk.Toplevel(self.window)
		window_add.geometry('620x50+700+450')
		window_add.title('Fill in a website!')
		new_web = tk.StringVar()
		tk.Entry(window_add, width=70,textvariable=new_web).grid(row=0, column=0)
		tk.Button(window_add, text="OK", command=close_add).grid(row=0, column=1)

	def sub_web(self):
		try:
			# get the selected one
			idx = self.listbox_web.curselection()[0]

			# remove the selected one from web_list
			self.web_list.remove(self.web_list[idx])
			self.listbox_web.delete(idx)
		except:
			print("error when sub_web")

	def like(self, *args):
		# get the selected one
		idxs1 = self.listbox_title.curselection()
		idxs2 = self.listbox_author.curselection()
		idxs3 = self.listbox_subject.curselection()

		if len(idxs1)==1:
			idx = int(idxs1[0])

		if len(idxs2)==1:
			idx = int(idxs2[0])

		if len(idxs3)==1:
			idx = int(idxs3[0])

		now_title = self.title_list[idx]

		sql_extract = '''SELECT DISTINCT title, author, link, subject FROM temp_table where title="''' + now_title + '''";'''
		sql_insert = "INSERT INTO `real_table`(`title`,`author`,`link`,`subject`,`history`, `favorite`) VALUES(%s,%s,%s,%s,%s,%s)"

		try:
			cur = self.conn.cursor()
			cur.execute(sql_extract)
			R = cur.fetchall()

			for i in range(len(R)):
				cur.execute(sql_insert, (R[i][0], R[i][1], R[i][2], R[i][3], 0, 1))

			self.conn.commit()
		except MySQLdb.OperationalError:
			print("error when insert like to real_table")
		else:
			cur.close()

	def show_favorite(self):
		sql = '''SELECT DISTINCT title, author, subject FROM real_table WHERE favorite=1'''
		try:
			cur = self.conn.cursor()
			cur.execute(sql)
			R = cur.fetchall()
			self.listbox_title.delete(0, tk.END)
			self.listbox_author.delete(0, tk.END)
			self.listbox_subject.delete(0, tk.END)
			for i in range(len(R)):
				self.listbox_title.insert(tk.END, R[i][0])
				self.listbox_author.insert(tk.END, R[i][1])
				self.listbox_subject.insert(tk.END, R[i][2])
			self.conn.commit()
		except MySQLdb.OperationalError:
			print("error when show favorite")
		else:
			cur.close()

	def link_out(self):
		# get the selected one 
		idxs1 = self.listbox_title.curselection()
		idxs2 = self.listbox_author.curselection()
		idxs3 = self.listbox_subject.curselection()

		if len(idxs1)==1:
			idx = int(idxs1[0])

		if len(idxs2)==1:
			idx = int(idxs2[0])

		if len(idxs3)==1:
			idx = int(idxs3[0])

		now_title = self.title_list[idx]

		sql_extract = '''SELECT DISTINCT title, author, link, subject FROM temp_table where title="''' + now_title + '''";'''
		sql_insert = "INSERT INTO `real_table`(`title`,`author`,`link`,`subject`,`history`, `favorite`) VALUES(%s,%s,%s,%s,%s,%s)"

		try:
			cur = self.conn.cursor()
			cur.execute(sql_extract)
			R = cur.fetchall()

			for i in range(len(R)):
				cur.execute(sql_insert, (R[i][0], R[i][1], R[i][2], R[i][3], 1, 0))

			self.conn.commit()
		except MySQLdb.OperationalError:
			print("error when insert history to real_table")
		else:
			cur.close()

		sql_link = '''select link from real_table where title="''' + now_title + '''";'''
		# update
		try:
			cur = self.conn.cursor()
			cur.execute(sql_link)

			R = cur.fetchall()
			webbrowser.open(R[0][0])

			self.conn.commit()
		except MySQLdb.OperationalError:
			print("error when link out")
		else:
			cur.close()

	def show_history(self):

		sql = '''SELECT DISTINCT title, author, subject FROM real_table WHERE history=1'''
		try:
			cur = self.conn.cursor()
			cur.execute(sql)
			R = cur.fetchall()
			self.listbox_title.delete(0, tk.END)
			self.listbox_author.delete(0, tk.END)
			self.listbox_subject.delete(0, tk.END)
			for i in range(len(R)):
				self.listbox_title.insert(tk.END, R[i][0])
				self.listbox_author.insert(tk.END, R[i][1])
				self.listbox_subject.insert(tk.END, R[i][2])
			self.conn.commit()
		except MySQLdb.OperationalError:
			print("error when show favorite")
		else:
			cur.close()

	def show_again(self):
		self.listbox_title.delete(0, tk.END)
		self.listbox_author.delete(0, tk.END)
		self.listbox_subject.delete(0, tk.END)

		for i in self.data:
			new_paper = tk.StringVar()
			new_paper.set(i["Title"])
			self.listbox_title.insert(tk.END,new_paper.get())
			new_paper.set(i["Authors"])
			self.listbox_author.insert(tk.END,new_paper.get())
			new_paper.set(i["Subject"])
			self.listbox_subject.insert(tk.END,new_paper.get())

	def run(self):
		self.window.mainloop()

	def exit(self):
		try:
			cur = self.conn.cursor()
			cur.execute("DROP TABLE IF EXISTS temp_table")
			self.conn.commit()
		except MySQLdb.OperationalError:
			print("delete table temp_table error")

		self.window.destroy()


if __name__ == "__main__":
	window = mainWindow()
	window.run()