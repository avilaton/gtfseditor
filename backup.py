#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import datetime

def main():
	now = datetime.datetime.now()
	# timestamp = now.strftime("%Y-%m-%d")
	timestamp = now.isoformat()
	filename = "mza_" + timestamp + ".tar"
	folderId = "0Bx2pbTBESHr7ZWdhV09EOUlPVjA"
	print("backing up as " + filename)
	subprocess.call("pg_dump -Ft mza > " + filename, shell=True)
	print("uploading to drive folder " + folderId)
	subprocess.call("drive upload -f " + filename + " -p " + folderId, shell=True)

if __name__ == '__main__':
	main()
