from collections import defaultdict
import random
import argparse


def GenPhrase(dict, n, seed):
    phrase = ''
    t1 = '$'
    t2 = '$'
    if not seed == '':
        phrase = seed
        t2 = seed
    if dict[t1, t2] == {}:
        print('начальное слово отсутствует в модели')
        return ''
    for i in range(n):
        l = []
        for i in dict[t1, t2]:
            l += [i]*dict[t1, t2][i]
        t3 = random.choice(l)
        if t3 in ':;.,!?' or t2 == '$':
            phrase = '{0}{1}'.format(phrase, t3)
            if t3 in '.!?':
                return phrase
        else:
            phrase = '{0} {1}'.format(phrase, t3)
        t1 = t2
        t2 = t3
    phrase += '.'
    return phrase.capitalize()


def Read(corpus):
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
model = Read(args.model)
Dict = defaultdict(lambda: defaultdict(lambda: 0))
for t1, t2, t3, count in model:
    Dict[t1, t2][t3] = count
phrase = GenPhrase(Dict, length, seed)
if args.output == 'stdout':
    print(phrase)
else:
    with open(args.output, 'w', encoding="utf-8") as fout:
        print(phrase, file=fout)
