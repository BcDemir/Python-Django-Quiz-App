import random

from django.db.models import Avg, Max, Min
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import *
from django.http import HttpResponse


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        questions = QuesModel.objects.all()
        rand_f_ques = random.sample(list(questions), 5)
        if request.method == 'POST':
            print(request.POST)
            score = 0
            wrong = 0
            correct = 0
            total = 0
            for q in rand_f_ques:
                total += 1
                print(request.POST.get(q.question))
                print(q.ans)
                print()
                if q.ans == request.POST.get(q.question):
                    score += 10
                    correct += 1
                else:
                    wrong += 1
            percent = score / (total * 10) * 100
            print(f'{percent} score: {score}')
            # if percent < 50:
            #     return HttpResponse(f'{percent} Your Score is too low! Please retake the test by clicking '
            #                         f'<a href="">here</a>')

            context = {
                'score': score,
                'time': request.POST.get('timer'),
                'correct': correct,
                'wrong': wrong,
                'percent': percent,
                'total': total
            }
            return render(request, 'Quiz/result.html', context)
        else:
            context = {
                'rand_f_ques': rand_f_ques
            }
            return render(request, 'Quiz/home.html', context)
    else:
        return redirect('login')


def addQuestion(request):
    if request.user.is_staff:
        form = addQuestionform()
        if (request.method == 'POST'):
            form = addQuestionform(request.POST)
            if (form.is_valid()):
                form.save()
                return redirect('/')
        context = {'form': form}
        return render(request, 'Quiz/addQuestion.html', context)
    else:
        return redirect('home')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = createuserform()
        if request.method == 'POST':
            form = createuserform(request.POST)
            if form.is_valid():
                user = form.save()
                return redirect('login')
        context = {
            'form': form,
        }
        return render(request, 'Quiz/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        context = {}
        return render(request, 'Quiz/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('/')


def quiz_create(request, template_name='Quiz/Home.html'):
    form = Quizform(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, template_name, {'form': form})


def history(request):
    allList = QuizModel.objects.filter(user_id=request.user.id)
    average = QuizModel.objects.filter(user_id=request.user.id).aggregate(Avg('percent'))
    highest = QuizModel.objects.filter(user_id=request.user.id).aggregate(Max('percent'))
    lowest = QuizModel.objects.filter(user_id=request.user.id).aggregate(Min('percent'))
    form = Quizform()

    context = {
        "allList": allList,
        'form': form,
        'average': average,
        'highest': highest,
        'lowest': lowest
    }
    return render(request, 'Quiz/history.html', context)
