
from html.parser import HTMLParser
from urllib.request import urlopen


seoTags = {'title':0,'meta':0,'headings':[0,0,0,0,0],'missingALT':0,'language':'none'}



class SEOHTMLParser(HTMLParser):
    def handle_starttag(self,tag,attrs):
        global seoTags

        if tag == 'html':
            if attrs.__len__() > 0:
                for a in attrs:
                    if a[0] == 'lang':
                        seoTags['language'] = a[1]
        elif tag == 'title':
            seoTags['title'] += 1
        elif tag == 'meta':
            seoTags['meta'] += 1
        elif tag == 'h1':
            seoTags['headings'][0] += 1
        elif tag == 'h2':
            seoTags['headings'][1] += 1
        elif tag == 'h3':
            seoTags['headings'][2] += 1
        elif tag == 'h4':
            seoTags['headings'][3] += 1
        elif tag == 'h5':
            seoTags['headings'][4] += 1
        elif tag == 'img':
             for a in attrs:
                 if a[0] == 'alt':
                     break
             else:
                 seoTags['missingALT'] += 1


def printPretty():
    print(f'Title Tag: {bool(seoTags["title"])}')
    print(f'Meta Tags: {seoTags["meta"]}')
    print(f'Declared Language: {seoTags["language"]}')
    print(f'H1 - {seoTags["headings"][0]}, H2 - {seoTags["headings"][1]}, H3 - {seoTags["headings"][2]}, H4 - {seoTags["headings"][3]}, H5 - {seoTags["headings"][4]}')
    print(f'Missing Alt Tags: {seoTags["missingALT"]}')


def main():
    parser = SEOHTMLParser()
    link = 'https://ajmportfolio.interconnected.live/'
    try:
        f = urlopen(link)
        contents = f.read()
        parser.feed(str(contents))
        printPretty()
    except:
        print("Error: webpage cannot be opened")


if __name__ == "__main__":
    main()