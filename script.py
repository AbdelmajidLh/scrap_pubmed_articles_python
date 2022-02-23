'''
Downloading scientific articles using beautifulsoup in python
@author : Abdelmajid EL. - 2022-02
            Data analyst
            Private use for educational purposes - The author has "no responsibility" for illegal use.
            '''
# import my libraries
from email import header
import imp
import os
import requests
from time import sleep, time
from bs4 import BeautifulSoup
import tomli
from tqdm import tqdm

# we will try one of this urls (if no result, you should find the correct url)
''' https://sci-hub.se
    https://sci-hub.st
    https://sci-hub.ru'''

# Working link (sci-hub)
my_link = "https://sci-hub.ru"

# user agent : in google put "my user agent" and copy the first result
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
    'Connection' : 'keep-alive'
}

# set directory for results
print("\n", "Writing files ... (please waite)")
my_dir = os.getcwd()
res_dir = my_dir + "/My_pdf_files"

# if res folder does not exist, create it
if not os.path.exists(res_dir):
    os.mkdir(res_dir)

# read PMIDs identifiers (pubMed identifiers)
my_PMID_list = open("my_list_PMIDs.txt", 'r')
PMID_list = my_PMID_list.readlines()

for element in tqdm(PMID_list):
    try:
        payload = {
            'sci-hub-plugin-check':'',
            'request': str(element.strip())
        }

        pdf_name = element.strip()
        base_url = my_link
        response = requests.post(base_url, headers= headers, data=payload, timeout=60)
        soup = BeautifulSoup(response.content, 'html.parser')
        #id=pdf (inpect a pdf into sci-hub page)
        content = soup.find(id='pdf').get('src').replace("#navpanes=0&view=fitH", '').replace('//', '/')

        if content.startswith('/downloads'):
            pdf = my_link + content
        elif content.startswith('/tree'):
            pdf = my_link + content
        elif content.startswith('/uptodate'):
            pdf = my_link + content
        else:
            pdf = 'https:/' + content

        # write pdf file
        r = requests.get(pdf, stream=True)
        with open(res_dir + '/' + pdf_name.replace('/', '-') + '.pdf', 'wb') as file:
            file.write(r.content)

        # create  txt file with Ids found
        pdfs = open('Pdfs_found.txt', 'a')
        pdfs.write(element.strip() + '\t' + pdf + '\n')

    except:
        # if pdf not found: create a txt file with PMID 
        nopdfs = open('PDFs_not_found.txt', 'a')
        nopdfs.write(element.strip() + '\n')
    sleep(1)