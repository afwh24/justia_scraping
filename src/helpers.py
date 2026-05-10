import requests, time
import json
import re
from config import headers, base_url, log_file
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import hashlib
from datetime import datetime

#get url response
def get_url_response(url, max_retries=5):

    #retry getting url response if there is any errors
    for attempt in range(1, max_retries+1):
        try:
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
            html = response.text
            return html
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code
            if status == 410: #response has been removed
                log_error(url, e)
                return None
            
            if status == 404: #invalid url
                log_error(url,e)
                return None
            
            print(f"[Retrying] {attempt}/{max_retries} (HTTP{status})")
            if attempt<max_retries:
                time.sleep((2**attempt)*30)
                continue
            print(f"[Error] Maxmium retries hit for getting url response - {e} ")
            raise
            
        except requests.exceptions.ReadTimeout as e:
            print(f"[Retrying] {attempt}/{max_retries}")
            if attempt<max_retries:
                time.sleep((2**attempt)*30)
                continue
            
            log_error(url, e)
            print(f"[Error] Maxmium retries hit for getting url response - {e} ")
            raise
            
#parse html response
def get_soup(html):
    return BeautifulSoup(html,"html.parser")

#get all the year urls
def get_year_urls(soup):
    years = []
    urls=[]
    ul = soup.find("ul", class_="list-columns list-columns-three list-no-styles")
    for a in ul.find_all("a"):
        year = a.get_text(strip=True)
        year_url = a['href']
        years.append(year)
        urls.append(year_url)

    return years,urls

#get all the court urls
def get_court_urls(soup):
    court_urls = []
    div = soup.find("div", class_="indented")
    for a in div.find_all("a"):
        court_url = a["href"]
        court_urls.append(court_url)
    
    return court_urls

#get all the case files urls
def get_case_file_urls(soup):
    case_urls = []
    div = soup.find("div", class_="has-negative-sides-30 zebra block has-no-bottom-margin -overflow-hidden")
    for a in div.find_all("a"):
        case_url = a["href"]
        case_urls.append(case_url)
    
    return case_urls

#get case title only
def get_case_title(soup):
    h1 = soup.find("h1", class_="heading-1")
    return h1.get_text(strip=True)

#get case text only
def get_case_text(soup):
    div = soup.find("div", class_="block", id="opinion")
    if div is None:
        div = soup.find("div", class_="wrapper jcard has-padding-30 blocks")
        if div is None:
            return None
    return div.get_text(strip=True)

#check if there is a download link
def check_download_pdf_link_exist(soup):
    a = soup.find("a", class_="pdf-icon pull-right has-margin-bottom-20")
    if a is None: return False
    return True

#get the pdf downloadable url
def get_pdf_url(soup):
    a = soup.find("a", class_="pdf-icon pull-right has-margin-bottom-20")
    raw_pdf_url = a["href"]
    pdf_url = urljoin(base_url, raw_pdf_url)
    return pdf_url


#download the actual pdf
def download_pdf(pdf_url:str, output_path:Path, max_retries=5):
    #if exist, then skip (act as checkpoint for those that can be downloaded into pdf)    
    if output_path.exists(): 
        print(f"[Skipped]{pdf_url} has been already been downloaded!")
        return 1
    #retry download if there is any errors
    for attempt in range(1, max_retries+1):
        try:
            #perform downloading of pdf
            print(f"[Downloading] {pdf_url} to {output_path}")
            with requests.get(pdf_url, headers=headers, timeout=60, stream=True) as r:
                r.raise_for_status()
                with open(output_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1 << 15):
                        if chunk:
                            f.write(chunk)
            print(f"{pdf_url} has been downloaded to {output_path}")
            return 1
        
        except Exception as e:
            print(f"[Retrying] {attempt}/{max_retries}")
            if attempt < max_retries:
                time.sleep((2**attempt)*30)
                continue
            
            print(f"[Error]: Maximum retries hit for downloading pdf - {e}")
            log_error(pdf_url, e)
            return 0


#clean invalid characters for filename
def sanitize_filename(filename):
    sanitized = re.sub(r'[\s<>:"/\\|?*]', '_', filename)
    return sanitized

#load existing case titles from jsonl only
def load_existing_urls (jsonl_path:Path):
    urls = set()
    if jsonl_path.exists():
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():continue
                record = json.loads(line)
                urls.add(record["url"])
    
    return urls

#remove empty jsonl

def remove_if_empty(jsonl_path: Path):
    """Delete jsonl_path if it contains no non-blank lines."""
    if not jsonl_path.exists():
        return  # nothing to do

    # check for any line with content
    with jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():        # found at least one non-blank line
                return              # keep the file
            
    # no non-blank lines found → delete it
    jsonl_path.unlink()
    print(f"[Removed empty file] {jsonl_path}")


#log the error message into a text file
def log_error(url, error_msg):
    with open(log_file, "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        f.write(f"[{now}] url: {url} -> {error_msg}\n")


#check pager exists -> testing
def get_page_urls(soup):
    page_urls = []
    div = soup.find("div", class_="pagination to-large-font")
    if not div: return []
    for span in div.find_all("span", class_="pagination page"):
        for a in span.find_all("a"):
            page_url = a["href"]
            page_urls.append(page_url)
    
    return page_urls

def hash_url(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]