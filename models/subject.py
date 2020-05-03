from models.mongo import Mongo
from models import Model


# class Subject(Model):
#     def __init__(self, form):
#         self.id = int(form.get('id', -1))
#         self.name = form.get('name', '')
#         self.open_sign = bool(form.get('open_sign', True))

class Subject(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('name', str, ''),
        ('open_sign', bool, True),
    ]


    # def delete_by_id(self, id):
    #     from models.error_set import ErrorSet
    #     from models.problems import Problems
    #     from models.chapter import Chapter
    #     ErrorSet.delete_by_id(subject_id=id)
    #     Problems.delete_by_id(subject_id=id)
    #     Chapter.delete_by_id(subject_id=id)
    #     self.delete()
