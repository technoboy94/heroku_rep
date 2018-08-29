import itertools as it
from pymarkovchain import MarkovChain
from nltk.tokenize import word_tokenize
from flask import Flask
from flask import request
import json

signs = {
    'gemini': 'Близнецы', 'cancer': 'Рак', 'leo': 'Лев', 'libra': 'Весы', 'pisces': 'Рыбы',
    'sagittarius': 'Стрелец', 'scorpio': 'Скорпион', 'taurus': 'Телец', 'virgo': 'Дева',
    'capricorn': 'Козерог', 'aries': 'Овен', 'aquarius': 'Водолей'
}


def read_horoscopes(tokenize: bool = False):
    horoscopes_by_sign = {}
    for sign in signs:
        with open('data/horoscopes/horoscope_{}.txt'.format(sign), encoding='utf-8') as horoscopes:
            if tokenize:
                horoscopes_by_sign[sign] = [' '.join(word_tokenize(line.split('.')[2])) for line in
                                            horoscopes.readlines()]
            else:
                horoscopes_by_sign[sign] = horoscopes.readlines(line.split('.')[2].lower())
    unified_horoscopes = it.chain.from_iterable(horoscopes_by_sign.values())
    return '\n'.join(unified_horoscopes)


def get_markov_chain_horoscopes(tokenize: bool = False):
    unified_horoscopes = read_horoscopes(tokenize)
    chain = MarkovChain()
    chain.generateDatabase(unified_horoscopes, n=2, sentenceSep='[\n]')
    return chain


def get_top_words(chain: MarkovChain, n: int):
    sorted_by_frequency = sorted(chain.db[('',)].items(), key=lambda t: (t[1], t[0]), reverse=True)
    return [x[0] for x in sorted_by_frequency][:n]


def generate_horoscope_with_first_word(chain: MarkovChain, first_word: str):
    return chain.generateStringWithSeed(first_word)


def generate_horoscope(chain: MarkovChain):
    return chain.generateString()


'''from astrolog_backend.astrolog import *

chain = get_markov_chain_horoscopes(True)
print(get_top_words(chain,10))
print(generate_horoscope(chain))
print(generate_horoscope_with_first_word(chain,"Звезды"))'''

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST', 'PUT'])
def api_root():
    a = request.values
    chain = get_markov_chain_horoscopes(True)
    a = generate_horoscope_with_first_word(chain, a['name'])
    a = {'text': a}
    return json.dumps(a, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True)