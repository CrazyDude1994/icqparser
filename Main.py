from httplib import HTTPConnection, HTTPResponse, HTTPException
from ICQParser import ICQParser
import sqlite3

class Application:
    def __init__(self, parsePages):
        self.parser = ICQParser()
        self.connection = HTTPConnection('forum.antichat.ru')
        self.parsePages = parsePages
        self.ICQList = []
        self.errorsPage = []
        self.sql = sqlite3.connect("mydb")
        self.cursor = self.sql.cursor()
        try:
            self.cursor.execute("CREATE TABLE ICQList (ICQNumber text)")
        except Exception as e:
            pass
        self.StartWork()

    def StartWork(self):
        for i in range(1, self.parsePages):
            try:
                self.connection.request('GET', '/memberlist.php?do=getall&page='+ str(i) +'&ltr=&pp=100&order=asc&postslower=0&postsupper=0&sort=username&ausername=&homepage=&icq=&aim=&yahoo=&msn=&joindateafter=&joindatebefore=&lastpostafter=&lastpostbefore=')
                self.parser.feed(self.connection.getresponse().read())
                self.ICQList.extend(self.parser.data)
                print "Proccessed", i, "page.", str((float(i) / self.parsePages) * 100) + "% has done."
            except HTTPException as e:
                self.errorsPage.append(i)
                print "Error on", i

        for icq in self.ICQList:
            self.cursor.execute("INSERT INTO ICQList VALUES (?)", (icq,))
        self.sql.commit()

if __name__ == "__main__":
    Application(1141)