from models.mongo import Mongo
from models import Model


# class Judgement(Model):
#     def __init__(self, form):
#         self.id = int(form.get('id', -1))
#         self.subject_id = int(form.get('subject_id', -1))
#         self.chapter_id = int(form.get('chapter_id', -1))
#         self.type = form.get('type', self.__class__.__name__)
#         self.topic = form.get('topic', '')
#         self.answer = bool(form.get('answer', True))
#         self.analysis = form.get('analysis', '')

class Judgement(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('subject_id', int, -1),
        ('chapter_id', int, -1),
        ('topic', str, ''),
        ('answer', bool, False),
        ('analysis', str, ''),
    ]
