import json
import time
from libs.utils import log


def save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)


class Model(object):
    @classmethod
    def db_path(cls):
        # print("db_path os" + os.path.abspath(__file__))
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def _new_from_dict(cls, d):
        m = cls({})
        for k, v in d.items():
            setattr(m, k, v)
        return m

    @classmethod
    def new(cls, form):
        m = cls(form)
        m.save()
        return m

    @classmethod
    def all(cls):
        """
        all 方法(类里面的函数叫方法)使用 load 函数得到所有的 models
        """
        path = cls.db_path()
        models = load(path)
        # 这里用了列表推导生成一个包含所有 实例 的 list
        # 因为这里是从 存储的数据文件 中加载所有的数据
        # 所以用 _new_from_dict 这个特殊的函数来初始化一个数据
        ms = [cls._new_from_dict(m) for m in models]
        return ms

    # todo 该函数已经修改,需要测试
    @classmethod
    def find_all(cls, **kwargs):
        all = cls.all()
        for key, value in kwargs.items():
            k, v = key, value
            ms = []
            for m in all:
                # 也可以用 getattr(m, k) 取值
                if v == m.__dict__[k]:
                    ms.append(m)
            all = ms
        return all

    # todo 该函数查询只查询满足最后一条记录的单个数据，需要修改
    @classmethod
    def find_by(cls, **kwargs):
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find_by(username='gua')
        """
        all = cls.all()
        for key, value in kwargs.items():
            k, v = key, value
            ms = []
            for m in all:
                # 也可以用 getattr(m, k) 取值
                if v == m.__dict__[k]:
                    ms.append(m)
            all = ms
        if all != None and all != []:
            return all[0]
        else:
            return None
        # all = cls.all()
        # for key, value in kwargs.items():
        #     k, v = key, value
        # for m in all:
        #     # 也可以用 getattr(m, k) 取值
        #     if v == m.__dict__[k]:
        #         return m
        # return None

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def delete(cls, id):
        models = cls.all()
        index = -1
        for i, e in enumerate(models):
            if e.id == id:
                index = i
                break
        # 判断是否找到了这个 id 的数据
        if index == -1:
            # 没找到
            pass
        else:
            obj = models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save(l, path)
            # 返回被删除的元素
            return obj

    def update(self, form, hard=False):
        for k, v in form.items():
            if hard or hasattr(self, k):
                setattr(self, k, v)
        # self.updated_time = int(time.time()) fixme
        self.save()

    @classmethod
    def upsert(cls, query_form, update_form, hard=False):
        ms = cls.find_by(**query_form)
        if ms is None:
            query_form.update(**update_form)
            ms = cls.new(query_form)
        else:
            ms.update(update_form, hard=hard)
        return ms

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def json(self):
        """
        返回当前 model 的字典表示
        """
        # copy 会复制一份新数据并返回
        d = self.__dict__.copy()
        return d

    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        models = self.all()
        # 如果没有 id，说明是新添加的元素
        if self.id is None or self.id == -1:
            # 设置 self.id
            # 先看看是否是空 list
            if len(models) == 0:
                # 我们让第一个元素的 id 为 1（当然也可以为 0）
                self.id = 0
            else:
                m = models[-1]
                self.id = m.id + 1
            models.append(self)
        else:
            # index = self.find(self.id)
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            models[index] = self
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)
