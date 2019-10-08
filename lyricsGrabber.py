__author__ = 'Phil'

from urllib import request, parse
from bs4 import BeautifulSoup


#TODO: adapt behvaiour for grabbing sole songs and (..?)
#TODO: create given directoy if it doesn't exist
class LyricsGrabber:

    def __init__(self, arguments):

        self.artist = parse.quote((str.lower(arguments['artist'])))
        self.fileLocation = str.lower(arguments['location'])

        self.baseUrl = "http://www.magistrix.de/lyrics/"

        #
        # list of fake user agents to avoid looking like a crawling bot
        #
        self.userAgentList = [ 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9']

    ################################
    #
    ################################
    def getSongList(self):

        #
        # do not always use the same user agent
        #
        for i in range(0, len(self.userAgentList)):
            userAgent = self.userAgentList[i]

        songListUrl = self.baseUrl + self.artist

        pageRequest = request.Request(songListUrl, headers={"User-Agent": str(userAgent)})

        try:
            website = request.urlopen(pageRequest).read().decode("utf-16", "replace")

            soup = BeautifulSoup(website, 'html.parser')
            links = soup.find_all('a')

            foundLinksCounter = 0

            #
            # the desired links all contain .html and besides of "uebersetzungen", no other links do (apparently)
            # TODO: Counter is currently not working correctly
            #
            for link in links:

                href = link.get('href')
                if(href != None):
                    #
                    # grab only the <a> tags linking to a site with the artist's name in it
                    #
                    if("/lyrics/"+self.artist in str.lower(href) and ".html" in str.lower(href) and "uebersetzungen" not in str.lower(href) ):

                        foundLinksCounter += 1

                        songLyricsRequest = request.Request(self.baseUrl+link.get('href'))
                        #
                        # utf-16 due to strange characters that happen to appear in some lyric texts
                        #
                        songLyricsSite = request.urlopen(songLyricsRequest).read().decode("utf-16", "replace")

                        # TODO: make target file path optional
                        # TODO: erase illegal characters from file names (e.g. '?')
                        # TODO: skip existing files?
                        file = open(self.fileLocation + link.get_text()+".txt", "w")
                        #
                        # print progress
                        #
                        totalSongCount = len(links)
                        print(str(links.index(link)) + " of " + str(totalSongCount))
                        print(self.fileLocation + link.get_text()+".txt")

                        soupLyrics = BeautifulSoup(songLyricsSite, 'html.parser')

                        #
                        # write the content of every item in the <div> containing the lyrics into a file
                        # except the content is empty
                        # TODO: handle <br> as currently the lyrics are not sectioned into strophes
                        # TODO: Content is not written into file
                        #

                        for stuff in soupLyrics.find_all(itemprop="text"):
                            text = stuff.get_text()
                            if(text != "\n" or text != ""):
                                file.write(stuff.get_text())



                        file.close()
            if(foundLinksCounter == 0):
                print("No lyrics found. A typo maybe?")

        except request.HTTPError as e:
            if(e.code == 410):
                print("[ERROR]: Entry for artist "+ self.artist + " has been removed.")
            elif(e.code == 404):
                print("[ERROR]: Magistrix.de cannot be reached.")
            print("[ERROR]: " + str(e))
