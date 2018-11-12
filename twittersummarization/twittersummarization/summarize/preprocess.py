from py_translator import Translator
import enchant
from time import sleep
import random
import re
import json
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def translate(text):
    counter = 1
    checker = enchant.Dict("en_US")
    split_text = text.split(' ')
    words = []
    translator = Translator()
    for word in split_text:
        if word != '':
            if checker.check(word) and word != 'twitter':
                translated_word = translator.translate(text=word, dest='id', src='en').text 
                words.append(translated_word)
                if counter > 10:
                    delay_request(5,7)
                    counter = 1
            else:
                words.append(word.replace(' ',''))
    return " ".join(words)

def delay_request(lower, upper):
    print(random.uniform(lower, upper))
    sleep(random.uniform(lower, upper))

def remove_url(text):
    return re.sub(r'http\S+', '', text)

def convert_text_to_lowercase(text):
    return text.lower()

def remove_emoji(text):
    return re.sub(r'(^|\s)(:D|:\/|:\)+|;\)|:-\))(?=\s|[^[:alnum:]+-]|$)', '', text)


def spell_checker(text):
    words = text.split(' ')
    with open('spellchecker.json') as file_opened:
        text = file_opened.read()
    word_checker = json.loads(text)
    for idx in range(len(words)):
        if words[idx] in word_checker:
            words[idx] = word_checker[words[idx]]
    return " ".join(words)

def substitue_character(text):
    new_text = text.encode('ascii',errors='ignore').decode('utf-8', 'ignore')
    new_text = new_text.replace('\n', ' ')
    new_text = new_text.replace('?', ' ')
    new_text = new_text.replace('"', '')
    new_text = new_text.replace("'", '')
    new_text = re.sub(r'[.,\/!$%\^&\*;:{}=\`~()]', ' ', new_text)
    return new_text

def dwilingga(text):
    match = re.match(r'\w*(?=2(nya)?)', text)
    if match is not None:
        words = text.split(' ')
        for idx in range(len(words)):
            match_word = re.match(r'\w*(?=2(nya)?)', words[idx])
            if match_word is not None:
                words[idx] = words[idx].replace('2', '-' + match_word.group())
        return " ".join(words)
    return text

def remove_code_word(text):
    match = re.search(r'(?:[\d]+[\w]|[\w]+[\d])[\w\d]*', text)
    if match is not None:
        words = text.split(' ')
        for idx in range(len(words)):
            match_word = re.match(r'(?:[\d]+[\w]|[\w]+[\d])[\w\d]*', words[idx])
            match_hastag = re.match(r'(#[\w\d]*)', words[idx])
            if match_word is not None and match_hastag is None:
                words[idx] = ''
        return " ".join(words)
    return text

def prefix_fixing(text):
    match = re.search(r'\b[bkmpst][bcdfghjklmnpqrstvwxyz]', text)
    words = text.split(' ')
    if match is not None:
        for idx in range(len(words)):
            match_word = re.search(r'\b[bkmpst][bcdfghjklmnpqrstvwxyz]', words[idx])
            if match_word is not None:
                words[idx] = words[idx][0] + 'e' + words[idx][1:]
    match3 = re.search(r'\b[p][bcdefghjklmnpqstvwxyz]', text)
    if match3 is not None:
        for idx in range(len(words)):
            match_word = re.search(r'\b[p][bcdfghjklmnpqstvwxyz]', words[idx])
            if match_word is not None:
                words[idx] = words[idx][0] + 'i' + words[idx][1:]
    match2 = re.search(r'\b[d][bcdefghjklmnpqrstvwxyz]', text)
    if match2 is not None:
        for idx in range(len(words)):
            match_word = re.search(r'\b[d][bcdfghjklmnpqrstvwxyz]', words[idx])
            if match_word is not None:
                words[idx] = words[idx][0] + 'i' + words[idx][1:]
    return " ".join(words) if match is not None or match2 is not None or match3 is not None else text

