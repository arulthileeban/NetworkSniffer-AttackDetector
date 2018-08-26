import re
filename = "normalTrafficTraining.txt"
st = ""
with open(filename,'r+') as f:
    lines = f.readlines()
    for i in xrange(0,len(lines)-14):
        content = lines[i]
        item = re.findall("^GET.*|POST.*$", content, re.MULTILINE)
        if item!=[]:
            #print item
            new_url=""
            url_content = lines[i+14]
            if not re.match("User-Agent",url_content):
                new_url+=item[0].replace("\r","").replace(" HTTP/1.1","")+"?"+url_content
                new_url= new_url.replace("\n","")
            else:
                new_url+=item[0].replace("\r","").replace(" HTTP/1.1","")
            st+=new_url+"\n"

f2 = open("newData.txt","w+")
f2.write(st)
