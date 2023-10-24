import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.db = db
        self.init_main()
        self.view_records()

    # метод инициализации виджетов
    def init_main(self):
        # ТулБар
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка добавления контакта
        # PhotoImage - добавление иконки
        self.add_img = tk.PhotoImage(file='./icons/add.png')
        # image - иконка кнопки
        # bg - фон
        btn_add = tk.Button(toolbar, text='Добавить',
                            image=self.add_img,
                            bg='#d7d7d7', bd=0,
                            command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        # Кнопка редактирования контакта
        self.upd_img = tk.PhotoImage(file='./icons/update.png')
        btn_upd = tk.Button(toolbar, text='Редактировать',
                            image=self.upd_img,
                            bg='#d7d7d7', bd=0,
                            command=self.open_update)
        btn_upd.pack(side=tk.LEFT)

        # Кнопка удаления контакта
        self.del_img = tk.PhotoImage(file='./icons/delete.png')
        btn_del = tk.Button(toolbar, text='Удалить',
                            image=self.del_img,
                            bg='#d7d7d7', bd=0,
                            command=self.del_records)
        btn_del.pack(side=tk.LEFT)

        # Кнопка поиска контакта
        self.search_img = tk.PhotoImage(file='./icons/search.png')
        btn_search = tk.Button(toolbar, text='Найти',
                               image=self.search_img,
                               bg='#d7d7d7', bd=0,
                               command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        # Кнопка обновления
        self.refresh_img = tk.PhotoImage(file='./icons/refresh.png')
        btn_refresh = tk.Button(toolbar, text='Обновить',
                                image=self.refresh_img,
                                bg='#d7d7d7', bd=0,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # таблица для вывода информации о контактах
        self.tree = ttk.Treeview(self,
                                 columns=('ID', 'name', 'email', 'number'),
                                 show='headings', height=20)
        # настройки для столбцов
        self.tree.column('ID', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=250, anchor=tk.CENTER)
        self.tree.column('email', width=200, anchor=tk.CENTER)
        self.tree.column('number', width=150, anchor=tk.CENTER)

        # задаём подписи столбца
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('email', text='Эл. почта')
        self.tree.heading('number', text='Номер телефона')

        self.tree.pack()

        # создание скролл-бара
        scroll = tk.Scrollbar(root, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # метод добавления в БД (посредник)
    def record(self, name, email, number):
        self.db.insert_data(name, email, number)
        self.view_records()

    # метод редактирования в БД
    def upd_record(self, name, email, number):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''
            UPDATE users SET name = ?, email = ?, number = ?
            WHERE id = ?
            ''', (name, email, number, id))
        self.db.conn.commit()
        self.view_records()

    # метод удаления из БД
    def del_records(self):
        for i in self.tree.selection():
            self.db.cur.execute('DELETE FROM users WHERE id = ?',
                                (self.tree.set(i, '#1'), ))
        self.db.conn.commit()
        self.view_records()

    # метод поиска в БД
    def search_records(self, name):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.db.cur.execute('SELECT * FROM users WHERE name LIKE ? ', ('%' + name + '%',))
        r = self.db.cur.fetchall()
        for i in r:
            self.tree.insert('', 'end', values=i)

    # перезаполнение виджета страницы
    def view_records(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.db.cur.execute('SELECT * FROM users')
        r = self.db.cur.fetchall()
        for i in r:
            self.tree.insert('', 'end', values=i)

    # метод открытия окна добавления
    def open_child(self):
        Child()

    # метод открытия окна редактирования
    def open_update(self):
        Update()

    # метод открытия окна поиска
    def open_search(self):
        Search()


# класс дочерних окон
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_child()

    # метод для создания виджетов дочернего окна
    def init_child(self):
        self.title('Добавление контакта')
        self.geometry('500x250')
        self.resizable(False, False)
        # перехват событий в приложении
        self.grab_set()
        # перехват фокуса
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_email = tk.Label(self, text='Эл. почта')
        label_number = tk.Label(self, text='Номер телефона')
        label_name.place(x=60, y=50)
        label_email.place(x=60, y=80)
        label_number.place(x=60, y=110)

        self.entry_name = tk.Entry(self)
        self.entry_email = tk.Entry(self)
        self.entry_number = tk.Entry(self)
        self.entry_name.place(x=240, y=50)
        self.entry_email.place(x=240, y=80)
        self.entry_number.place(x=240, y=110)

        # кнопка закрытия окна
        btn_close = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_close.place(x=250, y=160)
        self.btn_ok = tk.Button(self, text='Добавить')
        self.btn_ok.bind('<Button-1>',
                         lambda ev: self.view.record(self.entry_name.get(),
                                                     self.entry_email.get(),
                                                     self.entry_number.get()))
        self.btn_ok.place(x=320, y=160)


# класс редактирования
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()

    def init_update(self):
        self.title('Редактирование контакта')
        self.btn_ok.destroy()
        self.btn_upd = tk.Button(self, text='Изменить')
        self.btn_upd.bind('<Button-1>',
                          lambda ev: self.view.upd_record(self.entry_name.get(),
                                                          self.entry_email.get(),
                                                          self.entry_number.get()))
        self.btn_upd.bind('<Button-1>', lambda ev: self.destroy(),
                          add='+')
        self.btn_upd.place(x=320, y=160)

    # метод автозаполнения формы
    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('SELECT * FROM users WHERE id = ?', id)
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_number.insert(0, row[3])


# класс поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_search()

    # метод для создания виджетов дочернего окна
    def init_search(self):
        self.title('Поиск контакта')
        self.geometry('300x100')
        self.resizable(False, False)
        # перехват событий в приложении
        self.grab_set()
        # перехват фокуса
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=40, y=20)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=140, y=20)

        # кнопка закрытия окна
        btn_close = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_close.place(x=130, y=70)

        self.btn_ok = tk.Button(self, text='Найти')
        self.btn_ok.bind('<Button-1>',
                         lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_ok.bind('<Button-1>',
                         lambda ev: self.destroy(),
                         add='+')
        self.btn_ok.place(x=220, y=70)


# класс БД
class Db:
    # создание соединения курсора и таблицы
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                         id INTEGER PRIMARY KEY,
                         name TEXT,
                         email TEXT,
                         number TEXT
            )
''')

    # метод добавления в БД
    def insert_data(self, name, email, number):
        self.cur.execute('''
                INSERT INTO users (name, email, number)
                VALUES (?, ?, ?)
''', (name, email, number))
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Телефонная книга')
    root.geometry('665x450')
    root.resizable(False, False)
    db = Db()
    app = Main(root)
    app.pack()
    root.mainloop()
