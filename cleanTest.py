import re,urllib
filename = "newTest.txt"
st = ""
pattern = "FROM|SCRIPT|file|session|meta|\([0-9a-zA-Z]\)"
with open(filename,'r+') as f:
	lines = f.readlines()
	ct=0
	for content in lines:
		if re.search(pattern,content):
			url=urllib.unquote(content).decode('latin-1')
			url=url.encode("ascii", "ignore")
			url=urllib.unquote(url).decode('utf-8')
			st+=url
		
f2 = open("newMalTest.txt","w+")
f2.write(st)

