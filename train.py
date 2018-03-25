import re
from collections import defaultdict
import argparse


r_alphabet = re.compile(u'[а-яА-Я0-9-]+|[.,:;?!]+')


def GenLines(corpus):
    with open(corpus, 'r') as fout:
        for line in fout:
            if args.lc:
                yield line.encode('cp1251').decode('utf-8').lower()
            else:
                yield line.encode('cp1251').decode('utf-8')


def GenTokens(lines):
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token


def TriGrams(tokens):
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


def Write(dict, corpus):
    with open(corpus, 'w', encoding="utf-8") as fout:
        for t1, t2 in dict:
            for t3 in dict[t1, t2]:
                count = Dict[t1, t2][t3]
                l = '{0} {1} {2} {3}'.format(t1, t2, t3, count)
                print(l, file = fout)

parser = argparse.ArgumentParser(description = 'создание модели частот последовательностей слов на основе текста')

parser.add_argument("--input", help = 'Путь к файлу, из которого загружается текст', default = "stdin")
parser.add_argument("--model", help = 'Путь к файлу, в который сохраняется модель')
parser.add_argument("--lc", action = "store_true", help = 'Приведение текста к lowercase')
args = parser.parse_args()

if args.input == "stdin":
    line = input()
    tokens = line.split()
else:
    lines = GenLines(args.input)
    tokens = GenTokens(lines)
trigrams = TriGrams(tokens)
Dict = defaultdict(lambda: defaultdict(lambda: 0))
for t1, t2, t3 in trigrams:
    Dict[t1, t2][t3] += 1
Write(Dict, args.model)
