from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = [] 
    
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)
        self.fed.append(data)

    def get_data(self):
        return "".join(self.fed)

# # parser = MyHTMLParser()
# # parser.feed('<html><head><title>Test</title></head>'
# #             '<body><h1>Parse me!</h1></body></html>')


# parser = MyHTMLParser()
# parser.feed('Head <b>southeast</b> on <b>2380 St</b>')
# print(parser.get_data())
