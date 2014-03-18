#!/usr/bin/python
# -*- coding: utf-8 -*-

import tablib

def main():
    book = tablib.Databook()
    data = tablib.Dataset()
    data.title = 'first sheet'
    data.headers = ['First Name', 'Last Name']
    # collection of names
    names = ['Kenneth Reitz', 'Bessie Monke']

    for name in names:
        # split name appropriately
        fname, lname = name.split()

        # add names to Dataset
        data.append([fname, lname])

    book.add_sheet(data)
    with open('students.ods', 'wb') as f:
        f.write(book.ods)
    
if __name__ == '__main__':
    main()
