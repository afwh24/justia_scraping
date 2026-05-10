import json
from config import base_url,output_root_dir,districts, districts_group_1, districts_group_2, districts_group_3,districts_group_4,districts_group_5
from helpers import get_url_response, get_soup, get_year_urls, get_court_urls, get_case_file_urls, get_case_title, get_case_text, check_download_pdf_link_exist,get_pdf_url, download_pdf, load_existing_urls,remove_if_empty, hash_url,get_page_urls, log_error

def main():
    for district in districts:
        district_url = district.replace(" ","-")
        url = f"https://law.justia.com/cases/federal/district-courts/{district_url}"
        html_response = get_url_response(url)

        #get the years url
        years_soup = get_soup(html_response)
        years, years_url = get_year_urls(years_soup)
        
        for index in range(len(years)):
            counter = 1 #file counter to be used as part of file name convention - can be removed

            year = years[index]
            year_url = years_url[index]
            output_dir = output_root_dir/district/year
 
            output_dir.mkdir(parents=True, exist_ok=True)
            jsonl_path = output_dir/f"_{year}.jsonl"
            
            existing_urls = load_existing_urls(jsonl_path)

            with open(jsonl_path, "a", encoding="utf-8") as f:
                print(f"{year} -> {base_url}{year_url}")
                years_html_response = get_url_response(f"{base_url}{year_url}")
                
                court_soup = get_soup(years_html_response)
                court_urls = get_court_urls(court_soup)
                seen_page_urls = set(court_urls)

                for court_url in court_urls:
                    court_html_response = get_url_response(f"{base_url}{court_url}") #inside the first page
                    #get the case urls
                    case_soup = get_soup(court_html_response)
                    case_urls = get_case_file_urls(case_soup)

                    #add pages into the court_urls to continue processing for subsequent pages for the current district & year
                    for page_url in  get_page_urls(case_soup): 
                        if page_url not in seen_page_urls:
                            court_urls.append(page_url)
                            seen_page_urls.add(page_url)

                    
                    for case_url in case_urls:
                        url_to_extract = f"{base_url}{case_url}"

                        #use url to prevent storing of duplicates cases
                        if url_to_extract in existing_urls: continue 

                        case_html_response = get_url_response(url_to_extract)

                        #skipped if the case response has been removed (status code = 410)
                        if case_html_response is None: continue 

                        #scrape the information from the website -> causing scraping problem at times 
                        case_soup = get_soup(case_html_response)
                        case_title = get_case_title(case_soup)


                        #check if there is a download button
                        download_exist = check_download_pdf_link_exist(case_soup)

                        #extract the case title and content out and store it into a jsonl file    
                        #cannot download pdf file
                        if not download_exist:
                            print(f"[Extracting] {url_to_extract} to JSONL")
                            case_content = get_case_text(case_soup)
                            if case_content is None: 
                                log_error(url_to_extract, "Unable to extract or download PDF file")
                                continue

                            record = {
                                "url": url_to_extract,
                                "title": case_title,
                                "text": case_content
                            }

                            f.write(json.dumps(record, ensure_ascii=False)+ "\n")
                            existing_urls.add(url_to_extract)

                        else:
                            #can be downloaded as pdf
                            pdf_url = get_pdf_url(case_soup)
                            filename = hash_url(pdf_url)
                            #filename = f"{district}_{year}_{counter}".lower()
                            pdf_download_path = output_dir/f"{filename}.pdf"
                            counter+=download_pdf(pdf_url, pdf_download_path)
                    
    

            remove_if_empty(jsonl_path) #delete empty jsonl file
            print(f"{district}/{year} extraction has been completed")            
        print(f"{district} extraction has been completed")
       

main()