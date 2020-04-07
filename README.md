# Algorithm

Read a speech file and pass it into the homemade tokenizer that returns a list of tokens. The tokens list
is then passed to nltk's lemmatizer that returns a list of lemmas.
A unique list of lemmas will be created from the corpus which is called bag of words.
Length of bag of words will be saved.

The lemmas from the list will be written to an Excel file at column 1.
Now 56 columns for documents (tf), 1 column for a query (tf), 1 column for Document Frequency (df), 1
column for Inverse Document Frequency (idf), and re-iterate over the 56 columns to multiply tf and idf
to the document columns. 

Now again read each document one by one, for specific cell(token,doc-col) write the tf of that token.
This can be done by creating a set structure with key as a token and value as it’s count. Once the
document is scanned our set is ready. Now write that set into the doc-col and if there is no match
between bag of words and our set, write 0 for those tokens in Excel file.

Once all documents are scanned our doc-cols are filled.

Now for every token in Excel, go through each tf column, if not 0 increment the count and place the
count in respective df column.

Now calculate idf for that df by using log(N/df) and save it into the respective idf column. Now calculate
tf*idf for for each document, save it into the columns. Our work for one word has been done. Now do
this document preparing for each word.

After that, read a query, create tokens then lemmas, write it into tf col for query in Excel, calculate tfxidf
of query.

Now select a tfxidf doc column and multiple with tfxidf query, sum all those products if sum < alpha, add
that document id to result set. Do this for all tfxidf doc columns.

Since a cache excel file has been created with tf*idf scores, the next time the program runs, it will check
a if a file is created and if it is created will check a certain, if flag is turned on that means computation has
been done, we just have to process the scores for the query which would reduce the time of the system being
available for general use.