'''
Import to db venues from sqlite3.
'''
import sqlite3
from django.contrib.gis import geos
from venues.models import Masjid
from venues.models.sect import Sect


counter = 0

sq_conn = sqlite3.connect('masjid.db')
sq_curs = sq_conn.cursor()



for row in sq_curs.execute("SELECT * FROM Masjid;"):
    counter +=1
    try:
        Sect.objects.get(name=row[2])
    except:
        Sect.objects.create(name=row[2])

    masjid = Masjid(
        name = row[0],
        address = row[1],
        sect = row[2],
        location = geos.GEOSGeometry('POINT(%s %s)' %(row[3], row[4])),
        city = row[5],
        country = row[6]
    )

    masjid.save()


print "Saved in db: ", counter
sq_conn.close()

# TABLE Masjid (
#     name text, 
#     latitude int, 
#     longitude int
# );

