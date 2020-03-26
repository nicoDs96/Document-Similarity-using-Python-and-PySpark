# Document Similarity using Spark, Python and Web Scraping
In this repository we are going to check similarity between kijiji ads. 
Data are first processed using classical programming and then the code 
is re-implemented using Map Reduce framework with PySpark (Apache 
spark for Python).

## Web Scraping
This scripts just create a .csv dataset with fields: title, short description, location, price, timestamp, url <br>
The code is quite general but the function ```def adv_extractor_to_dataset(adv_container, dest_file)``` is highly specific to the website we are scraping. It just takes as input the HTML containing all the data and file where to write extracted data. This function can be considered as a sample upon which you can build your own data extractor.

### Dependencies
1. [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)


## Preprocessing data with NLTK

### Dependencies
1. [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)


## Shingling, Minwise Hashing, and Locality-Sensitive Hashing.


