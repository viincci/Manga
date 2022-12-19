import json
import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
from PIL import Image
from PyPDF2 import PdfMerger

def getChapterList(name):
    url = f'https://asura.gg/manga/{name}/'
    query = requests.get(url).content
    soup = BeautifulSoup(query,features="lxml")
    episodes = soup.find_all(name="div",attrs={"class":"eph-num"})
    statuses = soup.find(name='div',attrs={"class":"imptdt"})
    child = statuses.findChildren('i',  recursive=False)
    status = child[0].text
    
    lnks = []
    for ep in episodes:
        lnk = ep.find(name='a')
        if lnk['href']:
            lnks.append(lnk['href'])
    print(f"\nFile Info:\n\nName        :   { str(name).replace('-',' ')}\nChapters     :   {len(lnks)} Chapters\nStatus        : {status}")
    return lnks , status

def getComplete(name):
    print(f"\n {str(name).replace('-',' ')} has status of complete\nWritting a complete book ...")
    psth = os.walk(f'pdf/{name}')
    pdfs = []
    for pt in psth:
        pdfs = pt[-1]
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(f'pdf/{name}/{pdf}')

    merger.write(f"output/{name}-(Complete).pdf")
    merger.close()
# imagelist is the list with all image filenames

def getChapter(url_link,dname):
    url = url_link
    query = requests.get(url).content
    soup = BeautifulSoup(query,features="lxml")
    images = soup.find_all(name="img",attrs={"decoding":"async"})
    
    dir_name = url.removeprefix('https://asura.gg/').removesuffix('/').replace('/','-')
    try:
        os.mkdir(f'tmp/{dname}')
        os.mkdir(f'pdf/{dname}')
        
    except:
        pass
    os.mkdir(f'tmp/{dname}/{dir_name}')
    for img in images:
        if img['src']:
            url = img['src']
            url_img = requests.get(url).content
            name = str(url).removeprefix('https://asura.gg/wp-content/uploads/').removesuffix('.jpg').replace('/','-')
            with open(f"tmp/{dname}/{dir_name}/{name}.jpg","wb") as mg:
                mg.write(url_img)
    lstv=[]
    lst_img = []
    wrk_dr = os.getcwd()
    pat = os.walk(f'tmp/{dname}/{dir_name}')
    for p in pat:
        lst_img = p[-1]
    lst_img = lst_img[1:]
    i = 1
    for d in lst_img:
        name  = f'Image_{i}'
        name  = Image.open(f'{wrk_dr}/tmp/{dname}/{dir_name}/{d}')
        name2 = f'Img_{i}'
        name2 = name.convert('RGB')
        i = i + 1
        lstv.append(name2)
    
    im_1 = lstv[0]
    im_1.save(f'pdf/{dname}/{dir_name}.pdf', save_all=True, append_images=lstv)
    

def Download(name):
    Chapters , status = getChapterList(name)
    length = len(Chapters)
    pbar = tqdm(total=length, desc="Downloading")
    for Chpt in Chapters:
        try:
            getChapter(Chpt,name)
        except:
            print("\nFile Exist Skipping")
        pbar.update(n=1)
    if status.lower() =="dropped" or status.lower() == "completed":
        getComplete(name)    

def DownloadHome(name):
    Chapters , status = getChapterList(name)
    length = len(Chapters)
    pbar = tqdm(total=length, desc="Downloading")
    for Chpt in Chapters:
        try:
            getChapter(Chpt,name)
        except:
            print("\nFile Exist Skipping or It's an Error")
        pbar.update(n=1)
    
    getComplete(name)  


names = ['hoarding-in-hell','return-of-the-mount-hua-sect','heavenly-martial-god','the-second-coming-of-gluttony']
for name in names:
    print(f"File   : {name}")
    DownloadHome(name)


    

