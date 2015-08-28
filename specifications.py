import MySQLdb

import urllib2

from bs4 import BeautifulSoup

import re

import deviations

from HTMLParser import HTMLParser

db=MySQLdb.connect('127.0.0.1','root','','intern') #establish connection


def parser(data):

    result = []

    parser = HTMLParser()

    parser.handle_data = result.append

    parser.feed(data)

    data= "".join(result)

    parser.close()

    return data






def specifications(sql):

    db=MySQLdb.connect('127.0.0.1','root','','intern') #establish connection
    
    cursor=db.cursor()

    #sql = "SELECT id,url,site FROM urllist WHERE status!='done' limit 0,10" # to fetch the urls
    cursor.execute(sql)
    data=cursor.fetchall()
    
    for d in data:
        try:
            sql="SELECT * FROM `specdetails` WHERE site='%s'"%(d[2])
            cursor.execute(sql)
            tags=cursor.fetchall()
            tag=tags[0]
            # forming a proper url to open
            
            if "https" in str(d[1]) or "http" in str(d[1]):
                url=d[1]
            else :
                url="https://"+str(d[1])

            url=url.replace(" ","-").replace("'","-")

            if tag[14]:
                url=eval(tag[14])

                
            print url
            
            #open the required webpage for specifications
            url=urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
            page=urllib2.urlopen(url)
            source=page.read()
        
            soup=BeautifulSoup(source)
            if tag[2]:
                speciflist=soup.findAll(tag[0],{tag[1]:re.compile(tag[2])})

            else:
                speciflist=soup.findAll(tag[0],{tag[1]:tag[2]})
            
            
            #tag[0] - HTML tag in which specifications are present
            #tag[1] - Attribute of the HTML tag in which specifications are present
            #tag[2] - Corresponding attribute value

            for spec in speciflist:
                
                try:

                    ########################exception 1#######################################
                    
                    if tag[10]:
                        spec=str(spec)
                        print "type x"

                        eval(str(tag[10]))

                    else:
                        
                        sql="UPDATE `urllist` SET specifications='Present',status='done' WHERE id='%s'"%(d[0])
                        cursor.execute(sql)
                        db.commit()
                        
                        soup=BeautifulSoup(str(spec))
                        if tag[5]!='':
                            specifications=soup.findAll(tag[3],{tag[4]:re.compile(tag[5])})

                        else:
                            specifications=soup.findAll(tag[3],{tag[4]:tag[5]})


                        #specifications contains list of all specification name
                        #tag[3] - HTML tag in which name of the specification is present
                        #tag[4] - Attribute of the HTML tag in which name of specification is present
                        #tag[5] - Correspondinf attribute value

                        ##############exception with specifications ##########
                                                
                        if not specifications:
                            specifications=eval(tag[12])

                        # type selection
                        if (tag[3]==tag[6] and tag[4]==tag[7] and tag[5]==tag[8]): #condition for type1
                            try:
                                type1(d[0],specifications,tag[11])
                            except Exception as x:
                                print x
                                pass
    
            
                        elif (tag[6]=="" and tag[7]): #condition for type3 

                            try:
                                        
                                type3(d[0],specifications,tag[7],tag[8],d[2],tag[11],tag[12],tag[13],spec)

                                # tag[7] contains the delimiter sepeation specification label and sepcification details
                                # tag[8] contains the the tag(if any) which splits the given source in order to get the specification label and details seperated by delimiter
                                
                            except Exception as x:
                                print x
                                pass

                        else: 


                            if tag[8]!='':
                                specificdetails=soup.findAll(tag[6],{tag[7]:re.compile(tag[8])})


                            else:
                                specificdetails=soup.findAll(tag[6],{tag[7]:tag[8]})

                            ######### exception in specification details #########     

                            if not specificdetails:
                                specificdetails=eval(tag[13])


                            #specificdetails contains list of all specification labels
                            #tag[6] - HTML tag in which details of the specification is present
                            #tag[7] - Attribute of the HTML tag in which details of specification is present
                            #tag[8] - Corresponding attribute value
                            
                            type2(d[0],specifications,specificdetails,tag[11])

                except Exception as x:
                    print x
                    
            else:
                sql="UPDATE urllist SET specifications='Not Present',status='done' WHERE id='%s'"%(d[0])
                cursor.execute(sql)
                db.commit()
            
        except Exception as x:
            print x




#when specification name and specifications details are present in the same tag with same attributes or no attributes
def type1(sno,specifications,check):

                 #establish connection
    global db
    cursor=db.cursor()

    
    for i in range(0,len(specifications),2):

        ######################## exception 2 #######################################
        
        if check:
            eval(check)

            
        specname=parser(str(specifications[i])).strip()
        details=parser(str(specifications[i+1])).strip()
        print "name---"+str(specname)
        print "detail---"+str(details)

        if (str(specname) or str(details)):

            sql="""INSERT INTO specifications(id,name,details) VALUES ('%s','%s','%s')"""%(sno,specname.replace("'",""),details.replace("'",""))
            cursor.execute(sql)
            db.commit()







#when specification labels and specification values are present in different tags or in same tag with different attributes   

def type2(sno,specifications,specificdetails,check):

    global db
    cursor=db.cursor()

    for i in range(len(specifications)):
        
        specname=parser(str(specifications[i]))
        
        ########################exception 2#######################################
        
        if check:                                                       
            eval(check)

        details=parser(str(specificdetails[i]))

        print "name~~~~~~~~ "+specname.strip()
        print "details~~~~~~~ "+details.strip()
        
        if (str(specname) or str(details)):
        
            sql="""INSERT INTO specifications(id,name,details) VALUES ('%s','%s','%s')"""%(sno,specname.replace("'","").strip().replace("\\",""),details.replace("'","").replace("\\","").strip())
            cursor.execute(sql)
        
            db.commit()





def type3(sno,specifications,delimeter,brk,site,check,specexcep,detailexcep,spec):

    global db
    cursor=db.cursor()

    
    for i in range(len(specifications)):
        content=[]
        
        if brk:
            
            content=str(specifications[i]).replace('> <','><').split(brk)
        else:
            content.append(specifications[i])

        
        for c in content:
            
            if check:
                eval(check)
                
            if delimeter in str(c):

                spec=str(c).split(delimeter,1)
    
                specname=parser(spec[0]).strip()
    
                details=parser(spec[1]).strip()

                specname=filter(lambda x: ord(x)<128,specname)
                details = filter(lambda x: ord(x)<128,details)
        

            elif specexcep:
                specname=eval(specexcep)


                if len(specname)==2:

                    details=parser(str(specname[1])).strip()
                    specname=parser(str(spename[0])).strip()


                else:
                    
                    specname=parser(str(specname[0])).strip()
                    details=eval(detailexcep)
                    details=parser(str(details[0])).strip()
                

            print "name===== "+specname
            print "details==== "+details
        
                    
        if (str(specname) or str(details)):

                sql="""INSERT INTO specifications(id,name,details) VALUES ('%s','%s','%s')"""%(sno,specname.replace("'","").strip().replace("\\",""),details.replace("'","").replace("\\","").strip())
                try:
                    cursor.execute(sql)

                    db.commit()
                except Exception as x:
                    print x        

        

        

        
        
        

        
