#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : Quick program to download all book from http://www.glozman.com/textpages.html
    Start   : 03/1/2017
    End     : 03/15/2017
'''
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
## global variables
website = "http://www.glozman.com/textpages.html"
root    = "http://www.glozman.com/"
out_dir = "text/"

'''@function: given the website, create a dic with key is the name of the novel (Harry Potter),
            value is the links to each of the book of the novel
   @input   : website (string)
   @output  : dic (key: novel name, value: links to all books)
'''   
def get_links(web):
    soup = BeautifulSoup(urlopen(web))
    result ={}
    for link in soup.find_all('a', href=True):
        info = link['href'].split("/")[1].split("-")
        if len(info)<2:
            continue
        novel_info = info[0]
        if len(info)>=3:
            book = info[2]
        else:
            book = info[1]
        novel = novel_info.split(" ")
        novel = novel[0] + " " + novel[1]
        if novel in result:
            result[novel].append((book[1:],root+link['href']))
        else:
            result[novel]= [(book[1:],root+link['href'])]
    return result
def main():
    result = get_links(website)
    os.mkdir(out_dir)
    for novel in result:
        os.mkdir(out_dir+novel+"/")
        for book in result[novel]:
            print ("Working on novel: {}, and book :{}".format(novel,book[0]))
            fileout = open(out_dir+novel+"/"+book[0],"w")
            soup = BeautifulSoup(urlopen(book[1].replace(" ","%20")))
            fileout.write(soup.text)
            fileout.close()
main()