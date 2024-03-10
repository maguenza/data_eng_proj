# textClassify.py
'''
the following code takes Spotify podcast episode titles and descriptions and creates text classifications
we create dict counts of nouns and verbs
'''

import extract
import transform
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from collections import Counter

'''
we'll need to also count the words then pair it with tokenization
'''
# Define some text to tokenize and count words in
text = "This is a sample text to count words. This text has repeated words, so some words will have higher counts than others."

# Tokenize the text into individual words
words = word_tokenize(text)

# Count the number of occurrences of each word
word_counts = Counter(words)

# Print the word counts
for word, count in word_counts.items():
    print(f"{word}: {count}")

# how to combine the 2
tag_words = pos_tag(words)
tag_word_counts = Counter(tag_words)

for word, count in tag_word_counts.items():
    print(f"{word}: {count}")

if __name__ == '__main__':

client_id = '4cb9bf88a1844329886f8ab395c9dea0'
client_secret = 'e934c0e875434659b5efe6f4023c11dc'
base_url = 'https://api.spotify.com/v1/shows/'
show_id = '07SjDmKb9iliEzpNcN2xGD' #bill simmons podcast
# extract data
json_file = extract.get_request_results(client_id, client_secret, base_url, show_id)
# convert json_file to dataframe
load_df = transform.return_dataframe(json_file)

'''
potentially we update the dataframe with new columns for tokenization
'''
# tokenize the episode name then tag words
load_df['tokenized'] = load_df['name'].str.lower().apply(word_tokenize)
load_df['tagged'] = load_df['tokenized'].apply(pos_tag)

# we could then look for nouns and verbs
load_df['nouns'] = load_df['tagged'].apply(lambda x: [word for word, tag in x if tag in ['NN', 'NNS', 'NNP', 'NNPS']])
load_df['verbs'] = load_df['tagged'].apply(lambda x: [word for word, tag in x if tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']])

# but what about counts? we want that to be able to then create k clusters or find insights
# problem so far is that load_df['tokenized']'s value is a list, can't do counts because of this
# let's try this out next time, https://towardsdatascience.com/dealing-with-list-values-in-pandas-dataframes-a177e534f173
# the above doesn't work, but let's keep it for now

# this works so far
nouns = load_df['nouns'].tolist() #this makes a list of list, but type(count_nouns) finally is a list
list_nouns = [item for sublist in nouns for item in sublist] #this makes it a full list or flatten
count_nouns = Counter(list_nouns)

'''
the above is the same as this:
flat_list = []
for sublist in l:
    for item in sublist:
        flat_list.append(item)
'''

verbs = load_df['verbs'].tolist()
list_verbs = [item for sublist in verbs for item in sublist]
count_verbs = Counter(list_verbs)

#print it
for list_nouns, count_nouns in count_nouns.items():
    print(f"{list_nouns}: {count_nouns}")

for list_verbs, count_verbs in count_verbs.items():
    print(f"{list_verbs}: {count_verbs}")

# how about the episode descriptions?
# could probably do the same thing we did above and make new columns
# should probably make new dataframes for this?