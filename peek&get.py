import time,requests,tqdm,copy,os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

print ("Enter the name of the page to scan including https://")
web = input()
print ("Enter the name of the directory to download in C:\\python37\\descargas\\ or skip to assign"+web.split("/")[-1])
dirName = input()
if not dirName:
    dirName = web.split("/")[-1]
newDirPath = "\\python37\\descargas\\"+dirName
browser = webdriver.Firefox()
browser.get(web)
time.sleep(3)
imagesUrl = []
scrollPos=0
def scan():
    global imagesUrl
    images = browser.find_elements_by_tag_name("img")
    foundSomething = False
    for image in images:
        try:
            url = image.get_attribute("src")
            if url.startswith("http") and url not in imagesUrl and not url.endswith("20"):
                imagesUrl.append(url)
        except:
            pass

def advance():
    browser.execute_script("window.scrollTo(0, "+str(scrollPos)+")")
while True:
    scrollPos+=500
    scan()
    advance()
    time.sleep(0.1)
    if scrollPos>browser.execute_script("return document.documentElement.scrollHeight"):
        print ("end of page at pos "+str(scrollPos)+" and time " + str(scrollPos/10*1.5)+". Total images found: "+str(len(imagesUrl)))
        break
counter = 0
os.mkdir(newDirPath)
errors =[]
for url in tqdm.tqdm(imagesUrl):
    try:
        with open(newDirPath+os.path.sep+"image"+str(counter)+".jpg","wb") as f:
            f.write(requests.get(url).content)
        counter +=1
    except:
        errors.append(url)
        counter +=1
print (str(len(errors)),"errors") #you can try to run again the requests.get on the errors, get their index on the url list etc...

    
