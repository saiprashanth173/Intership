import MySQLdb

import urllib2

import re

from bs4 import BeautifulSoup

from HTMLParser import HTMLParser

db=MySQLdb.connect('127.0.0.1','root','','intern')

import specifications4

#this is to remove the html tags

def parser(data):

    result = []

    parser = HTMLParser()

    parser.handle_data = result.append

    parser.feed(data)

    data= "".join(result)

    parser.close()

    return data

#this is to pop certain detail with an exception 

def popexception(present,i,specifications,specificdetails,choice):

    if choice==0:

        if present in specifications[i]:
            specifications.pop(i)

    elif choice ==1:

        if present in specificdetails[i]:
            specificdetails.pop(i)



# this is used when the content has to be split in order to obtain the specifications


def splitApproach(pid,spec,split,spectag,specattr,speccontent,detailstag,detailsattr,detailscontent,check):

    print "entered"
    spec=spec.split(split)
    

    for spe in spec:

        soup=BeautifulSoup(spe)

        if speccontent!='':
            specifications=soup.findAll(spectag,{specattr:re.compile(speccontent)})
        else:
            
            specifications=soup.findAll(spectag,{specattr:speccontent})

        if detailstag:

            if detailscontent!='':

                specificdetails=soup.findAll(detailstag,{detailsattr:re.compile(detailscontent)})

            else:

                specificdetails=soup.findAll(detailstag,{detailsattr:detailscontent})

        

        if (detailstag==spectag and detailsattr==specattr and detailscontent==speccontetn):
            try:
                specifications4.type1(pid,specifications,check)

            except Exception as x:
                print x
                print "splitApproach" 

        else:
            try:
                specifications4.type2(pid,specifications,specificdetails,check)
            except Exception as x:
                print x
                print "splitApproach"



# this is called when specifications and specification details are not present

def getspec(tag,attr,content,spec):

    soup=BeautifulSoup(str(spec))
    if content=='':
        specif=soup.findAll(tag,{attr:content})

    else:
        specif=soup.findAll(tag,{attr:re.compile(content)})
            
    return specif



def elimination(condition,i,specifications,specificdetails,choice):

    if condition:
        if choice==0:
            specifications.pop(i)
            
        else:
            
            print specificdetails.pop(i)

    

def elimin(text,i,specifications,specificdetails,choice):
    if choice==0:
        if parser(str(specifications[i])).strip()==text:
            specifications.pop(i)
    else :
        if parser(str(specificdetails[i])).strip()==text:
            print specificdetails.pop(i)
        
            
# this is called when specifications and specification details are to be elimiated

def eliminate(condition,specifications,specificdetails,choice):

    if choice==0:

        specifications=map(lambda i: specifications[i],filter(lambda i: condition,range(len(specifications))))

    if choice==1:

        specificdetails=map(lambda i: specificdetails[i],filter(lambda i: condition,range(len(specificdetails))))

        print specificdetails

    

# url exception for samsung

def samsungurl(url):

    if "?" in url:
        url=url.replace("?","-spec?")

    else:
        url=url+"-spec"

    return url

def changeurl(url,wat,withwat):

    url=url.replace(wat,withwat)

    return url

def addtourl(url,addwat):

    url=url+addwat

    return url
