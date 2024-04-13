import requests
import re
import time
import bs4
import argparse
import random

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

    def isPatternExcluded(self, url):
        exclueded = False
        if 'wikimedia.org' not in url: exclueded = True
        #if 'commons' not in url or 'upload' not in url: exclueded = True
        if 'Template:Quality_image' in url: exclueded = True
        if '//meta' in url: exclueded = True
        if '//donate' in url: exclueded = True
        if '//stats' in url: exclueded = True
        if '//foundation' in url: exclueded = True
        if re.fullmatch(".*\/\/..\.wikimedia.*", url) is not None: exclueded = True
        return exclueded

    def crawl(self, startUrl, timeout_s = 10):
        tStart = time.time()

        visitedUrls = []
        imageUrls = []
        nextUrls = [startUrl]

        curUrl = startUrl
        while ((time.time() - tStart) < timeout_s ):
            print(f'Checking {curUrl}')
            nextUrls.remove(curUrl)
            try:
                resp = requests.get(curUrl, headers=self.headers)
                links = self.getLinks(resp.text)
                visitedUrls.append(curUrl)
            except:
                pass
            # print(visitedUrls)

            for l in links:
                if l is None: continue
                if self.isPatternExcluded(l): continue
                if self.isImage(l) and l not in imageUrls: imageUrls.append(l)
                elif l not in nextUrls and l not in visitedUrls: nextUrls.append(l)
            random.shuffle(nextUrls)
            curUrl = nextUrls[0]
        return imageUrls, len(visitedUrls)
        
if __name__ == "__main__":
    crwl = WikimediaCrawler()
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--url')
    parser.add_argument('--time', type=int, default= 10)
    parser.add_argument('--out', default='media_links.txt')
    args = parser.parse_args()

    crwl.media, visited = crwl.crawl(args.url, timeout_s=args.time)
    print(f'Found {len(crwl.media)} images and visited {visited} sites')

    with open(args.out, "w") as fp:
        for l in crwl.media:
            fp.write(l + '\n')
