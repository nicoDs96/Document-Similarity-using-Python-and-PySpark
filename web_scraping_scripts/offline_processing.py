from bs4 import BeautifulSoup,element
import time, re, os
from datetime import date, timedelta



def main():

    #insert the header iff the file does not exist
    if os.path.isfile('dataset_rent_rome_kijiji.tsv'):
        dataset = open('dataset_rent_rome_kijiji.tsv', 'ab')
    else:
        dataset = open('dataset_rent_rome_kijiji.tsv', 'wb')
        dataset.write('Title\tShort Description\tLocation\tPrice (Euro)\tTimestamp\tUrl Adv\n'.encode("utf-8"))  # HEADER

    #path = "C:\\Users\\nds\\PycharmProjects\\DM_HW1\\html_raw\\"
    path = os.getcwd()+"/html_raw/"
    #print(os.listdir())
    for filename in os.listdir(path):
        html_file = open(path+filename,'r', errors='ignore' )
        page = BeautifulSoup(html_file, 'html.parser')
        advs = page.find(id="search-result")  # ul tag containing as children a set of li tags with adv of houses/rooms for rent.
        adv_extractor_to_dataset(advs, dataset)  # 1st page written on tsv file (dataset)

    dataset.close()

#routine that extracts all the adv from a page and write them on the file passed as argument
def adv_extractor_to_dataset(adv_container, dest_file):

    for li in adv_container.children:
        if isinstance(li, element.Tag) and isinstance(li.div, element.Tag):
            adv = li.div
            title = adv.select(".title")[0].find("a").string\
                .replace('\n', ' ').replace('\t', ' ')
            title=re.sub('^ +','',title)

            short_description =  adv.select(".description")[0].string\
                .replace('\n', ' ').replace('\t', ' ')
            short_description = re.sub('^ +', '', short_description)

            location = adv.select(".locale")[0].string\
                .replace('\n', ' ').replace('\t', ' ')
            location = re.sub('^ +', '', location)

            price = adv.select(".price")[0].string\
                .replace('\n', ' ').replace('\t', ' ')
            price = re.sub( 'â‚¬ *', '', price)
            price = re.sub('^ +', '', price)

            timestamp = adv.select(".timestamp")[0].string\
                .replace('\n', ' ').replace('\t', ' ')
            timestamp = re.sub('Oggi', date.today().strftime('%d %B'), timestamp)
            timestamp = re.sub('Ieri', (date.today()-timedelta(days=1)).strftime('%d %B'), timestamp)

            url_adv = adv.select(".title")[0].find("a").get("href")\
                .replace('\n', ' ').replace('\t', ' ')

            line_out= re.sub(' +', ' ', title+'\t'+short_description+'\t'+location+'\t'+price+'\t'+timestamp+'\t'+url_adv+'\n')


            dest_file.write(line_out.encode("utf-8"))




if __name__ == "__main__":
    main()