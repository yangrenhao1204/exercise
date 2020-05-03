from models.mongo import Mongo
from models import Model


# class ErrorSet(Model):
#     def __init__(self, form):
#         self.id = int(form.get('id', -1))
#         self.openid = form.get('openid', -1)
#         self.subject_id = int(form.get('subject_id', -1))
#         self.type = form.get('type', '')
#         self.problem_list = form.get('problem_list', [])

class ErrorSet(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('openid', str, ''),
        ('subject_id', int, -1),
        ('problem_type', str, ''),
        ('problem_list', list, []),
    ]

    @classmethod
    def get_error_set(cls, form):
        error_set = []
        all_error_set = ErrorSet.find_all(
            openid=form.get('openid'),
            subject_id=form.get('subject_id'),
        )
        for item in all_error_set:
            error_set.append(item.__dict__)
        return error_set

    @classmethod
    def save_error_type_set(cls, form, problem_type):
        ErrorSet.upsert({
            'openid': form.get('openid'),
            'subject_id': form.get('subject_id'),
            'problem_type': problem_type,
        }, {
            'problem_list': form.get("incorrectIdSet")[problem_type],
        })

    @classmethod
    def save_error_set(cls, form):
        incorrect_id_set = form.get("incorrectIdSet")
        if incorrect_id_set.get('SingleChoice', None) != None:
            ErrorSet.save_error_type_set(form, 'SingleChoice')
        if incorrect_id_set.get('MultipleChoice', None) != None:
            ErrorSet.save_error_type_set(form, 'MultipleChoice')
        if incorrect_id_set.get('Judgement', None) != None:
            ErrorSet.save_error_type_set(form, 'Judgement')
