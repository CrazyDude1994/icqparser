from httplib import HTTPConnection, HTTPException
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
            print e
            
        self.StartWork()
        #self.ProcessErrors()

    def StartWork(self):
        for i in range(201, self.parsePages + 1):
            try:
                self.connection.request('GET', '/memberlist.php?do=getall&page='+ str(i)
                                         +'&ltr=&pp=100&order=asc&postslower=0&postsupper=0&sort=username&ausername=&homepage=&icq=&aim=&yahoo=&msn=&joindateafter=&joindatebefore=&lastpostafter=&lastpostbefore=')
                response = self.connection.getresponse()
                self.parser.feed(response.read())
                self.ICQList.extend(self.parser.data)
                print "Proccessed", i, "page.", str((float(i) / self.parsePages) * 100) + "% has done."
            except HTTPException as e:
                self.errorsPage.append(i)
                print "Error on", i, e
                break
            except KeyboardInterrupt:
                print "Stopped"
                break
                
        for icq in self.ICQList:
            self.cursor.execute("INSERT INTO ICQList VALUES (?)", (icq,))
        self.sql.commit()
        self.connection.close()
        print "Changes commited!"
        raw_input()
                
    def ProcessErrors(self):
        while len(self.errorsPage) > 0:
            tempErrorsPage = []
            for i in self.errorsPage:
                try:
                    self.connection.request('GET', '/memberlist.php?do=getall&page='+ str(i)
                                             +'&ltr=&pp=100&order=asc&postslower=0&postsupper=0&sort=username&ausername=&homepage=&icq=&aim=&yahoo=&msn=&joindateafter=&joindatebefore=&lastpostafter=&lastpostbefore=')
                    response = self.connection.getresponse()
                    self.parser.feed(response.read())
                    self.ICQList.extend(self.parser.data)
                    print "Proccessed", i, "error page."
                except HTTPException:
                    tempErrorsPage.append(i)
                    print "Error on", i
                except:
                    print "Hi"
            self.errorsPage = tempErrorsPage[:]
            
        for icq in self.ICQList:
            self.cursor.execute("INSERT INTO ICQList VALUES (?)", (icq,))
        self.sql.commit()

if __name__ == "__main__":
    Application(1141)