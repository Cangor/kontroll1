import doctest
import sqlite3

def data_check(mydata, data):
    """#Har datan skrivits in korrekt?.
    >>> connect = sqlite3.connect('data.db')
    >>> cursor = connect.cursor()
    >>> cursor.execute('SELECT * FROM data_tabell WHERE id = 0').fetchall()
    [(0, 'Gustav', 'Svensson', 5, 'smart', '1996-02-23', 'Gustav Svensson')]
    >>> cursor.execute('SELECT * FROM data_tabell WHERE id = 1').fetchall()
    [(1, 'Viktor', 'Vvensson', 2, 'hjälpsam', '1988-06-12', 'Viktor Vvensson')]
    >>> connect.close()
    """

doctest.testmod()