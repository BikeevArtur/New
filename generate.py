from collections import defaultdict
import random


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
            yield(l[0], l[1], l[2])


seed = ''
length = 30
Trigrams = Read('словарь')
Dict = defaultdict(lambda: defaultdict(lambda: 0))
for t1, t2, t3 in Trigrams:
    Dict[t1, t2][t3] += 1
k = GenPhrase(Dict, length, seed)
print(k)