from sqlite3 import *
conn = None
try:
	conn = connect('sms.db')
	print('Connected.')
	c = conn.cursor()
	c.execute("""CREATE TABLE records (rno int primary key, name text, marks int)""")
	print('TABLE CREATED.')
except Exception as e:
        conn.rollback()
	print('Issue:', e)
finally:
	if conn is not None:
		conn.close()
