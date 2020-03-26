from bs4 import BeautifulSoup,element
import requests, time, re, os, sys
from datetime import date, timedelta



def main():

    '''
    we insert the header iff the file does not exist, otherwise we open the file
    in append mode.
    '''
    if os.path.isfile('dataset_rent_rome_kijiji.tsv'):
        dataset = open('dataset_rent_rome_kijiji.tsv', 'ab')
    else:
        dataset = open('dataset_rent_rome_kijiji.tsv', 'wb')
        dataset.write('Title\tShort Description\tLocation\tPrice (Euro)\tTimestamp\tUrl Adv\n'.encode("utf-8"))  # HEADER
    request_log = open('request_log.txt', 'w')

    '''
    hard-coded url to the site to scrape
    NOTE: html element referenced in the code are strictly related to website we are scraping. To
    overcome to this limitation for generality of the script we extract information we need using the 
    function adv_extractor_to_dataset()
    '''
    url = 'https://www.kijiji.it/case/affitto/roma-annunci-roma/'
    page_counter = 1
    get_params = {'entryPoint': 'sb', 'p': page_counter}
    #1st Page is scanned outside while loop to configure last_page_number
    resp = requests.get(url, params=get_params)

    request_log.write("Request nr. "+str(page_counter)+" URL: "+resp.url+"\n\n")

    if resp.status_code >= 200 and resp.status_code <= 300:
        page = BeautifulSoup(resp.content,'html.parser')
        
        #save the page to process data offline if you need to
        raw_page = open('html_raw/page_'+str(page_counter)+'.html','wb')
        raw_page.write(page.prettify().encode("utf-8"))
        raw_page.close()

        advs = page.find(id="search-result")     # ul tag containing as children a set of li tags with adv of houses/rooms for rent.
        adv_extractor_to_dataset(advs,dataset)      #1st page written on tsv file (dataset)

        last_page_number = page.select(".last-page")[0].string      #get nr of pages
    else:
        print("HTTP Request failed."+" Status Code: "+str(resp.status_code)+".\nResponse:\n")
        print(resp.content)
        sys.exit(1)

    #fill the dataset from page 2 to last_page_number
    while page_counter < int(last_page_number):
        page_counter += 1
        print("Running... Parsing page "+str(page_counter)+" of " + last_page_number )

        get_params['p'] = page_counter
        resp = requests.get(url, params=get_params)
        request_log.write("Request nr. " + str(page_counter) + " URL: " + resp.url + "\n\n")

        if resp.status_code >= 200 and resp.status_code <= 300:
            page = BeautifulSoup(resp.content, 'html.parser')
            raw_page = open('html_raw/page_' + str(page_counter) + '.html', 'wb')
            raw_page.write(page.prettify().encode("utf-8"))
            raw_page.close()
            adv_extractor_to_dataset(page.find(id="search-result"), dataset)
            #sys.sleep() 3sec
            time.sleep(3);
        else:
            print("HTTP Request failed." + " Status Code: " + str(resp.status_code) + ".\nResponse:\n")
            print(resp.content)
            exit(1)

    dataset.close()
    request_log.close()
#routine that extracts all the adv from a page and write them on the file passed as argument
def adv_extractor_to_dataset(adv_container, dest_file):
    ''' 
    THIS CODE IS TIGHTLY COUPLED TO THE WEBSITE STRUCTURE. IT IS VARIABLE AND MIGHT NOT WORK ANYMORE EVEN ON KIJIJI.
    we extract for each ads title, short description, location, price, timestamp, url of the adv and write it into the output file
    '''
    for li in adv_container.children:
        if isinstance(li, element.Tag) and isinstance(li.div, element.Tag):
            adv = li.div
            title = adv.select(".title")[0].find("a").string \
                .replace('\n', ' ').replace('\t', ' ')
            title = re.sub('^ +', '', title)

            short_description = adv.select(".description")[0].string \
                .replace('\n', ' ').replace('\t', ' ')
            short_description = re.sub('^ +', '', short_description)

            location = adv.select(".locale")[0].string \
                .replace('\n', ' ').replace('\t', ' ')
            location = re.sub('^ +', '', location)

            price = adv.select(".price")[0].string \
                .replace('\n', ' ').replace('\t', ' ')
            price = re.sub('â‚¬ *', '', price)
            price = re.sub('^ +', '', price)

            timestamp = adv.select(".timestamp")[0].string \
                .replace('\n', ' ').replace('\t', ' ')
            timestamp = re.sub('Oggi', date.today().strftime('%d %B'), timestamp)
            timestamp = re.sub('Ieri', (date.today() - timedelta(days=1)).strftime('%d %B'), timestamp)

            url_adv = adv.select(".title")[0].find("a").get("href") \
                .replace('\n', ' ').replace('\t', ' ')

            line_out = re.sub(' +', ' ',
                              title + '\t' + short_description + '\t' + location + '\t' + price + '\t' + timestamp + '\t' + url_adv + '\n')


            dest_file.write(line_out.encode("utf-8"))



if __name__ == "__main__":
    main()