from venues.models import Cuisine

f = open('cuisineList.txt','r')
cats = [c.replace("\n", "") for c in f.readlines()]
f.close()

for c in cats:
    Cuisine.objects.create(name=c)

exit()