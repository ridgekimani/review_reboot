from django.contrib.gis import geos
import csv
from venues.models import Restaurant

f = open('Restaurants.csv', 'r')
read = csv.reader(f, delimiter=',')
next(read, None)

for row in read:
    temp = [element.replace("'", "''") for element in row]
    print row
    r = Restaurant(
        name=temp[0],
        address=temp[1],
        phone=temp[2],
        cuisine=temp[3],
        location=geos.Point(float(temp[6]), float(temp[5]))
    )
    r.save()

f.close()
exit()