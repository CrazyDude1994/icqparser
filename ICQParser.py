from HTMLParser import HTMLParser

#ICQ Parser class to parse ICQ from HTML
class ICQParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []

    def feed(self, data):
        self.data = []
        HTMLParser.feed(self, data)
       
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'onclick' and 'icq' in str(attr[1]):
                    mystr = [temp.strip("'") for temp in str(attr[1]).split(', ')][1]
                    self.data.append(mystr)