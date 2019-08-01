import random
import urllib
from googlesearch import search

# def synonim_net(word):
#     from bs4 import BeautifulSoup as bs
#     text = urllib.requests.get('https://synonim.net/synonim/' + word).text
#     soup = bs.text
#     listb = soup.find_all('a').text
#     return listb


def synonim_pl(word):
    lista=[]
    for j in search(' '.join(['synonimy',word]),tld='pl',lang='pl',num=10,start=1, stop=5,pause=2):    
        lista.append(j)
    return lista

def main():
    print('Alpha version of the program to lookup synonims')
    ans=input('Chose language: [p] - Polish, [e] - English :')
    while ans=='p':
        word=input('\nWpisz słowo: ')
        if word:
            listb=synonim_pl(word)
            print('strony zawierające synonim słowa ',word)
            for j in listb:
                print(j)
        else:
            ans='0'
        
main()
# synosy=synonim_net('brzuch')
# print(synosy)
