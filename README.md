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
2. [Pandas](https://pandas.pydata.org/docs/getting_started/index.html#getting-started)

## Preprocessing data with NLTK
For the linguistic analysis we used the NLTK Python library.
1. Firt we have to preprocess data. For each announcement (downloaded during web scraping) a textual Field (e.g. title + 
full description).Preprocessing consist of stopword removal, normalization, stemming.
2. The next step is to build a search-engine index. First, we need to build an inverted index,
and store it in a File. To Build an index that allows to perform proximity queries using the
cosine-similarity measure we have choosen fast cosine similarity algorithm (check .ipynb for details). Then we have some query-processing code, which, given some terms
it will bring the most related announcements.
<br><br>
Code is provided as a notebook, so we have either text and code with output.

### Dependencies
1. [Pandas](https://pandas.pydata.org/docs/getting_started/index.html#getting-started)
2. [NLTK](https://www.nltk.org/)


## Shingling, Minwise Hashing, and Locality-Sensitive Hashing.
Here we are implementing nearest-neighbor search for text documents. Implementation comprises shingling, 
minwise hashing, and locality-sensitive hashing. We split it into several parts:
- Implement a class that, given a document, creates its set of character shingles of some length k.
Then represent the document as the set of the hashes of the shingles, for some hash function.
- Implement a class, that given a collection of sets of objects (e.g., strings, or numbers), creates
a minwise hashing based signature for each set.
- Implement a class that implements the locally sensitive hashing (LSH) technique, so that,
given a collection of minwise hash signatures of a set of documents, it Finds the all the
documents pairs that are near each other.
To test the LSH algorithm, also a class is implemented that given the shingles of each of the documents, finds 
the nearest neighbors by comparing all the shingle sets with each other. <br>
We will apply the algorithm to solve the problem that companies such as kijiji face when
companies or individuals post many copies of the same announcement (maybe usign bots), usully they want to block
announcements that are near duplicates, otherwise users keep putting up announcements for the
same job to show up in the top. We work on the announcements for apartments of sraping part.
We want to find announcements that are near duplicates. We will say that two announcements are near 
duplicates if the Jaccard coefficient of their shingle sets is at least 80%. We will use shingles
of length 10 characters. <br> \
To apply the algorithm you have the following tasks:
1. Find the near-duplicates among all the announcements of dataset, using
LSH. Use the full description, if you have it, otherwise the short description.
2. Find the near-duplicates among all the announcements of Homework 1 by comparing them
with each other.
3. The number of duplicates found and the size of the intersection are reported in both cases.
4. The time required to compute the near duplicates in either case is also reported.
To create shinglings we will need a way to create a family of hash functions. One way is to use a hash function
and a code similar to the following.
```
# Implement a family of hash functions. It hashes strings and takes an
# integer to define the member of the family.
# Return a hash function parametrized by i
import hashlib
def hashFamily(i):
resultSize = 8 # how many bytes we want back
maxLen = 20 # how long can our i be (in decimal)
salt = str(i).zfill(maxLen)[-maxLen:]
def hashMember(x):
return hashlib.sha1(x + salt).digest()[-resultSize:]
return hashMember
```
Note that this code is an overkill because we use a cryptographic hash function, which can be very
slow, even though it is not needed to be as secure. However we will use it because we are too lazy to install some 
external hash library.
### Dependencies
1. [Pandas](https://pandas.pydata.org/docs/getting_started/index.html#getting-started)


## PySpark Implementation of LSH
Same principle but using MapRedue functions and key-value programming style to process data.
### Dependencies
1. [PySpark](https://spark.apache.org/docs/latest/api/python/index.html)
2. [Find Spark](https://github.com/minrk/findspark)
