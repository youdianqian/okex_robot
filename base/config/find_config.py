#coding=utf-8
import configparser

class ReadIni(object):
    # 为空时设定一个默认值
    # node为配置文件中的标识，可以设置多个分类配置信息
    def __init__(self, file_nam=None, node=None):
        if file_nam == None:
            self.file_name = r'G://gui_exchange//base//config//config.ini'
        if node == None:
            self.node = 'apikey'
        else:
            self.node = node
        self.cf = configparser.ConfigParser() 


    # 获取配置文件中的信息
    def get_value(self, key):
        self.cf.read(self.file_name)
        data = self.cf.get(self.node, key)
        return data

    # 更改配置文件中的信息
    def set_value(self, key, value):
        self.cf.read(self.file_name)
        self.cf.set(self.node, key, value)
        self.cf.write(open(r"G://gui_exchange//base//config//config.ini", "w"))

if __name__ == '__main__':
    read_init = ReadIni()
  #  print(read_init.get_value('api_key'))
  #  read_init.set_value('api_key', '1111')