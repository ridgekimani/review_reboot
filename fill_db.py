import psycopg2
import csv


def makeList(filename):
    allRows = []
    opened = open(filename, 'r')
    read = csv.reader(opened, delimiter=',')

    for row in read:
        temp = [element.replace("'", "''") for element in row]
        allRows.append(temp)

    return allRows


def makeQuery(row):
    # Now row here should be a list
    query = "INSERT INTO venues_restaurant(name, address, phone, cuisine, closed_reports_count, is_closed, yelp_id, yelp_url, foursquare_id, foursquare_url,\"eatingOptions\", location)" + \
            " VALUES('" + row[0] + "', '" + row[1] + "', '" + row[2] + "', '" + row[3] + "', 0, false, 0, '', 0, '', '" + row[4] + "', ST_Point(" + row[6] + ',' + row[5] + '))'
    print query

    return query


def insertData(connection, rowList):
    cursor = connection.cursor()

    for row in rowList:
        print row
        query = makeQuery(row)
        cursor.execute(query)


if __name__ == '__main__':
    conn = psycopg2.connect(dbname='odesk2', host='localhost', user='postgres', password="12345",
                            port='5432')
    allRows = makeList('Restaurants.csv')
    # Cut header row
    print len(allRows)
    allRows = allRows[1:]

    insertData(conn, allRows)
    conn.commit()