from models.mongo import Mongo
from models import Model


# class Article(Model):
#     def __init__(self, form):
#         self.id = int(form.get('id', -1))
#         self.chapter_id = int(form.get('chapter_id', -1))
#         self.title = form.get('title', '')
#         self.content = form.get('content', '')

class Article(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('chapter_id', int, -1),
        ('title', str, ''),
        ('content', str, ''),
    ]

    @classmethod
    def get_subject_and_chapter_name(self):
        obj = {}
        from models.subject import Subject
        from models.chapter import Chapter
        subjects = Subject.all()
        for s in subjects:
            clist = Chapter.find_all(subject_id=s.id)
            temp = []
            for c in clist:
                temp.append(c.__dict__)
            obj[s.id] = temp
        return obj

    def get_chapter(self):
        from models.chapter import Chapter
        return Chapter.find(self.chapter_id)

    def get_chapter_name(self):
        return self.get_chapter().name

    def get_subject_name(self):
        from models.subject import Subject
        chapter = self.get_chapter()
        return Subject.find(chapter.subject_id).name

    @classmethod
    def save_article(cls, form):
        from models.chapter import Chapter
        article = Article.upsert({
            'chapter_id': int(form.get('chapter_id')),
        }, {
            'title': form.get('title'),
            'content': form.get('content'),
        })
        Chapter.upsert({
            'id': article.chapter_id,
        }, {
            'article_id': article.id,
        })

# print(json.dumps(Article.get_subject_and_chapter_name(), ensure_ascii=False))
