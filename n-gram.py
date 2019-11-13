#Shadow Pritchard
import string
import math
import random
from itertools import permutations
import numpy as np
#normalizes to the scale of input.
def normalize(l, norm_scale = 1):
    tot = 0
    for i in l:
        tot+= i
    if tot == 0:
        return l
    return [(x/tot)*norm_scale for x in l]

#text is list of words
#n is length of sentence to generate
def word_generator(text, n = 1, length = 100):
    sentence = ['']*n
    possibilities = []
    probablities = []
    words = set()
    for t in text:
        words.update(set(t.split()))
    words = list(words)
    for _ in range(0, length):
        possibilities, probablities = get_possibles(text, sentence[-n:], words)
        sentence.append(str(''.join(np.random.choice(possibilities, p = probablities) ) ) )
    for i in range(n):
        sentence.remove("")
    return ' '.join(sentence)

#word generator helper function
def get_possibles(t, prev_words, words):
    result = []
    probs = []
    n = len(prev_words)
    if prev_words:
        for text in t:
            text = text.split()
            text = ['']*n + text
            for word in range(0, len(text) - n):
                if text[word:word + n] == prev_words:
                    if word + n + 1 < len(text):
                        result += [ text[word + n + 1] ] 
                        probs +=[1]
        if not result:
            return get_possibles(t, prev_words[1:], words)
    probs = normalize(probs, 99)
    other_words_probs = []
    for _ in words:
        other_words_probs += [1]
    normalize(other_words_probs, 1)
    probs = normalize(probs + other_words_probs, 1)
    result += words
    return result, probs

#not used but cool. takes hecking long to process but builds a dictionary 
#of all words and all possible words before them and the probabilities of
#word
def build_dict(text, n):
    result = {}
    words = set()
    for t in text:
        words.update(set(t.split()))
    words = list(words)
    count = 0
    for word in words:
        result[word] = {}
        for other_words in permutations(words, n):
            result[word][other_words] = [word_preceding_prob(text, word, list(other_words), len(words))]
        print(word, ": ", count, 'num left:', len(words) - count)
        count +=1

#gets probability of l_word given preceding words in the list_texts
def word_preceding_prob(list_texts, l_word, preceding, length = 10):
    assert preceding
    l_freq = 0
    prec_freq = 0
    length = 0
    for text in list_texts:
        text = text.split()
        length += len(text)
        for i in range(len(preceding) - 1, len(text)):  
            if text[i] == l_word:
                l_freq += 1
                if str(text[i - len(preceding):i] ) == str( preceding ):
                    #print(str(text[i - len(preceding):i] ), str( preceding ))
                    prec_freq +=1
    if l_freq == 0:
        return 0.1
    elif prec_freq == 0:
        return l_freq / length
    return prec_freq / l_freq

#probability that text is either from pos or neg
def word_lang_prob(text, pos, neg, n = 1):
    pos_prob = 0
    neg_prob = 0
    for i in range(n, len(text) ):
        pos_prob +=math.log( word_preceding_prob(pos, text[i], text[i-n:i]) )
        neg_prob += math.log ( word_preceding_prob(neg, text[i], text[i-n:i]) )
    # print(pos_prob, neg_prob)
    return normalize( [math.pow(math.e, pos_prob), math.pow(math.e, neg_prob) ])

#barely used in the final program but cool nonetheless. Just finds 
#probability that l_letter is preceded by preceding letters in 
#list_text
def char_preceding_prob(list_texts, l_letter, preceding):
    assert len(preceding) > 0
    l_frequency = 0
    prec_freq = 0
    for text in list_texts:
        for i in range(len(preceding) - 1, len(text)):
            if text[i] == l_letter:
                l_frequency +=1
                if text[i - len(preceding):i] == preceding:
                    prec_freq +=1
    if l_frequency == 0 or prec_freq == 0:
        return 0.01
    return prec_freq / l_frequency

#uses characters to determine probability of text being from
#pos or neg i.e. lang1 or lang2. 
def char_lang_prob(text, pos, neg, n = 1):
    pos_prob = 0
    neg_prob = 0
    for i in range(n, len(text) ):
        pos_prob +=math.log( char_preceding_prob(pos, text[i], text[i-n:i]) )
        neg_prob += math.log( char_preceding_prob(neg, text[i], text[i-n:i]) )
    return normalize( [math.pow(math.e, pos_prob), math.pow(math.e, neg_prob) ])

#gets one input set and splits into positive and negitive and makes test sets for both
def get_one_text():
    tr = str.maketrans("", "", string.punctuation)
    s = open('C:\\Users\\swpsh\\OneDrive\\Documents\\Python stuff\\n-gram\\imdb_labelled.txt')
    in_file = s.read().splitlines()

    fil = in_file[:int(2*len(in_file) / 3 )] #gets first 2/3 of in_file to use as training
    
    in_file = in_file[-int(2*len(in_file) / 3 ): ] #last third of in_file to use as test
    test = [ (x[:-3], x[-1] ) for x in in_file]
    test_pos = [x[0].lower().translate(tr) for x in test if x[1] == '1']
    test_neg = [x[0].lower().translate(tr) for x in test if x[1] =='0']

    text = [(x[:-3],x[-1] ) for x in fil ]
    
    pos_text = [x[0].lower().translate(tr) for x in text if x[1] == '1']

    neg_text = [x[0].lower().translate(tr) for x in text if x[1] == '0']

    return pos_text, neg_text, test_pos, test_neg

#gets two files, imdb and amazon, and makes train and test sets for them
def get_two_text():
    tr = str.maketrans("", "", string.punctuation)
    s = open('.\\imdb_labelled.txt')
    fil = s.read().splitlines()

    in_file = fil[:int((9/10) *len(fil))]
    test_file = fil[int((9/10) *len(fil)):]
    test1 = [x.lower().translate(tr)[:-3] for x in test_file]

    text1 = [x.lower().translate(tr)[:-3] for x in in_file]

    s = open('.\\amazon_cells_labelled.txt')
    fil = s.read().splitlines()
    in_file = fil[:int((9/10) *len(fil))]
    test_file = fil[int((9/10) *len(fil)):]
    test2 = [x.lower().translate(tr)[:-3] for x in test_file]

    text2 = [x.lower().translate(tr)[:-3] for x in in_file]

    return text1, text2, test1, test2

if __name__ == '__main__':
    
    lang1, lang2, test1, test2 = get_two_text()
    # print(char_lang_prob(test1[0], lang1, lang2, n = 3))
    result = [0,0]
    c_result = [0,0]
    leng = len(test2)
    for word in test2:
        res = word_lang_prob(word.split(), lang1, lang2, n = 3)
        c = char_lang_prob(word, lang1, lang2, n = 3)
        c_result[0], c_result[1] = c_result[0] + c[0], c_result[1] + c[1]
        result[0], result[1] = result[0] + res[0], result[1] + res[1]
    print('word: ' ,result[0]/leng, result[1]/leng)
    print('char: ', c_result[0]/leng, c_result[1]/leng) 

    # print(word_generator(lang1 + test1, n = 3, length= 10) )