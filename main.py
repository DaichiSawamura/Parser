import os
from classes import *


def main():
    path = os.path.join('filename.json')

    keyword = input('Какую вакансию Вы ищите? ')

    hh = HH(keyword)
    sj = SuperJob(keyword)
    with open('filename.json', 'w', encoding="UTF-8") as file:
        for key, val in hh.get_request().items():
            file.write('{}:{}\n'.format(key, val))
    with open('filename.json', 'a+', encoding="UTF-8") as file:
        for key, val in sj.get_request().items():
            file.write('{}:{}\n'.format(key, val))
            info = file.read()
    return info


main()
