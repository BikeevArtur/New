from collections import defaultdict
import random
import argparse


def gen_phrase(dict, phrase_length, seed):
    phrase = ''
    token1 = '$'
    token2 = '$'
    if not seed == '':
        phrase = seed
        token2 = seed
    if dict[token1, token2] == {}:
        print('начальное слово отсутствует в модели')
        return ''
    for i in range(phrase_length):
        list = []
        for i in dict[token1, token2]:
            list += [i]*dict[token1, token2][i]
        token3 = random.choice(list)
        if token3 in ':;.,!?' or token2 == '$':
            phrase = '{0}{1}'.format(phrase, token3)
            if token3 in '.!?':
                return phrase
        else:
            phrase = '{0} {1}'.format(phrase, token3)
        token1 = token2
        token2 = token3
    phrase += '.'
    return phrase.capitalize()


def read(corpus):
    with open(corpus, 'r') as fout:
        for line in fout:
            l = line.encode('cp1251').decode('utf-8')
            l = l.split()
            yield(l[0], l[1], l[2], int(l[3]))


parser = argparse.ArgumentParser(description = 'генератор случайных фраз на основе текста')

parser.add_argument("--model", help = 'Путь к файлу, из которого загружается модель')
parser.add_argument("--length", type = int, default = 10, help = 'Длина (количество слов и знаков препинания), '
                                                                         'по умолчанию 10')
parser.add_argument("--seed", default = '', help = 'Начальное слово, если не указано, выбирается случайное')
parser.add_argument("--output", default = 'stdout', help = 'Файл, куда будет записан результат, если не указан, stdout')
args = parser.parse_args()

seed = args.seed
length = args.length
model = read(args.model)
Dict = defaultdict(lambda: defaultdict(lambda: 0))
for token1, token2, token3, count in model:
    Dict[token1, token2][token3] = count
phrase = gen_phrase(Dict, length, seed)
if args.output == 'stdout':
    print(phrase)
else:
    with open(args.output, 'w', encoding="utf-8") as fout:
        print(phrase, file=fout)
