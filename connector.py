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
        if not os.path.isfile(self.data_file):
            file = open("filename.json", "w+")
            file.write("empty_list = []")
            file.close()
            raise FileNotFoundError(f"Файл {self.data_file} отсутствует")
        with open(self.__data_file, 'r', encoding="utf8") as file:
            json_reader = json.load(file)
            if not isinstance(json_reader, list):
                raise Exception('Файл должен содержать список')

    def insert(self, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        with open(self.__data_file, 'w', encoding="UTF-8") as file:
            json.dump([i.to_dict() for i in data], file, indent=4, ensure_ascii=False, skipkeys=True, sort_keys=True)

    def select(self, query):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        result = []
        with open(self.__data_file, 'r', encoding="UTF-8") as file:
            data = json.load(file)
        for item in data:
            for key, value in query.items():
                if item.get(key) == value:
                    result.append(item)
        return result

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        with open(self.__data_file, 'r', encoding="UTF-8") as file:
            data = json.load(file)
        if not query:
            return data
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
