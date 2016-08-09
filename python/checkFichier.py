#!/usr/bin/python
# -*- coding: utf-8 -*-

#	Fichiers referencés dans la BASE (table fichier) mais ABSENT sur le disque
#	Mettre à jour parametre de connexion a la base
#	METTRE à jour basePath


import MySQLdb
import os


db = MySQLdb.connect(host="localhost",    
                     user="viappel",         
                     passwd="viappel",
                     port=3306,
                     db="viappel")        

basePath="/opt/redhat/wildfly/current/standalone/data/viappel/audioContentStore/"




idFichiers = []
cur = db.cursor()
cur.execute('select id, concat("'+basePath+'", concat(concat(repertoire,"/"),nom_local)) from fichier ')

rows = cur.fetchall()

for row in rows:
	if ( os.path.exists(row[1]) == False):
			print row[1]
			idFichiers.append(str(row[0]))
			


db.commit();
db.close()

s='delete from fichier where id in ('
for i in range(0,len(idFichiers)):
	s=s+idFichiers[i]
	if i < len(idFichiers)-1 :
		s=s+", "
		
s=s+");"

print "## Commande a executer : "
print s

