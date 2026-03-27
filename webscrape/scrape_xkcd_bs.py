#  scrape_xkcd_bs 0.01           damiancclarke             yyyy-mm-dd:2026-03-27
#---|----1----|----2----|----3----|----4----|----5----|----6----|----7----|----8
#
# Syntax is: python scrape_xkcd_bs.py
#
# This file scrapes xkcd to find the total number of comics, and the prints out
# each comic's name.  It is not meant to be remarkably useful, rather it simply
# demonstrates the use of Python's urllib library, and some basic regular expr-
# ession searches.

#-------------------------------------------------------------------------------
# (1) Import required packages, set-up names used in urls
#-------------------------------------------------------------------------------
from urllib import request, error
from bs4 import BeautifulSoup


#-------------------------------------------------------------------------------
# (2) Loop through comics, finding each comic's title
#-------------------------------------------------------------------------------
target = 'http://www.xkcd.com'
output = open('xkcd_names_2.txt', 'w')
output.write('Comic, Number, Title \n')

for comic in range(1,3200):
    url = target + '/' + str(comic)
    soup = BeautifulSoup(request.urlopen(url),'html.parser')
    title = soup.title.string
    print(title)
    
    #print(soup.get_text())
    output.write('xkcd,' + str(comic) + ',' + title[6:] + '\n')

output.close()
