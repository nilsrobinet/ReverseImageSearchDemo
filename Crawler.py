import requests
import re
import time
import bs4

class WikimediaCrawler(object):
    '''Simple webcrawler that crawls wikimedia for images that can be fed into the ReverseImageSearch engine'''
    
    img_types = ['.png','.jpg','.gif']

    def __init__(self) -> None:
        self.newLinks = []
        self.visited = []
        self.media = []
        self.headers = {'User-Agent': 'reverseImageSearchTest/0.0'}
        self.startTime = 0

    def getLinks(self, html:str):
        ret = []
        soup = bs4.BeautifulSoup(html,"html.parser")
        for link in soup.find_all('a'):
            ret.append(link.get('href'))
        return ret

    def isImage(self, url):
        return "https://upload.wikimedia.org" in url and any([s in url[-4:] for s in self.img_types])

    def crawl(self, url, timeout_s = 10, first = True):
        if first:
            self.startTime = time.time()
        if time.time() - self.startTime > timeout_s:
            return
        
        self.visited.append(url)
        if url in self.newLinks:
            self.newLinks.remove(url)

        try:
            resp = requests.get(url, headers=self.headers)
            links = self.getLinks(resp.text)
        except:
            return

        for l in links:
            if l is None: continue
            if 'wikimedia.org' not in l: continue
            if self.isImage(l) and l not in self.media:
                self.media.append(l)
            elif l not in self.newLinks and l not in self.visited:
                self.newLinks.append(l)
        
        self.newLinks.sort(key=lambda x: not any([s in x for s in self.img_types]))

        for l in self.newLinks:
            self.crawl(l, first=False)

if __name__ == "__main__":
    crwl = WikimediaCrawler()
    crwl.crawl("https://commons.wikimedia.org/w/index.php?search=puppy&title=Special:MediaSearch&go=Go&type=image", timeout_s=60)
    

    print(f'Found {len(crwl.media)} images and visited {len(crwl.visited)} sites')

    with open('media_links.txt', "w") as fp:
        for l in crwl.media:
            fp.write(l + '\n')
