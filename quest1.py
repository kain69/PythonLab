import json
import collections
import operator
import threading
import multiprocessing.dummy


# загрузить словарь
def loadJson():
    jDict = json.load(open('db.json', 'r'))
    return jDict.get('peoples')  # возвращает список со словарями


# топ 5 по сложности предмета
def top5difficult():
    peoples = loadJson()
    subjectAndMark = collections.Counter()  # сумма оценок по предметам
    subjectAndAverage = {}
    for people in peoples:
        for subject in people['subject']:
            subjectAndMark[subject['name']] += (subject['mark'])  # добавить к предмету его оценки

    for names in list(subjectAndMark.keys()):
        subjectAndAverage[names] = subjectAndMark[names] / 5  # найти среднюю оценку

    answerTupple = sorted(subjectAndAverage.items(), key=operator.itemgetter(1))  # создать тапл и отсортировать его
    print('\n10 самых трудных предметов:')
    for elem in answerTupple[:5]:  # вывод
        print('{p[0]} ({p[1]})'.format(p=elem))


# топ 5 по успеваемости
def top5performance():
    peoples = loadJson()
    nameAndMark = collections.Counter()  # сумма оценок ученика
    nameAndAverage = {}
    for people in peoples:
        for subject in people['subject']:
            nameAndMark[people['name']] += (subject['mark'])  # добавить к имени его оценки

    for names in list(nameAndMark.keys()):
        nameAndAverage[names] = nameAndMark[names] / 5  # найти среднюю успеваемость

    answerTupple = sorted(nameAndAverage.items(), key=operator.itemgetter(1),
                          reverse=True)  # создать тапл и отсортировать его
    print('\n10 самых успешных учеников:')
    for elem in answerTupple[:5]:  # вывод
        print('{p[0]} ({p[1]})'.format(p=elem))


# топ 5 по пропускам
def top5leaves():
    peoples = loadJson()
    nameAndMark = collections.Counter()  # сумма пропусков ученика
    for people in peoples:
        for subject in people['subject']:
            nameAndMark[people['name']] += (subject['leave'])  # добавить к имени его пропуски

    answerTupple = sorted(nameAndMark.items(), key=operator.itemgetter(1),
                          reverse=True)  # создать тапл и отсортировать его
    print('\n10 самых лютых прогульщиков:')
    for elem in answerTupple[:5]:  # вывод
        print('{p[0]} ({p[1]})'.format(p=elem))


def linear():
    top5difficult()
    top5performance()
    top5leaves()


def thread():
    thread1 = threading.Thread(target=top5difficult())
    thread2 = threading.Thread(target=top5performance())
    thread3 = threading.Thread(target=top5leaves())
    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()


def process():
    pool = multiprocessing.dummy.Pool()
    pool.map(lambda f: f(), [top5difficult])
    pool.map(lambda f: f(), [top5performance])
    pool.map(lambda f: f(), [top5leaves])
    pool.close()
    pool.join()


# Генераторы
# топ 5 по сложности предмета
def gen_top5difficult():
    peoples = loadJson()
    subjectAndMark = collections.Counter()  # сумма оценок по предметам
    subjectAndAverage = {}
    for people in peoples:
        for subject in people['subject']:
            subjectAndMark[subject['name']] += (subject['mark'])  # добавить к предмету его оценки

    for names in list(subjectAndMark.keys()):
        subjectAndAverage[names] = subjectAndMark[names] / 5  # найти среднюю оценку

    answerTupple = sorted(subjectAndAverage.items(), key=operator.itemgetter(1))  # создать тапл и отсортировать его
    print('\n10 самых трудных предметов:')
    for elem in answerTupple[:5]:  # вывод
        yield elem


# топ 5 по успеваемости
def gen_top5performance():
    peoples = loadJson()
    nameAndMark = collections.Counter()  # сумма оценок ученика
    nameAndAverage = {}
    for people in peoples:
        for subject in people['subject']:
            nameAndMark[people['name']] += (subject['mark'])  # добавить к имени его оценки

    for names in list(nameAndMark.keys()):
        nameAndAverage[names] = nameAndMark[names] / 5  # найти среднюю успеваемость

    answerTupple = sorted(nameAndAverage.items(), key=operator.itemgetter(1),
                          reverse=True)  # создать тапл и отсортировать его
    print('\n10 самых успешных учеников:')
    for elem in answerTupple[:5]:  # вывод
        yield elem


# топ 5 по пропускам
def gen_top5leaves():
    peoples = loadJson()
    nameAndMark = collections.Counter()  # сумма пропусков ученика
    for people in peoples:
        for subject in people['subject']:
            nameAndMark[people['name']] += (subject['leave'])  # добавить к имени его пропуски

    answerTupple = sorted(nameAndMark.items(), key=operator.itemgetter(1),
                          reverse=True)  # создать тапл и отсортировать его
    print('\n10 самых лютых прогульщиков:')
    for elem in answerTupple[:5]:  # вывод
        yield elem


def generator():
    answer1 = gen_top5difficult()
    for i in range(5):
        print(next(answer1))
    answer2 = gen_top5performance()
    for i in range(5):
        print(next(answer2))
    answer3 = gen_top5leaves()
    for i in range(5):
        print(next(answer3))


print('\n================================')
print('\nОднопоточность:')
linear()
print('\n================================')
print('\nМногопоточность:')
thread()
print('\n================================')
print('\nМультипроцессность:')
process()
print('\n================================')
print('\nГенераторы:')
generator()
