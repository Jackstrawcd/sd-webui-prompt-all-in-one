import os
from pathlib import Path
import json
import time

class storage:
    storage_path = ''
    def __init__(self):
        pass

    def __get_storage_path(self):
        self.get_storage_path = os.path.join(Path().absolute(), 'physton-prompt')
        if not os.path.exists(self.get_storage_path):
            os.makedirs(self.get_storage_path)
        return self.get_storage_path

    def __get_data_filename(self, key):
        return self.__get_storage_path() + '/' + key + '.json'

    def __get_key_lock_filename(self, key):
        return self.__get_storage_path() + '/' + key + '.lock'

    def __lock(self, key):
        file_path = self.__get_key_lock_filename(key)
        with open(file_path, 'w') as f:
            f.write('1')

    def __unlock(self, key):
        file_path = self.__get_key_lock_filename(key)
        if os.path.exists(file_path):
            os.remove(file_path)

    def __is_locked(self, key):
        file_path = self.__get_key_lock_filename(key)
        return os.path.exists(file_path)

    def __get(self, key):
        filename = self.__get_data_filename(key)
        if not os.path.exists(filename):
            return None
        with open(filename, 'r') as f:
            data = json.load(f)
        return data

    def __set(self, key, data):
        file_path = self.__get_data_filename(key)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def set(self, key, data):
        while self.__is_locked(key):
            time.sleep(0.01)
        self.__lock(key)
        try:
            self.__set(key, data)
            self.__unlock(key)
        except Exception as e:
            self.__unlock(key)
            raise e

    def get(self, key):
        return self.__get(key)

    def delete(self, key):
        file_path = self.__get_data_filename(key)
        if os.path.exists(file_path):
            os.remove(file_path)

    def __get_list(self, key):
        data = self.get(key)
        if not data:
            data = []
        return data

    # 向列表中添加元素
    def list_push(self, key, item):
        while self.__is_locked(key):
            time.sleep(0.01)
        self.__lock(key)
        try:
            data = self.__get_list(key)
            data.append(item)
            self.__set(key, data)
            self.__unlock(key)
        except Exception as e:
            self.__unlock(key)
            raise e

    # 从列表中删除和返回最后一个元素
    def list_pop(self, key):
        while self.__is_locked(key):
            time.sleep(0.01)
        self.__lock(key)
        try:
            data = self.__get_list(key)
            item = data.pop()
            self.__set(key, data)
            self.__unlock(key)
            return item
        except Exception as e:
            self.__unlock(key)
            raise e

    # 从列表中删除和返回第一个元素
    def list_shift(self, key):
        while self.__is_locked(key):
            time.sleep(0.01)
        self.__lock(key)
        try:
            data = self.__get_list(key)
            item = data.pop(0)
            self.__set(key, data)
            self.__unlock(key)
            return item
        except Exception as e:
            self.__unlock(key)
            raise e

    # 从列表中删除指定元素
    def list_remove(self, key, index):
        while self.__is_locked(key):
            time.sleep(0.01)
        self.__lock(key)
        data = self.__get_list(key)
        data.pop(index)
        self.__set(key, data)
        self.__unlock(key)

    # 获取列表中指定位置的元素
    def list_get(self, key, index):
        data = self.__get_list(key)
        return data[index]

    # 清空列表中的所有元素
    def list_clear(self, key):
        while self.__is_locked(key):
            time.sleep(0.01)
        self.__lock(key)
        try:
            self.__set(key, [])
            self.__unlock(key)
        except Exception as e:
            self.__unlock(key)
            raise e