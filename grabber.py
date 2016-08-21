import lxml.html
import requests
import time

add = 'http://government.ru/docs/'
docs_directory = 'government_docs/'


def download(url, file_name):
    with open(docs_directory+file_name, "wb") as file:
        response_download = requests.get(url)
        file.write(response_download.content)


for i in range(25000):
    response = requests.get(add + str(i)+'/?ajax=reader')
    if response.status_code == 200:
        tree = lxml.html.fromstring(response.text)
        links = tree.xpath('//a[@class="entry_file_link"]/@href')
        for link in links:
            download('http://government.ru' + link, str(i))
    else:
        print(str(i) + ' ' + str(response.status_code))
    time.sleep(0.3)