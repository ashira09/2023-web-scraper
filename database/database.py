import sqlite3

def get_sections_name(cur):
    cur.execute(f'''SELECT sections.name FROM sections''')
    names = [string[0] for string in cur.fetchall()]
    return names

def get_subsections_name(cur):
    cur.execute(f'''SELECT subsections.name FROM subsections''')
    names = [string[0] for string in cur.fetchall()]
    return names

def get_section_url(cur, name: str):
    cur.execute(f''' SELECT sections.url FROM sections WHERE name = '{name}' ''')
    url = cur.fetchall()
    if len(url) != 0:
        return url[0][0]
    else:
        return 'Пусто'

def get_subsection_url(cur, name: str):
    cur.execute(f''' SELECT subsections.url FROM subsections WHERE name = '{name}' ''')
    url = cur.fetchall()
    if len(url) != 0:
        return url[0][0]
    else:
        return 'Пусто'

def get_book(cur, url: str):
    cur.execute(f''' SELECT * FROM books WHERE url = '{url}' ''')
    book = cur.fetchall()
    if len(book) != 0:
        return [0][0]
    else:
        return 'Пусто'

def get_all_books(cur):
    cur.execute(f''' SELECT books.name, books.author, books.cost, books.url FROM books ''')
    books = cur.fetchall()
    return books

def add_section(cur, conn, name: str, url: str):
    cur.execute(f'''INSERT INTO sections (name, url) VALUES ('{name}', '{url}')''')
    conn.commit()

def add_subsection(cur, conn, name: str, url: str):
    cur.execute(f'''INSERT INTO subsections (name, url) VALUES ('{name}', '{url}')''')
    conn.commit()

def add_book(cur, conn, name: str, author: str, cost: str, url: str):
    cur.execute(f'''INSERT INTO books (name, author, cost, url) VALUES ('{name}', '{author}', '{cost}', '{url}');''')
    conn.commit()

def create_tables(cur, conn):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            url VARCHAR(255)
        );''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS subsections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            url VARCHAR(255)
        );''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            author VARCHAR(255),
            cost VARCHAR(255),
            url VARCHAR(255)
        );''')
    conn.commit()

def truncate_books(cur, conn):
    cur.execute(''' DELETE FROM books; ''')
    conn.commit()

with sqlite3.connect('./data/prodalit.db', check_same_thread=False) as conn:
    cur = conn.cursor()
    create_tables(cur, conn)