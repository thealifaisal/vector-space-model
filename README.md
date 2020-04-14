# Vector Space Model

Documents and queries are represented as vectors.

![Vector-1](https://wikimedia.org/api/rest_v1/media/math/render/svg/6568769b5001c6040e121596945b7e419dddb4da)
![Vector-2](https://wikimedia.org/api/rest_v1/media/math/render/svg/d5b3e7c8ef051ef2c6411266ea1a490d36c8011e)

Each dimension corresponds to a separate term. If a term occurs in the document, its value in the vector is non-zero. Several different ways of computing these values, also known as (term) weights, have been developed. One of the best known schemes is tf-idf weighting (see the example below).

The definition of term depends on the application. Typically terms are single words, keywords, or longer phrases. If words are chosen to be the terms, the dimensionality of the vector is the number of words in the vocabulary (the number of distinct words occurring in the corpus).

Vector operations can be used to compare documents with queries.

## Algorithm

### Overview

In VSM, all the documents are parsed and tokenized and then lemmatized. A bag of words is formed.
N number of document-vectors are created having dimension of size length of bag-of-words.
Each vector has tf-idf value in each of its dimensions.
When query is entered, it is also parsed and tokenized and then lemmatized. A query vector has tf-idf values
in its dimensions. Dot product is calculated between the query and every document vector.
The scalar product found is then divided by product of norm of query and document vector to find the cosine angle.
If the cosine angle is closer to cos(0)=1 and greater then cut-off the such a document is relavent and is added to result set.

### Detailed

1 - When a program starts, it will check for a cache file named tf-idf.xlsx in the folder named 'out'.
If the cache is found, then it will load the excel file into the memory and goes to step - 9, else to step - 2. 

2 - Read a speech file and pass it into the homemade tokenizer that returns a list of tokens. 
From the tokens list, each token is then passed to nltk's lemmatizer and returned lemmas 
are added to a set as keys with their value being term-frequency for that document.
Similarly, all the documents are processed and a list named 'lemma-list' of sets is created. 
Each set represents a document and has lemmas as keys and value as term-frequency.

3 - By iterating over each set in lemma-list, we access each key and check whether it is in the bag-of-words.
if it’s not in bag-of-words it is appended to it else ignored. After doing this, we have a bag-of-words that
has lemmas from the entire corpora.

4 - size of bag-of-words is calculated to len-of-bag-of-words.

5 - by using openpyxl library, a workbook is created and a sheet is created.

6 - a loop iterates for len-of-bag-of-words times to cover the rows of sheet.
accesses a word from bag-of-words and writes into sheet's column 1.

7 - an inner loop iterates over each set in lemma-list to cover the columns.
a set is accessed and a word from outer loop is searched in set to get the term-frequency for that doc.
the tf is written to document column in sheet and if tf is non zero document-freqeuncy is incremented
and this works until all document set is visited and writes df to df-column (59) and calculates Inverse-Doc-Frequency(idf)
by the formula log10(N/df) where N is the size of corpora and writes idf to idf-column (60).
another inner loop re-iterates over the document columns to multiply the tf in those cells with idf to calculate tf-idf 
and placing tf-idf in those columns. 
Similarly, the outer loop iterated for every word in bag-of-words.

8 - Since, the sheet has all the document vectors prepared and the bag-of-words.
lemma-list and bag-of-words are cleared to save memory and the sheet is saved to disk.

9 - After that, read a query, create tokens then lemmas, and a set of lemmas for that query will be created
with lemmas as keys and tf as values.

10 - a loop iterates for len-of-bag-of-words and fetches a word in each iteration from the 1st column in sheet.
the word is checked query-lemma-set, 
if word is in the set, then its tf is fetched from the set and multiplied with idf from
the idf column and placed in i-th row at query column.
if word is not in the set, then tf is assigned 0 and placed in i-th row at query column.
thus, when loop finishes, a query vector is prepared.

Now to fetch the result-set,

11 - a main loop iterates for every document column in sheet.
and an inner loop iterates for every word in sheet, and at each iteration the tf-idf values from the query and doc column
are multiplied and added to scalar_product, and also from query column the tf-idf value is squared and added to norm-of-query-vector,
and same from document column the tf-idf value is squared and added to norm-of-document-vector.
outside the inner loop, norm-of-document-vector and norm-of-query-vector are both passed in sqrt() to find the respective norm values.
and scalar_product is also found of two vectors. Now to find the angle between the two vectors.
angle is found by dividing the scalar_product by the product of two norms.
if the angle is gretaer than the alpha, then the document is added to the result set.
Similary, this is done for every iteration of main loop.

12 - Sort the result-set by angles in descending order and write the result set to file.
