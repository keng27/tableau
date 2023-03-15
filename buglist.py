#!/usr/bin/python3
import re
import requests
from bs4 import BeautifulSoup

supportDict = { 
    '2022.3': 5,
    '2022.2': 7,
    '2022.1': 10,
    '2021.4': 11,
    '2021.3': 16,
    '2021.2': 17,
    '2021.1': 19,
    '2020.4': 22 }

## No MR for below version so stop extracting it..
#    '2020.3': 14,
#    '2020.2': 19,
#    '2020.1': 22,
#    '2019.4': 25,
#    '2019.3': 26,
#    '2019.2': 29,
#    '2019.1': 29 }

filen = "TFSresolv.csv"
ofile = open(filen, 'a+')
ofile.write("product^version^build number^TFS id^TFS id2^TFS Desc\n")
for prodtxt in ["server", "desktop"]:
    for version, j in supportDict.items():
        for i in range(0, j+1):

            vertext = version if (i == 0) else version + "." + str(i)
            surl = 'https://www.tableau.com/support/releases/' + prodtxt + '/' + vertext + '#esdalt'
            dwhtml = requests.get(surl)

            soup = BeautifulSoup(dwhtml.text, features="html.parser")
            h3txt = soup.select('h3.heading--h2')
            h5list = soup.find_all('div', class_='grid--4 text--centered')
            if not h5list:
                print(prodtxt + " version " + vertext + " not found! skipping..")
                continue
            h5txt = h5list[0].get_text()
            buildno = h5txt.split("\n")[2]  # print the actual build no

            search1 = re.search("Resolved", str(h3txt))
            if (search1):
                tfsid = soup.select('td.text--label')
                tfsdesc = soup.select('td.relative')
#                print(len(tfsid))
                for h in range(len(tfsid)):
                    tid1 = tfsid[h].get_text()
                    tid1 = tid1.strip()
                    tid1 = tid1.replace('\n',' ')
                    tidlist = tid1.split()
#                    print(len(tidlist))
                    if len(tidlist) > 1:
                        tid1 = tidlist[0]
                        tid2 = tidlist[-1]
                    else:
                        tid2 = tid1
#                       print(tid1 + "][" + tid2)

                    tdesc = tfsdesc[h].get_text()
                    tdesc = tdesc.strip()
                    tdesc = tdesc.replace('\n',' ')
#                   print(tdesc)
#                    print(vertext + "^" + str(tid1) + "^" + str(tid2) + "^" + tdesc)
                    ofile.write(prodtxt + "^" + vertext + "^" + str(buildno) + "^" + str(tid1) + "^" + str(tid2) + "^ " + tdesc + "\n")

ofile.close()
