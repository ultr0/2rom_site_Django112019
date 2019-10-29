import datetime

from django.contrib.auth.models import User
from django.shortcuts import render
from hashlib import  md5
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views import generic

from oge2020.helpers import motivation
from .forms import profileForm, EduMode
from django.http import JsonResponse


from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView

#from .models import Zadania
from .models import Theme, Journal, Mode
from .models import Variant
from .models import Exercise
from .models import Question
#from .models import ExerciseResult
#from .models import Analysis

# from oge2020 import forms as helpers, models



# REGISTRATION
class MyRegisterFormView(FormView):
    # Указажем какую форму мы будем использовать для регистрации наших пользователей, в нашем случае
    # это UserCreationForm - стандартный класс Django унаследованный
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "../accounts/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "registration/register.html"

    def form_valid(self, form):
        form.save()
        # Функция super( тип [ , объект или тип ] ) 
        # Возвратите объект прокси, который делегирует вызовы метода родительскому или родственному классу типа .
        return super(MyRegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(MyRegisterFormView, self).form_invalid(form)

# USER PROFILE
#@login_required
def profile(request):     
    if request.method == 'POST':
        form = profileForm(data=request.POST, instance=request.user)
        update = form.save(commit=False)
        update.user = request.user
        update.save()
    else:
        form = profileForm(instance=request.user)

    return render(request, 'oge2020/profile.html', {'form': form})

def mode(request):
    """
    Функция отвечает за назначения режима, для изучения
    :param request:
    :return:
    """
    if request.method == "GET":
        message = motivation(request)
        # проверяем, есть ли уже настройка интенсивности, если нет, то значение по умолчению - иначе предыдущее значение
        if len(Mode.objects.filter(user=request.user)) == 0:
            form = EduMode()
        else:
            config = Mode.objects.filter(user=request.user).first()
            form = EduMode(initial={'mode': config.mode})
    elif request.method == "POST":
        form = EduMode(request.POST or None)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            if len(Mode.objects.filter(user=request.user)) == 0:
                f.save(form.cleaned_data)
            else:
                # проверяем, есть ли уже настройка интенсивности, изменяем предыдущую
                config = Mode.objects.filter(user=request.user).first()
                config.mode = f.mode
                config.save()

    return render(request, 'oge2020/mode.html', {'form':form, 'motivation':message})

def mystatistics(request):
    journal_theme_array = []
    journal_variant_array = []
    progress_in_themes_array = []
    if request.method == "GET":
        message = motivation(request)
        themes = Theme.objects.all()
        variants = Variant.objects.all()
        journal = Journal.objects.filter(user=request.user).all()

        for variant in variants:
            questions = Question.objects.filter(theme_number=variant)
            correct, incorrect = 0, 0
            question_array = []
            for question in questions:
                if question.variant_number == variant:
                    records_array = []
                    for record in journal:
                        if record.question.variant_number == variant:
                            if record.question == question:
                                if record.correct == True:
                                    correct += 1
                                else:
                                    incorrect += 1
                                records_array.append(record)
                    question_array.append(records_array)
            progress_in_themes_array.append([correct, incorrect])
            variant_dict = dict(name=(variant.name + ' №' + str(variant.number)), questions=question_array, correct=correct,
                              incorrect=incorrect)
            journal_variant_array.append(variant_dict)

        for theme in themes:
            questions = Question.objects.filter(theme_number=theme)
            correct, incorrect = 0, 0
            question_array = []
            for question in questions:
                if question.theme_number == theme:
                    records_array = []
                    for record in  journal:
                        if record.question.theme_number == theme:
                            if record.question == question:
                                if record.correct == True:
                                    correct+=1
                                else:
                                    incorrect+=1
                                records_array.append(record)
                    question_array.append(records_array)
            progress_in_themes_array.append([correct, incorrect])
            theme_dict = dict(name=(theme.name+' №'+str(theme.number)), questions=question_array, correct=correct, incorrect=incorrect)
            journal_theme_array.append(theme_dict)

    return render(request, "oge2020/mystatistics.html", {
        'journal': journal,
        'motivation': message,
        'journal_theme':journal_theme_array,
        'journal_variant':journal_variant_array,})

#################################################################################################
#################################################################################################
 
# def exercise_list_view(request):
    # exercise_list = Exercise.objects.all()
    
    # context = dict(
        # exercise_list=exercise_list
    # )
    # return render(request, 'oge2020/exercise_list.html', context)


# def question_view(request, pk, q=1):
    # student_exercise = Exercise.objects.get(pk=pk)
    # student_question = Question.objects.filter(exercise_number=pk)
    #нормальная отдача страницы
    # context = dict(
        # student_exercise=student_exercise,
        # student_question=student_question
    # ) 
    # return render(request, 'oge2020/test_page.html', context)


#################################################################################################
#################################################################################################
    
def index(request):
    # userform = UserForm()
    # if request.method == "POST":
        # userform = UserForm(request.POST)
        # if userform.is_valid():
            # name = userform.cleaned_data["name"]
            # return HttpResponse("<h2>Hello, {0}</h2>".format(name))
    # return render(request, "index.html", {"form": userform})
    return render(request, "index.html")

def bank(request):
    return render(request, "oge2020/bank.html")

def statistics(request):
    data = []
    if request.method == "GET":
        message = motivation(request)

        users = User.objects.all()
        themes = Theme.objects.all()
        variants = Variant.objects.all()

        for user in users:
            sessions = [0]
            journal = Journal.objects.filter(user=user).all()
            correct = Journal.objects.filter(user=user, correct=True).all()
            incorrect = Journal.objects.filter(user=user, correct=False).all()
            for record in journal:
                session_id = record.session_id
                for session in sessions:
                    if session_id != session:
                        sessions.append(session_id)
            value_session = len(sessions)
            print(value_session)
            user_dict = dict(user=user, correct=len(correct), incorrect=len(incorrect))
            data.append(user_dict)

    return render(request, "oge2020/statistics.html", {
        'data':data,
        'motivation': message,
    })

    
def allstatistics(request):
    return render(request, "oge2020/allstatistics.html")

 
# THEMES 
class ThemeListView(generic.ListView):
    model = Theme
    context_object_name = 'my_theme_list'   # ваше собственное имя переменной контекста в шаблоне
    template_name = 'themes/themes_list.html'
    
class ThemeDetailView(generic.DetailView):
    model = Theme
    template_name = 'themes/theme-detail.html'

# TASK
# class ZadaniaListView(generic.ListView):
    # model = Zadania
    # context_object_name = 'my_zadania_list'   # ваше собственное имя переменной контекста в шаблоне
    # template_name = 'zadania/zadania_list.html' 
    
# class ZadaniaDetailView(generic.DetailView):
    # model = Zadania
    # template_name = 'zadania/zadanie-detail.html'    





    
class ExerciseListView(generic.ListView):
    model = Exercise
    context_object_name = 'my_exercises_list'   # ваше собственное имя переменной контекста в шаблоне
    template_name = 'exercises/exercises_list.html'
    
class ExerciseDetailView(generic.DetailView):
    model = Exercise
    template_name = 'exercises/exercise-detail.html'

    
    def get_context_data(self, **kwargs):
        #
        context = super(ExerciseDetailView, self).get_context_data(**kwargs)
        context['exercise_object'] = Exercise.objects.get(id=self.kwargs.get('pk'))
        context['question_list'] = Question.objects.filter(exercise_number=self.kwargs.get('pk'))   #all()
        return context
        
    def post(self, request, *args, **kwargs):
        return None
        
        

# VARIANT    
class VariantListView(generic.ListView):
    model = Variant
    context_object_name = 'my_variants_list'   # ваше собственное имя переменной контекста в шаблоне
    template_name = 'variants/variants_list.html'
    
class VariantDetailView(generic.DetailView):
    model = Variant
    template_name = 'variants/variant-detail.html'
    
    def get_context_data(self, **kwargs):
        # xxx will be available in the template as the related objects
        context = super(VariantDetailView, self).get_context_data(**kwargs)
        context['variant_object'] = Variant.objects.get(id=self.kwargs.get('pk'))
        context['question_list'] = Question.objects.filter(variant_number=self.kwargs.get('pk'))   #all()
        #AnotherModel.objects.filter(var=self.get_object())
        return context

class AnalysisListView(generic.ListView):
    model = Exercise
    context_object_name = 'my_analysis_list'   # ваше собственное имя переменной контекста в шаблоне
    template_name = 'analysis/analysis_list.html'
    
class AnalysisDetailView(generic.DetailView):
    model = Exercise
    template_name = 'analysis/analise-detail.html'
    
    def get_context_data(self, **kwargs):
        # xxx will be available in the template as the related objects
        context = super(AnalysisDetailView, self).get_context_data(**kwargs)
        context['question_list'] = Question.objects.filter(exercise_number=self.kwargs.get('pk'))   #all()
        #AnotherModel.objects.filter(var=self.get_object())
        return context
    
    
    
#class TestListView(generic.ListView):
    #model = Test
    #context_object_name = 'my_test_list'   # ваше собственное имя переменной контекста в шаблоне
    #template_name = 'tests/tests_list.html'
    
#class TestDetailView(generic.DetailView):
    #model = Test
    #template_name = 'tests/test-detail.html'

    
# def book_detail_view(request,pk):
    # try:
        # book_id=Book.objects.get(pk=pk)
    # except Book.DoesNotExist:
        # raise Http404("Book does not exist")

    # #book_id=get_object_or_404(Book, pk=pk)
    
    # return render(
        # request,
        # 'catalog/book_detail.html',
        # context={'book':book_id,}
    # )


    
    
# def zadania(request):
    # zadania = Zadania.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # return render(request, "oge2020/zadania/", {'zadania': zadania})       
    
def exersices(request):
    return render(request, "oge2020/exersices.html")

def exersice(request):
    #testAnswerform = TestAnswerForm()
    #tests = get_object_or_404(Zadania, pk=exersice_id)
    #zadania = Zadania.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    #zadania = Zadania.objects.all()
    zadania = get_object_or_404(Zadania, pk=id)
    return render(request, "exercises/exercise-detail.html", {"zadania": zadania})
    #return render(request, "exercises/exercise-detail.html", {"form": testAnswerform})
    

    
def enter(request):
    return render(request, "oge2020/enter.html")

def exersice_result(request):
    """
    Функция обработки POST запроса в ручную без использования DjangoForm
    :param request:
    :return:
    """
    # создаём уникальный идетификатор, для последующего показа пользователю результата
    session_id = md5(str(datetime.datetime.now()).encode('utf-8')).hexdigest()
    error = None
    if request.POST:
       for data in request.POST:
           if data != 'csrfmiddlewaretoken': # исключаем ключ проверки формы
               doc = None
               correct = False
               answer = request.POST[data]  # выбираем ответ по ключу
               id_question = data.split('-')[1] # дробим имя для вычленения ID вопроса, который был задан в шаблоне
               question = Question.objects.filter(id=id_question).first()
               if answer == question.question_answer:
                    correct =True
               number_questions_in_variant = len(Question.objects.filter(variant_number=question.variant_number))
               if request.FILES:
                   for file in request.FILES:
                       if id_question == file.split('-')[1]:
                           doc = request.FILES[file]
               Journal.objects.create(question=question, correct=correct, answer=answer, answer_document=doc,
                                      session_id=session_id, number_questions_in_variant=number_questions_in_variant,
                                      user=request.user )

    else:
        error = "Решите задания, чтобы потом узнать результат."

    results = Journal.objects.filter(session_id=session_id).all()
    correct = len(Journal.objects.filter(session_id=session_id, correct=True))

    return render(request, "exercises/exercise_result.html", {
        'error': error,
        'results': results,
        'correct': correct,
                                                              })

    
# def register(request):
    # return render(request, "oge2020/register.html")

# def profile(request):
    # return render(request, 'registration/profile.html', {})

# def theory(request):
    # return render(request, "oge2020/theory.html")