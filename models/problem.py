from models.single_choice import SingleChoice
from models.multiple_choice import MultipleChoice
from models.judgement import Judgement
from models.error_set import ErrorSet

from libs.utils import getDistListFromObjectList


class Problem():
    @staticmethod
    def upsert(form):
        type = form.get('type')
        options = {}
        options['A'] = form.get('A', '')
        options['B'] = form.get('B', '')
        options['C'] = form.get('C', '')
        options['D'] = form.get('D', '')
        query_form = {
            'id': int(form.get('id', -1))
        }
        if type == 'SingleChoice':
            update_form = dict(
                subject_id=int(form.get('subject_id')),
                chapter_id=int(form.get('chapter_id')),
                type=form.get('type'),
                topic=form.get('topic'),
                options=options,
                answer=form.get('answer'),
                analysis=form.get('analysis', ''),
            )
            problem = SingleChoice.upsert(query_form, update_form)
        elif type == 'MultipleChoice':
            update_form = dict(
                subject_id=int(form.get('subject_id')),
                chapter_id=int(form.get('chapter_id')),
                type=form.get('type'),
                topic=form.get('topic'),
                options=options,
                answer=form.get('answer'),
                analysis=form.get('analysis', ''),
            )
            problem = MultipleChoice.upsert(query_form, update_form)
        elif type == 'Judgement':
            if form.get('answer') == 'true':
                answer = True
            else:
                answer = False
            update_form = dict(
                subject_id=int(form.get('subject_id')),
                chapter_id=int(form.get('chapter_id')),
                type=form.get('type'),
                topic=form.get('topic'),
                answer=answer,
                analysis=form.get('analysis', ''),
            )
            problem = Judgement.upsert(query_form, update_form)
        return problem

    @staticmethod
    def all():
        problems = []
        single_choice = SingleChoice.all()
        multiple_choice = MultipleChoice.all()
        judgement = Judgement.all()
        problems.extend(getDistListFromObjectList(single_choice))
        problems.extend(getDistListFromObjectList(multiple_choice))
        problems.extend(getDistListFromObjectList(judgement))
        return problems

    @staticmethod
    def find(type, problem_id):
        if type == 'SingleChoice':
            problem = SingleChoice.find(problem_id)
        elif type == 'MultipleChoice':
            problem = MultipleChoice.find(problem_id)
        elif type == 'Judgement':
            problem = Judgement.find(problem_id)
        return problem

    @staticmethod
    def find_all(**kwargs):
        problems = {}
        single_choice = SingleChoice.find_all(**kwargs)
        multiple_choice = MultipleChoice.find_all(**kwargs)
        judgement = Judgement.find_all(**kwargs)
        problems["SingleChoice"] = getDistListFromObjectList(single_choice)
        problems["MultipleChoice"] = getDistListFromObjectList(multiple_choice)
        problems["Judgement"] = getDistListFromObjectList(judgement)
        return problems

    @staticmethod
    def get_problem_type_list():
        type_list = []
        type_list.append('SingleChoice')
        type_list.append('MultipleChoice')
        type_list.append('Judgement')
        return type_list

    @staticmethod
    def get_subject_name(subject_id):
        from models.subject import Subject
        return Subject.find(subject_id).name

    @staticmethod
    def get_chapter_name(chapter_id):
        from models.chapter import Chapter
        return Chapter.find(chapter_id).name

    @classmethod
    def add_problem(cls, subject_id, chapter_id, item):
        form = dict(
            subject_id=subject_id,
            chapter_id=chapter_id,
            type=item[3],
            topic=item[4],
            A=item[5],
            B=item[6],
            C=item[7],
            D=item[8],
            answer=item[9],
            analysis=item[10],
        )
        cls.upsert(form)

    @classmethod
    def add_problem_from_xls(cls, lists):
        from models.subject import Subject
        from models.chapter import Chapter
        subject = Subject.new({
            "name": lists[0][0],
        })
        chapter_id_flag = -1
        chapter_id = -1
        for item in lists:
            if int(item[1]) != chapter_id_flag:
                chapter = Chapter.new({
                    'subject_id': subject.id,
                    'name': item[2]
                })
                chapter_id = chapter.id
                chapter_id_flag = int(item[1])
            cls.add_problem(subject.id, chapter_id, item)

    @staticmethod
    def delete(type, id):
        if type == 'SingleChoice':
            obj = SingleChoice.find(id).delete()
        elif type == 'MultipleChoice':
            obj = MultipleChoice.find(id).delete()
        elif type == 'Judgement':
            obj = Judgement.find(id).delete()
        return obj
