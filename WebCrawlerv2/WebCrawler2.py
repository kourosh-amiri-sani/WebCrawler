import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Node:
    def __init__(self, domainList, depth, url, nodeList):
        self.nodeList = nodeList
        self.domainList = domainList
        self.depth = depth
        self.url = url

    def addToList(self, domain):
        self.domainList.append(domain)

    def setDepth(self, depthValue):
        self.depth = depthValue

    def getUrl(self):
        return self.url

    def getDepth(self):
        return self.depth


startURL = 'https://whynohttps.com/'
firstNode = Node([], 0, startURL, [])


def myfunction(myNode):
    if myNode.depth >= 3 or len(myNode.domainList) >= 3:
        return myNode
    else:
        page = requests.get(myNode.getUrl()).text
        soup = BeautifulSoup(page, 'lxml')
        for a in soup.findAll('a'):
            if len(myNode.domainList) == 3:
                return myNode
            href = a.get('href')
            if href is not None and href[0] is not ('/' or '#') and ('png' or 'jpeg') not in href:
                originDomain = urlparse(myNode.getUrl()).netloc
                newDomain = urlparse(href).netloc
                if originDomain != newDomain and (
                        'https' or 'http' or 'www') in href and newDomain not in myNode.domainList:
                    myNode.domainList.append(newDomain)
                    myNode.nodeList.append(myfunction(Node([], myNode.getDepth() + 1, href, [])))


for x in myfunction(firstNode).nodeList:
    print(x.getUrl())
