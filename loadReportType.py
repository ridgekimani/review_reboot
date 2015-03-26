from venues.models.report import ReportType
ReportType.objects.all().delete()
f = open('typesList.txt','r')
types = [c.replace("\n", "") for c in f.readlines()]
f.close()

for c in types:
    ReportType.objects.create(report_type=c)

exit()