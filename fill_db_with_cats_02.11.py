from venues.models import Category

f = open('categories_name.txt','r')
cats = [c.replace("\n", "") for c in f.readlines()]
f.close()

for c in cats:
    Category.objects.create(name=c)

exit()