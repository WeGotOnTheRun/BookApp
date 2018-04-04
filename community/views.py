from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def get_all_questions():
    questions = Question.objects.all()
    return questions


def get_all_answers():
    answers = Answer.objects.all()
    return answers


def question_form(request):
    question_form = WriteQuestion()
    return request, question_form


def answer_form():
    AnswerForm = WriteAnswer()
    return AnswerForm


def save_question(request, userid):
    question = models.Question()
    question.user = models.User.objects.get(pk=userid)
    QuestionForm = WriteQuestion(request.POST, request.FILES, instance=question)
    if QuestionForm.is_valid():
        QuestionForm.save()
        FeedBack = "Question is posted"
        AlertType = 'alert-success'
        request, QuestionForm = question_form(request)
        return request, FeedBack, QuestionForm, AlertType
    else:
        FeedBack = QuestionForm['Content'].errors
        AlertType = 'alert-danger'
        request, QuestionForm = question_form(request)
        return request, FeedBack, QuestionForm, AlertType


def save_answer(request, userid, questionid):
    answer = models.Answer()
    answer.user = models.User.objects.get(pk=userid)
    answer.question_id = models.Question.objects.get(pk=questionid)
    AnswerForm = WriteAnswer(request.POST, request.FILES, instance=answer)
    if AnswerForm.is_valid():
        question = models.Question.objects.get(pk=questionid)
        increment = question.number_of_answers
        increment += 1
        question.number_of_answers = increment
        question.save()
        AnswerForm.save()
        FeedBack = "Your Answer Is Posted"
        AlertType = 'alert-success'
        AnswerForm = answer_form()
        return request, FeedBack, AnswerForm, AlertType
    else:
        FeedBack = AnswerForm['content'].errors
        AlertType = 'alert-danger'
        AnswerForm = answer_form()
        return request, FeedBack, AnswerForm, AlertType

@login_required
def home(request):
    questions = get_all_questions()
    answers = get_all_answers()
    request, Question_form = question_form(request)
    Answer_form = answer_form()
    return render(request, 'community_view/index.html', {'QuestionForm': Question_form, 'AnswerForm': Answer_form, 'questions': questions, 'answers': answers})


@login_required
def savequestion(request):
    if request.user.is_active:
        questions = get_all_questions()
        user_id =request.user.id
        AnswerForm = answer_form()
        answers = get_all_answers()
        request, FeedBack, QuestionForm, AlertType = save_question(request, user_id)
        return redirect('community:home')
    else:
        return render(request, 'general_view/404.html')

def GetUserByID(self, userID):
    user = User.objects.get(pk=userID)
    return user


@login_required
def saveanswer(request, questionid):
    if request.user.is_active:
        user_id = request.user.id
        request, FeedBack, AnswerForm, AlertType = save_answer(request, user_id, questionid)
        request, QuestionForm = question_form(request)
        answers = get_all_answers()
        questions = get_all_questions()
        return redirect('community:home')
    else:
        return render(request, 'general_view/404.html')
