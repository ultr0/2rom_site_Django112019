from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views import generic
from .forms import UserForm
from .forms import profileForm
from .forms import MyForm
from .forms import ReplyForm
from django.http import JsonResponse


from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView

#from .models import Zadania
from .models import Theme
from .models import Variant
from .models import Exercise
from .models import Question
#from .models import ExerciseResult
#from .models import Analysis

from oge2020 import forms as helpers, models



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
    return render(request, 'oge2020/mode.html')

def mystatistics(request):
    return render(request, "oge2020/mystatistics.html")

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
    return render(request, "oge2020/statistics.html")

    
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
    #queryset = Exercise.objects.all()
    #queryset = Question.objects.filter(exercise_number=id)
    #queryset = Question.objects.all()    
    
    
    # ваше собственное имя переменной контекста в шаблоне
    #queryset = Book.objects.filter(title__icontains='war')[:5] # Получение 5 книг, содержащих слово 'war' в заголовке
    #template_name = 'books/my_arbitrary_template_name_list.html'
    
    def get_context_data(self, **kwargs):
        # xxx will be available in the template as the related objects
        context = super(ExerciseDetailView, self).get_context_data(**kwargs)
        context['exercise_object'] = Exercise.objects.get(id=self.kwargs.get('pk'))
        context['question_list'] = Question.objects.filter(exercise_number=self.kwargs.get('pk'))   #all()
        context['form'] = ReplyForm
        #AnotherModel.objects.filter(var=self.get_object())
        return context
        
    def post(self, request, *args, **kwargs):
        HttpResponse('This is POST request!')
 
 
    def post(self, request, *args, **kwargs):
        form = ReplyForm(request.POST)
        
        print >>sys.stderr, 'POST Method start!'
        
        if form.is_valid():
            # reply = form.save(commit=False)
            # reply.creator = request.user
            # reply.question = self.get_object()
            # reply.save()
            
            #answer = form.cleaned_data['answer']
            #message = form.cleaned_data['message']
            #sender = form.cleaned_data['sender']
            #cc_myself = form.cleaned_data['cc_myself']
            
            self.object = self.get_object()
            answer = request.POST['answer']
            creator = request.user
            
            #fort = Family(names = n, age = a, vid = v)
            #fort.save()
            
            #if request.method=='POST' and 'btnform2' in request.POST:
            #pk = request.POST.get('address_pk', 0)

            messages.info(request, f'Набрано баллов за тестовую часть!')

            
            context = super(ExerciseDetailView, self).get_context_data(**kwargs)
            ex_id = self.kwargs.get('pk')
            #result = ExerciseResult(ex_number=ex_id, author = creator, checked=555)
            #result.save()
            #context['form'] = ReplyForm
            context['ex_id'] = ex_id
            #context['answ'] = form.cleaned_data['answer']
            #context['student_name'] = creator
            
            #if 'btnform1' in request.POST:
                #context['answer'] = request.POST['answer']
            #return JsonResponse({"devices": devices})
            return render(request, 'test_page.html', {'obj': context})

            #self.render_to_response('exercises/exercise-result.html', context=context)

        else:
            messages.info(request, f'Ветка 2!')
            self.object = self.get_object()
            context = super(ExerciseDetailView, self).get_context_data(**kwargs)
            context['form'] = form
            context['ex_id'] = ex_id
            return render(request, 'test_page.html', {'obj': context})
            #return self.render_to_response('exercises/exercise-result.html', context=context)    
        
        

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
    return render(request, "exercises/exercise_result.html")

    
# def register(request):
    # return render(request, "oge2020/register.html")

# def profile(request):
    # return render(request, 'registration/profile.html', {})

# def theory(request):
    # return render(request, "oge2020/theory.html")