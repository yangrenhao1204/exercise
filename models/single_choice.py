from models.mongo import Mongo
from models import Model


# class SingleChoice(Model):
#     def __init__(self, form):
#         self.id = int(form.get('id', -1))
#         self.subject_id = int(form.get('subject_id', -1))
#         self.chapter_id = int(form.get('chapter_id', -1))
#         self.type = form.get('type', self.__class__.__name__)
#         self.topic = form.get('topic', '')
#         self.options = form.get('options', {})
#         self.answer = form.get('answer', '')
#         self.analysis = form.get('analysis', '')

class SingleChoice(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('subject_id', int, -1),
        ('chapter_id', int, -1),
        ('topic', str, ''),
        ('options', dict, {}),
        ('answer', str, ''),
        ('analysis', str, ''),
    ]
