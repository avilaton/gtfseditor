#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#	   ormGeneric.py
#	   v 2012 07 05
#	   
#	   Copyright 2012 Gaston Avila <avila.gas@gmail.com>
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

import os
import sqlite3
import json

class dbInterface:
	def __init__(self,dbfile):
		"""Connect to the database at file 'dbfile', default to RowFactory"""
		self.connection = sqlite3.connect(dbfile)
		self.connection.row_factory = sqlite3.Row
		self.cursor = self.connection.cursor()
		
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
	
	def executeScript(self,script):
		"""Execute SQL script"""
		try:
			self.cursor.executescript(script)
			print 'Successfully Executed:\n'
		except sqlite3.OperationalError as err:
			print "Error executing", script, '\n'
			print err
	
	def insert(self,table,**kw):
		"""generates a INSERT sql statement"""
		c1 = '('+','.join([':'+k for k,v in kw.items()])+')'
		c2 = '('+','.join([k for k,v in kw.items()])+')'
		try:
			self.cursor.execute("""INSERT OR REPLACE INTO """+table+' '+c2+" VALUES "+c1,kw)
		except Exception as err:
			print 'error', '\n'
			print err
			return
		return self.cursor.lastrowid
		
	def update(self,table,columns,**kw):
		"""generates a UPDATE sql statement"""
		c1 = ' AND '.join([k+'=:'+k for k,v in kw.items()])
		c2 = ','.join([k+'=:'+k for k in columns])
		print c1
		print c2
		print """UPDATE """+table+' SET '+c2+" WHERE "+c1
		try:
			self.cursor.execute("""UPDATE """+table+' SET '+c2+" WHERE "+c1,kw)
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
		#~ else:
			#~ self.cursor.execute("DELETE FROM "+table)
		return

def main():
	db = dbInterface('testdb.sqlite')
	db.query("""CREATE TABLE IF NOT EXISTS ids (
			id INTEGER PRIMARY KEY,
			name TEXT,
			age INTEGER)""")
	for i in range(40,50):
		db.insert(table='ids',id=i,name=str(i*i),age=str(2*i))
	print db.select(table='ids')
	kw = {'id':44,'age':'test','name':'John'}
	db.update('ids',['age','name'],**kw)
	db.close()

	
if __name__ == '__main__':
	main()
