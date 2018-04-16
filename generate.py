from collections import defaultdict
import random
import argparse


def random_choices(population, cum_weights):
    size = len(population)
    random_count = random.randint(1, cum_weights[size - 1])
    i = 0
    for i in range(size):
        if(cum_weights[i] >= random_count):
            return population[i]


def gen_phrase(frequencies, phrase_length, seed):
    phrase = ''
    token1 = '$'
    token2 = '$'
    if not seed == '':
        phrase = seed
        token2 = seed
    if frequencies[token1][token2] == {}:
        print('начальное слово отсутствует в модели')
        return ''
    for i in range(phrase_length):
        token_list = []
        weights = []
        sum_weights = 0
        for j in frequencies[token1][token2]:
            token_list += [j]
            sum_weights += frequencies[token1][token2][j]
            weights.append(sum_weights)
        token3 = random_choices(token_list, weights)
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
frequencies = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
for token1, token2, token3, count in model:
    frequencies[token1][token2][token3] = count
phrase = gen_phrase(frequencies, length, seed)
if args.output == 'stdout':
    print(phrase)
else:
    with open(args.output, 'w', encoding="utf-8") as fout:
        print(phrase, file=fout)
