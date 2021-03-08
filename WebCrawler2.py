import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from treelib import tree, Tree


class Node:
    def __init__(self, domainList, depth, url, nodeList):
        self.nodeList = nodeList
        self.domainList = domainList
        self.depth = depth
        self.url = url


startURL = 'https://whynohttps.com/'
firstNode = Node([], 0, startURL, [])
tree = Tree()


def myfunction(myNode):
    # base
    if myNode.depth >= 3 or len(myNode.domainList) >= 3:
        return myNode
    else:
        page = requests.get(myNode.url).text
        soup = BeautifulSoup(page, 'lxml')
        for a in soup.findAll('a'):
            # to not have the list be infinite
            if len(myNode.nodeList) == 3:
                return myNode
            href = a.get('href')
            # no images or links with # or /
            if href is not None and href[0] is not ('/' or '#') and ('png' or 'jpeg') not in href:
                originDomain = urlparse(myNode.url).netloc
                newDomain = urlparse(href).netloc
                # making sure its a valid link and the new domain isnt being repeaated
                if originDomain != newDomain and (
                        'https' or 'http' or 'www') in href and newDomain not in myNode.domainList:
                    print("from", myNode.url, "into", href)
                    myNode.domainList.append(newDomain)
                    print(myNode.url, myNode.domainList)
                    print(myNode.depth, 'depth')
                    print("\n")
                    myNode.nodeList.append(myfunction(Node([], myNode.depth + 1, href, [])))
    # incase no new links are found it doesnt return None
    return myNode


root = myfunction(firstNode)
tree.create_node(urlparse(root.url).netloc, root)
for a in root.nodeList:
    tree.create_node(urlparse(a.url).netloc, a, parent=root)
    for b in a.nodeList:
        tree.create_node(urlparse(b.url).netloc, b, parent=a)
        for c in b.nodeList:
            tree.create_node(urlparse(c.url).netloc, c, parent=b)

print("\n")
tree.show()
