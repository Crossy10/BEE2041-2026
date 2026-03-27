#  scrape_xkcd 0.01              damiancclarke             yyyy-mm-dd:2026-03-26
#---|----1----|----2----|----3----|----4----|----5----|----6----|----7----|----8
#
# Syntax is: python scrape_xkcd.py
#
# This file scrapes xkcd to find the total number of comics, and the prints out
# each comic's name.  It is not meant to be remarkably useful, rather it simply
# demonstrates the use of Python's urllib library, and some basic regular expr-
# ession searches.

#-------------------------------------------------------------------------------
# (1) Import required packages, set-up names used in urls
#-------------------------------------------------------------------------------
from urllib import request, error
import re

target = 'http://www.xkcd.com'


#-------------------------------------------------------------------------------
# (2) Scrape target url and find the last comic number
#-------------------------------------------------------------------------------
response = request.urlopen(target)

#data = response.read()
#print(data.decode('utf-8'))

for line in response:
    line = line.decode('utf-8')
    #print(line)
    if 'Permanent' in line:
       print(line)
       lastComic = re.findall(r'\d+', line)[0]

#-------------------------------------------------------------------------------
# (3) Loop through all comics, finding each comic's title or capturing errors
#-------------------------------------------------------------------------------
output = open('xkcd_names.txt', 'w')
output.write('Comic, Number, Title \n')

#Currently, we iterate through ~20 comics: should start from 1
for comic in range(3200,int(lastComic)):
    url = target + '/' + str(comic)
    try:
        response = request.urlopen(url)
        for line in response:
            line = line.decode('utf-8')
            if 'ctitle' in line:
                print(line[17:-7])
                output.write('xkcd,' + str(comic) + ',' + line[17:-7] + '\n')
                        
    except error.URLError as e:
        print(f"URLError: {e}")
    except error.HTTPError as e:
        print(f"HTTPError: {e}")
    except:
        print("Other error")

output.close()
