from models.mongo import Mongo
from models import Model
from models.error_set import ErrorSet
from models.problem import Problem


# class Chapter(Model):
#     def __init__(self, form):
#         self.id = int(form.get('id', -1))
#         self.subject_id = int(form.get('subject_id', -1))
#         self.name = form.get('name', '')
#         self.article_id = int(form.get('article_id', -1))


class Chapter(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('subject_id', int, -1),
        ('name', str, ''),
        ('article_id', int, -1),
    ]

    # def delete_chapter(self):
    #     query = {
    #         'chapter_id' : self.id,
    #         'subject_id': self.subject_id,
    #     }
    #     ErrorSet.delete_all(query)
    #     Problems.delete_all(query)
    #     self.delete()

    def get_subject_name(self):
        from models.subject import Subject
        return Subject.find(self.subject_id).name

    @classmethod
    def get_subject_id_map(self):
        id_map = {}
        all = Chapter.all()
        for c in all:
            id_map[c.id] = c.subject_id
        return id_map
