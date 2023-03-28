import json
import os


class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None

    def __init__(self, file_path: str):
        self.__data_file = file_path
        self.__connect()

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        # тут должен быть код для установки файла
        self.__data_file = value
        self.__connect()

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """
        if not os.path.isfile("filename.json"):
            raise FileNotFoundError("Файл filename.json отсутствует")
        try:
            with open(self.__data_file, 'r', encoding='windows-1251') as file:
                json_reader = json.load(file)
                print(len(json_reader))
                for i in json_reader:
                    if i.get('name') < 0:
                        print('Something wrong')
                    else:
                        raise Exception
        except Exception:
            print('Файл filename.json поврежден')

    def insert(self, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        with open('filename.json', 'a', encoding="UTF-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def select(self, query):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        pass

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        pass

# if __name__ == '__main__':
# df = Connector('df.json')
#
# data_for_file = {'id': 1, 'title': 'tet'}
#
# df.insert(data_for_file)
# data_from_file = df.select(dict())
# assert data_from_file == [data_for_file]
#
# df.delete({'id':1})
# data_from_file = df.select(dict())
# assert data_from_file == []
