
from html.parser import HTMLParser
from urllib.request import urlopen


class SEOInfo():
    """
        Class : SEOInfo
        Purpose: To hold the data parsed from an HTML document
    """
    language = ''   # Todo
    title = ''
    meta = {
        'charset':'',
        'viewport':'',
        'description':'',
        'keywords':'',
        'og:title':'',  
        'og:description':'', 
        'og:type':'',   
        'og:url':'',    
        'og:image':''   
        }
    headings = [0,0,0,0,0] # Todo
    images = { 
        'amount':0,
        'missingALT':[]
        }
    links = []  # Todo

class SEOHTMLParser(HTMLParser):
    """
        Class    : SEOHTMLParser
        Inherits : HTMLParser
        Purpose  : Parsing Rules to find and store various tags and data, to later use to evaluate SEO score
    """
    # Create a tags object to hold the information
    tags = SEOInfo()
    # Placeholder Variable
    hold = ''

    def handle_starttag(self,tag,attrs):
        # If it finds the html tag, check if the language has been declared
        if tag == 'html':
            if attrs.__len__() > 0:
                for a in attrs:
                    if a[0] == 'lang':
                        self.tags.language = a[1]
        # This finds the title tag and "flags" the parser to record its data
        elif tag == 'title':
            self.hold = 'title'
        # Check to see if any of the meta characters in the checklist are found, record there values
        elif tag == 'meta':
            checklist = ['viewport','description','keywords','og:title','og:description','og:type','og:url','og:image']
            if attrs.__len__() > 0:
                for a in attrs:
                    if self.hold != '':
                        self.tags.meta[self.hold] = a[1]
                        self.hold = ''
                    if a[0] == 'charset':
                        self.tags.meta['charset'] = a[1]
                        break;
                    if a[1] in checklist:
                        self.hold = a[1]
        # Find and record all heading tags found
        elif tag == 'h1':
            self.tags.headings[0] += 1
        elif tag == 'h2':
            self.tags.headings[1] += 1
        elif tag == 'h3':
            self.tags.headings[2] += 1
        elif tag == 'h4':
            self.tags.headings[3] += 1
        elif tag == 'h5':
            self.tags.headings[4] += 1
        # Find all img tags and check if they are not missing any alt tags
        elif tag == 'img':
            if attrs.__len__() > 0:
                self.tags.images['amount'] += 1
                for a in attrs:
                    if a[0] == 'alt':
                        break
                else:
                    for a in attrs:
                        if a[0] == 'src':
                            self.tags.images['missingALT'].append(a[1])
                            break
                    else:
                        self.tags.images['missingALT'].append('No image src found')
        # Record all links
        elif tag == 'a':
            if attrs.__len__() > 0:
                for a in attrs:
                    if a[0] == 'href':
                        self.tags.links.append(a[1])
    # Records title tag data
    def handle_data(self,data):
        if self.hold != '':
            if self.hold == 'title':
                self.tags.title = data
                self.hold = ''
    # Returns the SEOInfo
    def getData(self):
        return self.tags


# Runs through the SEOInfo and outputs information based on what was found
def evaluateTags(tags):
    # Language
    print('\nNo language specified' if tags.language == '' else f'Your sites specified language is {tags.language}')
    # Title
    if (tags.title == ''):
        print('\nNo title tag! Add <title>Your title here</title> to your <head>')
    elif (len(tags.title) > 35):
        print(f'\nYour title {tags.title} is bit lengthy. Try making it clear, and concise, aim for around 25-30 characters')
    elif (len(tags.title) < 20):
        print(f'\nYour title {tags.title} is a little bit short. Try making it a bit more descriptive, aim for around 25-30 characters')
    else:
        print(f'\nYour title {tags.title} is looking good!')
    # Description
    if (tags.meta['description'] == ''):
        print('\nYou have no Meta Description! Add <meta name="description" content="Your description here"> to your <head>')
    elif (len(tags.meta['description']) > 160):
        print(f'\nYour meta description might be a little bit too long. {len(tags.meta["description"])} characters. Aim for 70-160 characters.')
    elif (len(tags.meta['description']) < 70):
        print(f'\nYour meta description might be a little bit too short. {len(tags.meta["description"])} characters. Aim for 70-160 characters.')
    else:
        print(f'\nYour description is looking good! - {tags.meta["description"]}')
    # Charset
    print('\nYou do not have any encoding! Add <meta charset="utf-8"> to your <head>' if tags.meta['charset'] == '' else f'\nYou have specified the character set - {tags.meta["charset"]}')
    # Viewport
    if (tags.meta['viewport'] == ''):
        print('\nYou dont have a viewport set. Add <meta name="viewport" content="width=device-width, initial-scale=1" /> to your <head>')
    else:
        print(f'\nYou have a viewport! {tags.meta["viewport"]}')
    #Keywords
    if (tags.meta['keywords'] == ''):
        print('\nYou have no keywords specified. Add <meta name="keywords" content="keywords,go,here"> to your <head>')
    else:
        format = 0
        print(f'\nYour keywords ({len(tags.meta["keywords"].split(","))}) are: ')
        for i in tags.meta['keywords'].split(","):
            if format != 0 and format % 4 == 0:
                print('')
            print(f'{i:<25}', end = " ", flush = True)
            format += 1
        print('\n')
    # OpenGraph
    if (tags.meta['og:title'] == '' and tags.meta['og:description'] == '' and  tags.meta['og:type'] == '' and tags.meta['og:url'] == '' and tags.meta['og:image'] == ''):
        print("\nYou dont have any OpenGraph tags") 
    else:
        print("\nYou have no OpenGraph Title" if tags.meta['og:title'] == '' else f'\nYour Opengraph title is {tags.meta["og:title"]}')
        print("You have no OpenGraph Description" if tags.meta['og:description'] == '' else f'Your Opengraph description is {tags.meta["og:description"]}')
        print("You have no OpenGraph Type" if tags.meta['og:type'] == '' else f'Your Opengraph type is {tags.meta["og:type"]}')
        print("You have no OpenGraph URL" if tags.meta['og:url'] == '' else f'Your Opengraph URL is {tags.meta["og:url"]}')
        print("You have no OpenGraph Image" if tags.meta['og:image'] == '' else f'Your Opengraph image is {tags.meta["og:image"]}')
    # Images
    print(f'\nYou have {tags.images["amount"]} images')
    if len(tags.images["missingALT"]) >= 1:
        for src in tags.images["missingALT"]:
            print(f'Image {src} is missing an alt atribute')
    # Links
    if len(tags.links) > 0:
        print('\nYour links are:')
        for link in tags.links:
            if link != '#':
                print('-',link)
    else:
        print('\nYou have no links!')
    # Headings
    print("\nYou have the following Headings...")
    for e, h in enumerate(tags.headings,1):
        print(f'H{e} - {h}')


def main():
    parser = SEOHTMLParser()
    link = input("Please enter the URL you would like to search: ")
    try:
        f = urlopen(link)
        contents = f.read()
        parser.feed(str(contents))
        evaluateTags(parser.getData())
    except:
        print("Error: webpage cannot be opened")

if __name__ == "__main__":
    main()