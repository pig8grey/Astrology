
import re
import numpy as np
import requests
import itertools
from bs4 import BeautifulSoup
import time

def flatten(l):
    l=list(itertools.chain(*l))
    return l

def urlgen(year,month,day):
    url=[]
    ct=[]
    for i in range (len(year)):
        for j in range (len(month)):
            for k in range (len(day)):
                url.append(('https://serennu.com/astrology/ephemeris.php?inday='+day[k]+'&inmonth='+month[j]+'&inyear='+year[i]+'&inhours=03&inmins=54&insecs=15&insort=deg30&z=t&gh=g&addobj=&inla=&inlo=&h=P'))
                ct.append(year[i]+" "+month[j]+" "+day[k])
    return url,ct 

#def block (rows): #Needs fixing
#    blocklist=['Ceres','Pluto-Charon','Mors-Somnus','Arawn','Logos','Teharonhiawako','Albion','Altjira','Deucalion','Praamzius','Typhon','Huya']
#    elements=0
#    while(elements<len(blocklist)):
#        if (rows[elements][1]==blocklist[elements]):
#            rows.pop(elements)
#        else:
#            elements+=1
#            continue
#    return rows

    
def process(rows,natal,natalS,ct):
    results=[]
    types=0


    while (types<len(rows)):

        if (rows[types][5]=="TNO" or rows[types][5]=="Dwarf" or rows[types][5]=="SDO"):
            types+=1
            continue
            
        else:
            rows.pop(types)
            
#    rows=block(rows)
    rows=pretty(rows)
    temp=ac(rows,natal,ct)
    results.append(temp)
#    temp=acs(rows,natalS,ct)
#    results.append(temp)
    results=flatten(results)
    return results

def adddata (url,natal,natalS,ct):
    stars=[]
    for i in range(len(url)):
        print("Processing {}th link. Total of {}".format(i,len(url)))
        temp=scrape(url[i])
        temp=process(temp,natal,natalS,ct[i])
        if (any(temp)):
            stars.append(temp)
        else:
            continue


    return stars

def scrape(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    my_table = soup.find('table', attrs={'id': 'results'})
    rows=str(my_table.findAll('tr'))
    rows=cleanhtml(rows)
    rows=re.split('\n',rows)
    rows.pop(0)
    rows.pop(0)
    rows=chunks(rows,9)
    time.sleep(1)
    return rows

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]
    
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def ac (transit,natal,ct):

    results=[]

#    dd = np.subtract.outer(transit[:][1][0]-natal[:][1][0])
#    md = np.subtract.outer(transit[:][1][1]-natal[:][1][1])
#    
#    
#    ddcc=np.logical_and(dd==0,md<5)
#    
#    ddc30=np.logical_and(dd%30==0,md<5,np.logical_not(ddcc))  
#    
#    ddc45=np.logical_and(dd%45==0,md<5,np.logical_not(ddcc))
#    
#    ddc60=np.logical_and(dd%120==0,md<5,np.logical_not(ddcc),np.logical_not(ddc30))  
#    
#    ddc90=np.logical_and(dd%90==0,md<5,np.logical_not(ddcc),np.logical_not(ddc45),np.logical_not(ddc30))
#    
#    ddc120=np.logical_and(dd%120==0,md<5,np.logical_not(ddcc),np.logical_not(ddc30),np.logical_not(ddc60)) 
#    
#    ddc135=np.logical_and(dd%135==0,md<5,np.logical_not(ddcc),np.logical_not(ddc45))
#    
#    ddc150=np.logical_and(dd%150==0,md<5,np.logical_not(ddcc),np.logical_not(ddc30))   
#    
#    ddc180=np.logical_and(dd%180==0,md<5,np.logical_not(ddcc),np.logical_not(ddc60),np.logical_not(ddc45),np.logical_not(ddc90),np.logical_not(ddc30))   
# 
#    

    


    
    
    for i in range (len(transit)):
        for j in range (len(natal)):
            dd=abs(transit[i][1][0]-natal[j][1][0])
            md=abs(transit[i][1][1]-natal[j][1][1])
            if (dd==0):
                if (md<5):
                    aspect='Conjunction'; 
                    results.append(ct+" "+transit[i][0]+" is "+aspect+" with "+natal[j][0])
                    continue
            if (dd%180==0):
                 if (md<5):
                     aspect= 'Opposition';
                     results.append(ct+" "+transit[i][0]+" is "+aspect+" with "+natal[j][0])
                     continue
            if (dd%60==0):
                if (dd%120==0):
                    if (md<5):
                        aspect='Triene';
                        results.append(ct+" "+transit[i][0]+" is "+aspect+" with "+natal[j][0])
                        continue
                elif (md<5):
                    aspect='Sextile';
                    results.append(ct+" "+transit[i][0]+" is "+aspect+" with "+natal[j][0])
                    continue
            if (dd%90==0):
                if (md<5):
                    aspect='Square';
                    results.append(ct+" "+transit[i][0]+" is "+aspect+" with "+natal[j][0])
                    continue
                
            if (dd%45==0):
                if (dd%135==0):
                    if (md<5):
                        aspect='135 degree';
                        results.append(ct+" "+transit[i][0]+" is "+aspect+" with "+natal[j][0])
                        continue
                elif (md<5):
                    aspect='45 degree';
                    results.append(ct+" "+transit[i][0]+" is "+aspect+" with "+natal[j][0])
                    continue
    return results

