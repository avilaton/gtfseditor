
@manager.command
def backup(dbname):
  import subprocess
  import datetime

  now = datetime.datetime.now()
  # timestamp = now.strftime("%Y-%m-%d")
  timestamp = now.isoformat()
  filename = dbname + "_" + timestamp + ".tar"
  folderId = "0Bx2pbTBESHr7ZWdhV09EOUlPVjA"
  print("backing up as " + filename)
  subprocess.call("pg_dump -Ft " + dbname + " > " + filename, shell=True)
  print("uploading to drive folder " + folderId)
  subprocess.call("drive upload -f " + filename + " -p " + folderId, shell=True)

