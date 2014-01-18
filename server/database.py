#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#	   database.py
#	   2014 01 18
#	   
#	   Copyright 2014 Gaston Avila <avila.gas@gmail.com>
#	   
#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU General Public License as published by
#	   the Free Software Foundation; either version 2 of the License, or
#	   (at your option) any later version.
#	   
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU General Public License for more details.
#	   
#	   You should have received a copy of the GNU General Public License
#	   along with this program; if not, write to the Free Software
#	   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#	   MA 02110-1301, USA.

import sqlite3
import psycopg2
import psycopg2.extras

class baseDb(object):
	def __init__(self):
		pass
		
	def close(self):
		"""Close connection to database"""
		self.connection.commit()
		self.connection.close()

	def query(self,stmt):
		"""Execute SQL query 'stmt'"""
		try:
			self.cursor.execute(stmt)
			#~ print 'Successfully Executed:\n'
		except sqlite3.OperationalError as err:
			print "Error executing", stmt, '\n'
			print err

	def execute(self, stmt, args=None):
		"""Execute SQL query 'stmt'"""
		try:
			if args:
				self.cursor.execute(stmt, args)
			else:
				self.cursor.execute(stmt)
			#~ print 'Successfully Executed:\n'
		except sqlite3.OperationalError as err:
			print "Operational Error executing", stmt, '\n'
			print err
	
	def insert(self,table,**kw):
		"""generates a INSERT sql statement"""
		fields = '('+','.join([k for k,v in kw.items()])+')'

		if self.type is "named":
			params = '('+','.join([':'+k for k,v in kw.items()])+')'
			pass
		elif self.type is "pyformat":
			params = '(' + ','.join(['%('+k+')s' for k,v in kw.items()])+')'

		try:
			self.cursor.execute("""INSERT INTO """+table+' '+fields+" VALUES "+params,kw)
		except Exception as err:
			print 'error', '\n'
			print err
			return
		return self.cursor.lastrowid
		
	def update(self,table,where,data):
		""" 
		Generates a UPDATE sql statement. Arguments SELECTED and UPDATED 
		are dictionaries which specify columns to be updated and values to 
		be updated respectively
		"""
		whereQuery = ' AND '.join([str(k)+'="'+str(v)+"\"" for k,v in where.items()])
		setQuery = ','.join([str(k)+'="'+str(v)+"\"" for k,v in data.items()])
		q = """UPDATE """+table+' SET '+setQuery+" WHERE "+whereQuery
		try:
			self.cursor.execute(q)
		except Exception as err:
			print 'error', '\n'
			print err
			return
		return self.cursor.lastrowid

	def select(self,table,**kw):
		"""generates a SELECT sql statement. If no kw arguments are given, 
		defaults to all elements"""
		c1 = ' AND '.join([k+"='"+v+"'" for k,v in kw.items()])
		if kw:
			self.cursor.execute("SELECT * FROM "+table+" WHERE "+c1,kw)
		else:
			self.cursor.execute("SELECT * FROM "+table)
		return self.cursor.fetchall() 

	def remove(self,table,**kw):
		"""generates a REMOVE sql statement"""
		c1 = ' AND '.join([k+"='"+v+"'" for k,v in kw.items()])
		if kw:
			self.cursor.execute("DELETE FROM "+table+" WHERE "+c1)
		# else:
			# self.cursor.execute("DELETE FROM "+table)
		return

class dbInterface(baseDb):
	"""Sqlite supports qmark (?,?), positional (:1,:2), named (:id,:name)"""

	def __init__(self, filename):
		"""Connect to the database at file 'dbfile', default to RowFactory"""
		super(dbInterface, self).__init__()
		self.filename = filename
		self.type = "named"
		self.connection = sqlite3.connect(filename)
		self.connection.row_factory = sqlite3.Row
		self.cursor = self.connection.cursor()

class Postgress(baseDb):
	"""Pstgress supports format (%s,%s), pyformat (%(id)s, %(name)s)"""

	def __init__(self, **kwargs):
		"""All keyword arguments are passed to the connect statement"""
		super(Postgress, self).__init__()
		self.type = "pyformat"
		self.connection = psycopg2.connect(**kwargs)
		self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

def main():
	postgress = Postgress(database='testdb', user='tester', password='tester', host='127.0.0.1')
	sqlite = dbInterface(filename='testdb.sqlite')
	postgress.execute("""DROP TABLE IF EXISTS ids;""")
	postgress.execute("""CREATE TABLE IF NOT EXISTS ids (
			id INTEGER PRIMARY KEY,
			name TEXT,
			age INTEGER)""")
	sqlite.execute("""DROP TABLE IF EXISTS ids;""")
	sqlite.query("""CREATE TABLE IF NOT EXISTS ids (
			id INTEGER PRIMARY KEY,
			name TEXT,
			age INTEGER)""")

	# postgress.execute("SELECT version()")
	# print(postgress.cursor.fetchall())

	for i in range(40,50):
		postgress.execute("""
			INSERT INTO ids (id, name, age) 
			VALUES (%s,%s,%s)""",
			(i,str(i*i),str(2*i)) )
		postgress.execute("""
			INSERT INTO ids (id, name, age) 
			VALUES (%(id)s,%(name)s,%(age)s)""",
			{"id": i+100, "name": str(i*i), "age": str(2*i)})

		postgress.insert('ids', id=i+400, name=str(i*i), age=str(2*i))

		sqlite.execute("""
			INSERT INTO ids (id, name, age) 
			VALUES (?,?,?)""",
			(i,str(i*i),2*i) )
		sqlite.execute("""
			INSERT INTO ids (id, name, age) 
			VALUES (:id,:name,:age)""",
			{"id": i+100, "name": str(i*i), "age": str(2*i)})
		sqlite.execute("""
			INSERT INTO ids (id, name, age) 
			VALUES (:1,:2,:3)""",
			(i+200,str(i*i),2*i) )

		sqlite.insert('ids', id=i+400, name=str(i*i), age=str(2*i))


	
	sqlite.execute("SELECT * FROM ids ORDER BY id")
	print("sqlite results")
	for r in sqlite.cursor.fetchall():
		print(dict(r))

	postgress.execute("SELECT * FROM ids ORDER BY id")
	print("postgress results")
	for r in postgress.cursor.fetchall():
		print(dict(r))

	postgress.close()
	sqlite.close()

	
if __name__ == '__main__':
	main()
