import os
import MySQLdb


#	Fichiers presents sur DISQUE  mais ABSENT de la BDD (table fichier)
#	METTRE a jour dirToSave


dirToSave=['/opt/redhat/wildfly/current/standalone/data/viappel/audioContentStore/']

pathBase="/"


db = MySQLdb.connect(host="localhost",    
                     user="viappel",         
                     passwd="viappel",
                     port=3306,
                     db="viappel")        


for n in range(0,len(dirToSave)):

   chemins = [dirToSave[n]]

   dirs = chemins[0].split("/")
   dirs.pop(len(dirs)-1)
   #print "dirs : "+str(dirs)
   for k in range(0,len(dirs)-1):
      pathBase=pathBase+dirs[k]
      #print pathBaseFtp
                  
  
   k=0
   i=0
   z = len(chemins)

   while (i<z):
      pathToSave = chemins[i]
     
      for filename in os.listdir(pathToSave):
               
         if os.path.isdir(pathToSave+filename):
             chemins.append(pathToSave+filename+"/")
             z = len(chemins)
         else:
         	 cur = db.cursor()
         	 cur.execute('select id from fichier where repertoire ="'+pathToSave[len(dirToSave[n]):]+'" and nom_local="'+filename+'"')
         	 row = cur.fetchone()
         	 print "repertoire = "+pathToSave[len(dirToSave[n]):len(pathToSave)-1]+"  nom_local = "+filename
         	 if row != None :
         	 	 print "rm -rf "+pathToSave+filename
      i+=1      

   print 'done'

db.commit();
db.close()
