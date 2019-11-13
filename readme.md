Program reads in the data set and uses an n-gram algorithm to determine probability that an input sentence belongs to one of the given datasets

If simply run, program uses a set of data from imdp and a set of data from amazon, and tests with a subset of the data set from amazon. 
Uses n = 3 for character n-gram and word n-gram and the probabilities of the text belonging to imdb is printed first, with amazon second. 
Output should be formatted as follows:
word:  0.1 0.9
char:  0.3 0.7
where .1 is probability text belongs to imdb and .9 it belongs to amazon using n-gram on words, and the char: row is the result of the character n-gram for imdb and amazon respectively.

## Below is the readme for the data sets used:


This dataset was created for the Paper 'From Group to Individual Labels using Deep Features', Kotzias et. al,. KDD 2015
Please cite the paper if you want to use it :)

It contains sentences labelled with positive or negative sentiment, extracted from reviews of products, movies, and restaurants

=======
Format:
=======
sentence \t score \n


=======
Details:
=======
Score is either 1 (for positive) or 0 (for negative)	
The sentences come from three different websites/fields:

imdb.com
amazon.com
yelp.com

For each website, there exist 500 positive and 500 negative sentences. Those were selected randomly for larger datasets of reviews. 
We attempted to select sentences that have a clearly positive or negative connotaton, the goal was for no neutral sentences to be selected.



For the full datasets look:

imdb: Maas et. al., 2011 'Learning word vectors for sentiment analysis'
amazon: McAuley et. al., 2013 'Hidden factors and hidden topics: Understanding rating dimensions with review text'
yelp: Yelp dataset challenge http://www.yelp.com/dataset_challenge
