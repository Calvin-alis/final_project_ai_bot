

def add(a, b):
    return a + b


def test_add():
    assert add(5, 10) == 15, 'Something wrong with add'
    assert add(10, 5) == 15, 'Something wrong with add'
    assert add('a', 'b') == 'ab', 'Something wrong with add'


import sqlite3

with sqlite3.connect('storage/chat_sessions.db') as conn:
    cursor = conn.cursor()
    
    cursor.execute('select * from gpt_sessions;')
    
    res = cursor.fetchall()
    print(res)