def acs (transit,natal,ct):

    results=[]


    for i in range (len(transit)):
        for j in range (len(natal)):
            dd=abs(transit[i][1][0]-natal[j][1][0])
            md=abs(transit[i][1][1]-natal[j][1][1])
            if (dd==0):
                if (md<5):
                    aspect='Conjunction'; 
                    results.append(ct+" "+transit[i][0]+" is "+aspect+" with "+natal[j][0])
                    continue
            if (dd%180==0):
                 if (md<5):
                     aspect= 'Opposition';
                     results.append(ct+" "+transit[i][0]+" is "+aspect+" with "+natal[j][0])
                     continue

            if (dd%90==0):
                if (md<5):
                    aspect='Square';
                    results.append(ct+" "+transit[i][0]+" is "+aspect+" with "+natal[j][0])
                    continue
    return results

def z2d (word):

    zodiac={'ar':0,'ta':30, 'ge':60, 'cn':90,'le':120, 'vi':150, 'li':180, 'sc':210,'sa':240,'cp':270,'aq':300,'pi':330}
    angle=[word[0],zodiac[word[1]],word[2],word[3]]
    result=np.array([int(angle[0])+int(angle[1]),int(angle[2]),int(angle[3])])
    return result
    
def pretty(star):
    for n in range (len(star)):
        word=star[n][1]
        word=re.sub('\'+', ' ',word)
        word=re.sub('"+', ' ',word)
        word=re.sub(' +', ' ',word)
        word=word.strip()
        word=word.split(" ")
        angle=z2d(word)
        star[n][1]=angle
        
    return star

def unpack(data):
    
    goodlist=[]
    for stuff in data: 
        
        if type(stuff) is list:
            asd=unpack(stuff)
            for i in asd:
                goodlist.append(i)
            
        else:

            goodlist.append(stuff)
        
    return goodlist

    
#Change your Natal Charts Here

natal=[['MC','99 ta 99\'99"'],['ASC','99 le 99\'99"'],['Sun','99 sc 99\'99"'],['Moon','99 ta 99\'99"'],['Mercury','99 sc 99\'99"'],['Venus','99 sa 99\'99"']]
natalS=[['Mars','99 sa 99\'99"'],['Jupiter','99 sa 99\'99"']]


natal=pretty(natal)
natalS=pretty(natalS)


url=[]


year=['2019','2020']
month=['1','2','3','4','5','6','7','8','9','10','11','12']
day=['1','10','20']
[url,ct]=urlgen(year,month,day)
stars=adddata(url,natal,natalS,ct)
stars=unpack(stars)
