from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Question(models.Model):

    question_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=350)
    number_of_answers = models.IntegerField(default=0)
    posted_time = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        db_table = 'Question'

    def __str__(self):
        return self.content


@python_2_unicode_compatible
class Answer(models.Model):

    answer_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=350)
    posted_time = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        db_table = 'Answer'

    def __str__(self):
        return self.content