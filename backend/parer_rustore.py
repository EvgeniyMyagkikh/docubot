
import random

import requests
from bs4 import BeautifulSoup
from htmldocx import HtmlToDocx

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': '_ym_uid=1720192459296821044; _ym_d=1720192459; _ym_isad=1; _ga=GA1.1.1027643322.1720192459; _ga_3R5JQM4WFB=GS1.1.1720224881.7.0.1720224881.0.0.0; _ym_visorc=b',
    'if-modified-since': 'Sat, 06 Jul 2024 14:12:28 GMT',
    'if-none-match': 'W/"6687ff4c-e6a7"',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

sitemap = 'https://www.rustore.ru/sitemap-help.xml/'
 
url_link = requests.get(sitemap)
file = BeautifulSoup(url_link.text, "lxml")
links = file.find_all('loc')

ports_url = 'http://spys.one/proxy-port/'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}

proxies = []
soup = BeautifulSoup(requests.post(ports_url, headers=headers, data={'xpp': 5}).content, 'html.parser')

for f in soup.select('td[colspan="2"] > a > font.spy6')[:20]:
    u = 'http://spys.one/proxy-port/' + f.text + '/'
    s = BeautifulSoup(requests.post(u, headers=headers, data={'xpp': 5}).content, 'html.parser')
    for ff in s.select('tr > td:nth-child(1) > font.spy14'):
        proxies.append(ff.text)

proxy = random.choice(proxies)

def get_html(url, headers):
    global proxy
    try:
        response = requests.get(url, headers=headers, proxies={'http': proxy}, timeout=10)
    except:
        proxy = random.choice(proxies)
        response = requests.get(url, headers=headers, proxies={'http': proxy}, timeout=10)
    if 'К сожалению, мы не смогли найти запрашиваемую вами страницу.' in response.content.decode('utf8'):
        return None
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    else:
        proxy = random.choice(proxies)
        return get_html(url, headers)
    
import os
import random
import time

from tqdm import tqdm

if not os.path.exists("rustore/"): 
    os.makedirs("rustore/") 

results = []


for i in tqdm(links[147:]):
    to_parse = i.text
    output = to_parse.replace('https://www.rustore.ru/', '').replace('/','_')
    if '%E2%80%8E0' in output:
        to_parse = to_parse.replace('%E2%80%8E0', '0')
        output = output.replace('%E2%80%8E0', '0')
    if output.endswith('_'):
        output = output[:-1]
    soup = get_html(to_parse, headers)
    if soup == None:
        continue
    with open(f'rustore/{output}.html', 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
    time.sleep(0.5)
    
# postprocess

import glob
import os
import re

from bs4 import BeautifulSoup

# Define the directory containing your HTML files
input_directory = 'rustore/'
output_directory = 'cleaned_rustore/'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Define the HTML blocks to remove
selectors = [
        {'name': 'div', 'attrs': {'aria-label': 'Перейти к основному содержимому', 'role': 'region'}},
        {'name': 'nav', 'attrs': {'aria-label': 'Main', 'class': 'navbar navbar--fixed-top'}},
        {'name': 'button', 'attrs': {'aria-label': 'Прокрутка к началу', 'class': 'clean-btn theme-back-to-top-button backToTopButton_sjWU', 'type': 'button'}},
        {'name': 'aside', 'attrs': {'class': 'theme-doc-sidebar-container docSidebarContainer_YfHR'}},
        {'name': 'nav', 'attrs': {'aria-label': 'Навигационная цепочка текущей страницы', 'class': 'theme-doc-breadcrumbs breadcrumbsContainer_Z_bl'}},
        {'name': 'nav', 'attrs': {'aria-label': 'Страница документа', 'class': 'pagination-nav docusaurus-mt-lg'}},
        {'name': 'div', 'attrs': {'class': 'tocCollapsible_ETCw theme-doc-toc-mobile tocMobile_ITEo'}},
        {'name': 'div', 'attrs': {'class': 'col col--3'}},
        {'name': 'footer', 'attrs': {'class': 'footer'}}
    ]

def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    for t in soup.find_all('title'):
        t.decompose()
        
    for script in soup.find_all('script'):
        script.decompose()

    for code in soup.find_all('code'):
        code.replace_with(" " + code.get_text() + " ")

    for llink in soup.find_all('a'):
        llink.replace_with(" " + llink.get_text() + " ")

    for img in soup.find_all('img'):
        if ('/help/' in img.get('src')) and ('.svg' in img.get('src')):
            '/help/cross-icon.svg'
            img.replace_with(img.get('src').split('/')[-1].replace('.svg','').replace('-', '_'))
        else:
            img.decompose()


    for selector in selectors:
        tag = soup.find(selector['name'], attrs=selector['attrs'])
        if tag:
            tag.decompose()
    
    return str(soup)


for filename in glob.glob(f'{input_directory}/*.html'):
    input_path = filename
    output_path = os.path.join(output_directory, filename.split('/')[-1])

    with open(input_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    cleaned_html = clean_html(html_content)
    cleaned_html = re.sub(u'[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\U00010000-\U0010FFFF]+', '', cleaned_html)

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_html)

os.system('cd cleaned_rustore')
os.system('cat *.html > output.html')
os.system('cd ..')


new_parser = HtmlToDocx()
new_parser.parse_html_file('cleaned_rustore/output.html', 'output')
