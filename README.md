# Algorithm

Read a speech file and pass it into the homemade tokenizer that returns a list of tokens. The tokens list
is then passed to nltk's lemmatizer that returns a list of lemmas.
A unique list of lemmas will be created from the corpus which is called bag of words.
Length of bag of words will be saved.

The lemmas from the list will be written to an Excel file at column 0.
Now 56 columns for documents (tf), 1 column for a query (tf), 1 column for Document Frequency (df), 1
column for Inverse Document Frequency (idf), 56 columns for document's tf*idf, 1 column for query's
tf*idf will be created.

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

After that, read a query, create tokens then lemmas, write it into tf col for query in Excel, calculate tf*idf
of query.

Now select a tf*idf doc column and multiple with tf*idf query, sum all those products if sum < alpha, add
that document I’d to result set. Do this for all tf*idf doc columns.