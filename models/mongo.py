import time
from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017")
mongodb_name = 'exercise'
db = mongo[mongodb_name]


def timestamp():
    return int(time.time())


def next_id(name):
    query = {
        'name': name,
    }
    update = {
        '$inc': {
            'seq': 1
        }
    }
    kwargs = {
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }
    # 存储数据的 id
    doc = db['data_id']
    # find_and_modify 是一个原子操作函数
    new_id = doc.find_and_modify(**kwargs).get('seq')
    return new_id


class Mongo(object):
    __fields__ = [
        '_id',
        # (字段名, 类型, 值)
        ('id', int, -1),
        ('type', str, ''),
        ('deleted', bool, False),
        ('created_time', int, 0),
        ('updated_time', int, 0),
    ]

    def save(self):
        name = self.__class__.__name__
        db[name].save(self.__dict__)

    @classmethod
    def new(cls, form=None, **kwargs):
        name = cls.__name__
        m = cls()
        # 把定义的数据写入空对象, 未定义的数据输出错误
        fields = cls.__fields__.copy()
        # 去掉 _id 这个特殊的字段
        fields.remove('_id')
        if form is None:
            form = {}
        for f in fields:
            k, t, v = f
            if k in form:
                setattr(m, k, t(form[k]))
            else:
                # 设置默认值
                setattr(m, k, v)
        # 处理额外的参数 kwargs
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError
        # 写入数据id
        m.id = next_id(name)
        ts = timestamp()
        m.created_time = ts
        m.updated_time = ts
        m.type = name
        m.save()
        return m

    @classmethod
    def _new_with_bson(cls, bson):
        """
        这是给内部 all 这种函数使用的函数
        从 mongo 数据中恢复一个 model
        """
        m = cls()
        fields = cls.__fields__.copy()
        # 去掉 _id 这个特殊的字段
        fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in bson:
                setattr(m, k, t(bson[k]))
            else:
                # 设置默认值
                setattr(m, k, v)
        setattr(m, '_id', bson['_id'])
        m.type = cls.__name__
        return m

    @classmethod
    def _find(cls, **kwargs):
        name = cls.__name__
        # 过滤掉被删除的元素
        kwargs['deleted'] = False
        flag_sort = '__sort'
        sort = kwargs.pop(flag_sort, None)
        ds = db[name].find(kwargs)
        if sort is not None:
            ds = ds.sort(sort)
        result = [cls._new_with_bson(d) for d in ds]
        return result

    @classmethod
    def all(cls):
        return cls._find()

    @classmethod
    def find_all(cls, **kwargs):
        return cls._find(**kwargs)

    @classmethod
    def find_one(cls, **kwargs):
        # 过滤掉被删除的元素
        # kwargs['deleted'] = False
        l = cls._find(**kwargs)
        # print('find one debug', kwargs, l)
        if len(l) > 0:
            return l[0]
        else:
            return None

    @classmethod
    def find_by(cls, **kwargs):
        return cls.find_one(**kwargs)

    @classmethod
    def find(cls, id):
        return cls.find_one(id=id)

    @classmethod
    def has(cls, **kwargs):
        return cls.find_one(**kwargs) is not None

    @classmethod
    def upsert(cls, query_form, update_form, hard=False):
        # print("upsert", cls.__name__, query_form, update_form)
        ms = cls.find_one(**query_form)
        if ms is None:
            query_form.update(**update_form)
            ms = cls.new(query_form)
        else:
            ms.update(update_form, hard=hard)
        return ms

    def update(self, form, hard=False):
        for k, v in form.items():
            if hard or hasattr(self, k):
                setattr(self, k, v)
        # self.updated_time = timestamp()
        self.save()

    def delete(self):
        name = self.__class__.__name__
        query = {
            'id': self.id,
        }
        values = {
            '$set': {
                'deleted': True
            }
        }
        db[name].update_one(query, values)

    def delete_all(self, **kwargs):
        name = self.__class__.__name__
        kwargs['id'] = {'$gt': -1}
        values = {
            'deleted': True
        }
        db[name].update_many(kwargs, values)

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    @classmethod
    def _clean_field(cls, source, target):
        """
        清洗数据用的函数
        例如 User._clean_field('is_hidden', 'deleted')
        把 is_hidden 字段全部复制为 deleted 字段
        """
        ms = cls._find()
        for m in ms:
            v = getattr(m, source)
            setattr(m, target, v)
            m.save()

    def blacklist(self):
        b = [
            '_id',
        ]
        return b

    def json(self):
        _dict = self.__dict__
        d = {k: v for k, v in _dict.items() if k not in self.blacklist()}
        return d
