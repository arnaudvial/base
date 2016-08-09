#!/usr/bin/python

import os, time
import fnmatch
import ftplib
import commands

status, res = commands.getstatusoutput("uname -n")

ftp = ftplib.FTP('ftpperso.free.fr','arnaud.vial','md7x518a')
ftp.cwd('/'+res)

for filename in os.listdir("/home/pi"):
   if  fnmatch.fnmatch(filename, '*.jar') or fnmatch.fnmatch(filename, '*.py') or fnmatch.fnmatch(filename, '*.c'):
       print  filename
       ftp.storbinary('STOR '+str(filename),open('./'+filename,'rb'))

ftp.quit()