def rank_word(text):
    match = re.match(r'(?!ke)\d*\b', text)
    number_dict = {
        '1': 'satu',
        '2': 'dua',
        '3': 'tiga',
        '4': 'empat',
        '5': 'lima',
        '6': 'enam',
        '7': 'tujuh',
        '8': 'delapan',
        '9': 'sembilan'
    }
    if match is not None:
        words = text.split(' ')
        for idx in range(len(words)):
            match_word = re.match(r'(?!ke)\d*\b', words[idx])
            if match_word is not None:
                words[idx] = words[idx].replace('2', '-' + match_word.group())
        return " ".join(words)
    return text

def remove_mention(text):
    return re.sub(r'@[\w\d_]+', '', text)

def cut_to_many_character(text):
    list_of_char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    list_of_vocal = ['a', 'i', 'u', 'e', 'o']
    new_text = text
    for idx in range(len(list_of_vocal)):
        for jdx in range(idx, len(list_of_vocal)):
            pattern = r'\b' + list_of_vocal[idx] + list_of_vocal[jdx] + r'\b'
            pattern_2 = r'\b' + list_of_vocal[jdx] + list_of_vocal[idx] + r'\b'
            pattern_3 = r'\b[bcdfghjklmnpqrstvwxyz][bcdfghjklmnpqrstvwxyz]\b'
            new_text = re.sub(pattern, '', new_text)
            new_text = re.sub(pattern_2, '', new_text)
            new_text = re.sub(pattern_3, '', new_text)
    for character in list_of_char:
        pattern = character + r'{3,}'
        pattern_2 = character + r'{2,}\b'
        new_text = re.sub(pattern, character, new_text)
        new_text = re.sub(pattern_2, character, new_text)
    new_text = re.sub(r'(wk){2,}', '', new_text)
    new_text = re.sub(r'(ha){2,}', '', new_text)
    new_text = re.sub(r'(he){2,}', '', new_text)
    new_text = re.sub(r'(hi){2,}', '', new_text)
    new_text = re.sub(r'(bla){2,}', '', new_text)
    new_text = re.sub(r'\b[a-z]\b', '', new_text)
    new_text = re.sub(r'\b(kw)\b', '', new_text)
    new_text = re.sub(r'\b(ha)\b', '', new_text)
    new_text = re.sub(r'\b(he)\b', '', new_text)
    new_text = re.sub(r'\b(bla)\b', '', new_text)
    new_text = re.sub(r'\b(hi)\b', '', new_text)
    new_text = re.sub(r'\b(co)\b', '', new_text)
    new_text = re.sub(r'\b(id)\b', '', new_text)
    new_text = re.sub(r'\b(com)\b', '', new_text)
    new_text = re.sub(r'\b(org)\b', '', new_text)
    new_text = re.sub(r'\b(net)\b', '', new_text)
    new_text = re.sub(r'\b(gov)\b', '', new_text)
    new_text = remove_mention(new_text)
    new_text = remove_code_word(new_text)
    new_text = dwilingga(new_text)
    new_text = rank_word(new_text)
    new_text = prefix_fixing(new_text)
    new_text = re.sub(r' {2,}', ' ', new_text)
    return new_text

def remove_stop_words(sentence):
    factory = StopWordRemoverFactory().create_stop_word_remover()
    return factory.remove(sentence)

def stemming(sentence):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    return stemmer.stem(sentence)

def preprocess_text(text):
    new_text = substitue_character(text)
    new_text = convert_text_to_lowercase(new_text)
    new_text = remove_url(new_text)
    new_text = remove_emoji(new_text)
    new_text = cut_to_many_character(new_text)
#     new_text = translate(new_text)
    new_text = remove_stop_words(new_text)
    new_text = spell_checker(new_text)
    new_text = stemming(new_text)
    new_text = new_text.replace('#', '')
    return new_text