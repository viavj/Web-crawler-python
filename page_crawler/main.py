
# # word frequency counter



import requests  # for download data from web
from  bs4 import BeautifulSoup  # filter the data
import operator  # dictionary


def start(url):
    word_list = []  # blank file
    source_code = requests.get(url).text  # just clean text, without binary data, or something like that
    soup = BeautifulSoup(source_code, "html.parser")  # filter clean all html crap
    for post_text in soup.findAll('a', {'class': 'reference internal'}): # findAll (element, {property : name of property})
        content = post_text.string  # remove all html and get only text
        words = content.lower().split()  # convert toLower case, then split the content into separated words
        for each_word in words:
            word_list.append(each_word)
    clean_list(word_list)

def clean_list(word_list):
    clean_word_list = []
    for word in word_list:
        symbols_to_delete = '!@\#$%^&*()_+\'.,/'  # filter
        for i in range(len(symbols_to_delete)):
            word = word.replace(symbols_to_delete[i], ' ')  # give a space to not concat two words
        # after clean up in case if you might had words like ':)' or '+=' ... you gonna have an ampty string of two chars
            # in your list, so check before add it
        if len(word) > 0:
            # print(word)
            clean_word_list.append(word)
    create_dictionary(clean_word_list)

def create_dictionary(clean_word_list):
    word_count = {}
    for word in clean_word_list:
        if word in word_count:  # if is true
            word_count[word] += 1
        else:
            word_count[word] = 1
    for key, value in sorted(word_count.items(), key=operator.itemgetter(1)): # 'key' is an property, not the var we created -
        # in the loop, and operator is the one we imported
        print(key, value)

start('https://docs.djangoproject.com/en/1.9/')



