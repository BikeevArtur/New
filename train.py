import re
from collections import defaultdict
import argparse


r_alphabet = re.compile(u'[а-яА-Я0-9-]+|[.,:;?!]+')


def gen_lines(corpus):
    with open(corpus, 'r') as fout:
        for line in fout:
            if args.lc:
                yield line.encode('cp1251').decode('utf-8').lower()
            else:
                yield line.encode('cp1251').decode('utf-8')


def gen_tokens(lines):
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token


def gen_trigrams(tokens):
    token1 = '$'
    token2 = '$'
    for token3 in tokens:
        yield token1, token2, token3
        if token3 in '.!?':
            yield token2, token3, '$'
            yield token3, '$', '$'
            token1 = '$'
            token2 = '$'
        else:
            token1 = token2
            token2 = token3


def Write(frequencies, corpus):
    with open(corpus, 'w', encoding="utf-8") as fout:
        for token1 in frequencies:
            for token2 in frequencies[token1]:
                for token3 in frequencies[token1][token2]:
                    count = frequencies[token1][token2][token3]
                    l = '{0} {1} {2} {3}'.format(token1, token2, token3, count)
                    print(l, file=fout)

parser = argparse.ArgumentParser(description = 'создание модели частот последовательностей слов на основе текста')

parser.add_argument("--input", help = 'Путь к файлу, из которого загружается текст', default = "stdin")
parser.add_argument("--model", help = 'Путь к файлу, в который сохраняется модель')
parser.add_argument("--lc", action = "store_true", help = 'Приведение текста к lowercase')
args = parser.parse_args()

if args.input == "stdin":
    line = input()
    tokens = line.split()
else:
    lines = gen_lines(args.input)
    tokens = gen_tokens(lines)
trigrams = gen_trigrams(tokens)
frequencies = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
for token1, token2, token3 in trigrams:
    frequencies[token1][token2][token3] += 1
Write(frequencies, args.model)
