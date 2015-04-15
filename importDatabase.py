'''
Import to db venues from sqlite3 with categories,
if category not in list categories_name.txt, adds without one.

Cuisine, eatingOptions and categories don't stored in db.
'''
import sqlite3
from django.contrib.gis import geos
from venues.models import Cuisine, Restaurant

RESTS_SQLITE_FILE = 'upload.db'

f = open('cuisineList.txt', 'r')
cats = [c.replace("\n", "") for c in f.readlines()]
f.close()

counter = 0

sq_conn = sqlite3.connect(RESTS_SQLITE_FILE)
sq_curs = sq_conn.cursor()

for row in sq_curs.execute("SELECT * FROM Restaurant;"):
    rest_cats = row[3].split(', ')
    rest = Restaurant(
        name=row[0],
        address=row[1],
        phone=row[2].replace(" ", "") or '',
        catering="Catering" in row[4],
        delivery="Delivery" in row[4],
        location=geos.GEOSGeometry('POINT(%s %s)' % (row[10], row[9])),
        yelp_url=row[6] or '',
        foursquare_url=row[8] or '',
        approved=True,
        city=row[11],
        country=row[12],
    )
    rest.save()
    counter += 1
    for cat in rest_cats:
        try:
            cat_in_db = Cuisine.objects.get(name=cat)
            rest.cuisines.add(cat_in_db)
            rest.save()
        except:
            pass

print "Saved in db: ", counter
sq_conn.close()

# TABLE Restaurant (
# 0name text,
#     1address text, 
#     2phone int,
#     3cuisine text, 
#     4eating_options text, 
#     5yelp_id text, 
#     6yelp_url text, 
#     7fq_id text,  
#     8fq_url text, 
#     9latitude int, 
#     10longitude int
# );
