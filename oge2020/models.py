from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

from datetime import date

class BaseModel(models.Model):
    #created_time = models.DateTimeField(auto_now_add=True)
    #modified_time = models.DateTimeField(auto_now=True)

    created_date    = models.DateTimeField(default=timezone.now)
    published_date  = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    class Meta:
        abstract = True

# THEME
class Theme(BaseModel):
    # Theme description
    number          = models.IntegerField("Номер темы*:", primary_key=True)
    name            = models.TextField("Имя темы*:")
    content         = models.TextField("Содержание темы*:")
    source_name     = models.TextField("Название источника:", blank=True, null=True, default=None)
    source_link     = models.URLField("Ссылка на источник:", blank=True, null=True, default=None)
    # Additional references
    reference1_name = models.TextField("Пример 1:", blank=True, null=True, default=None)
    reference1_link = models.URLField("Ссылка 1:", blank=True, null=True, default=None)
    reference2_name = models.TextField("Пример 2:", blank=True, null=True, default=None)
    reference2_link = models.URLField("Ссылка 2:", blank=True, null=True, default=None)
    reference3_name = models.TextField("Пример 3:", blank=True, null=True, default=None)
    reference3_link = models.URLField("Ссылка 3:", blank=True, null=True, default=None)
    # изображения
    picture1        = models.ImageField(verbose_name='Изображение 1', null=True, blank=True)
    picture2        = models.ImageField(verbose_name='Изображение 2', null=True, blank=True)
    picture3        = models.ImageField(verbose_name='Изображение 3', null=True, blank=True)
    picture4        = models.ImageField(verbose_name='Изображение 4', null=True, blank=True)
    picture5        = models.ImageField(verbose_name='Изображение 5', null=True, blank=True)
    # info
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '{} №{}'.format(self.name, self.number)

#################################################################################################
#################################################################################################
# EXERCISE
class Exercise(BaseModel):
    name = models.TextField("Название задания", blank=True, null=True, default=None)
    number = models.IntegerField("Номер задания", blank=True, null=True, default=None)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '{} №{}'.format(self.name, self.number)

# class ExerciseResult(BaseModel):
    # ex_number       = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='questions', verbose_name='Question')
    # author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    # answ            = models.IntegerField("User Answer", blank=True, null=True, default=None)
    # points          = models.IntegerField("Points",blank=True, null=True, default=None)
    # checked         = models.IntegerField("Points",blank=True, null=True, default=None)


# VARIANT
class Variant(models.Model):
    name = models.TextField("Имя варианта", blank=True, null=True, default=None)
    number=models.IntegerField("Номер варианта", blank=True, null=True, default=None)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    def publish(self):
       self.published_date = timezone.now()
       self.save()

    def __str__(self):
        return '{} №{}'.format(self.name, self.number)


class Question(BaseModel):
    theme_number    = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='test_questions', verbose_name='Тема')
    exercise_number = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='questions', verbose_name='Вопрос')
    variant_number  = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='variants', verbose_name='Вариант')
    question_text   = models.TextField()
    question_answer = models.TextField()
    question_type   = models.IntegerField(default = 1)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    picture1 = models.ImageField(verbose_name='Изображение 1', null=True, blank=True)
    picture2 = models.ImageField(verbose_name='Изображение 2', null=True, blank=True)
    picture3 = models.ImageField(verbose_name='Изображение 3', null=True, blank=True)
    picture4 = models.ImageField(verbose_name='Изображение 4', null=True, blank=True)
    picture5 = models.ImageField(verbose_name='Изображение 5', null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.question_text)

class Journal(BaseModel):
    """
    Сущность (таблица) для журналирования ответов на вопросы от пользователей
    """
    # timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время ответа')
    question  = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    correct = models.BooleanField(verbose_name='Верный ответ', default=False)
    answer = models.TextField(verbose_name='Ответ', null=True, blank=True)
    answer_document = models.FileField(verbose_name='Документ для проверки', null=True, blank=True)
    session_id = models.TextField(verbose_name='Индивидуальный номер для объединения результатов тестирования')
    number_questions_in_variant = models.IntegerField(verbose_name='Количество всех вопросов в варианте на момент сдачи')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return 'Ответ {} на вопрос {}'.format(self.user, self.question)

    def is_correct(self):
        if self.correct == True:
            answer = 'Верно'
        else:
            answer = 'Неверно'
        return answer




#################################################################################################
#################################################################################################

# class User(AbstractUser):
    # bio = models.TextField(max_length=500, blank=True)
    # location = models.CharField(max_length=30, blank=True)
    # birth_date = models.DateField(null=True, blank=True)


# class BaseModel(models.Model):
    # created_time = models.DateTimeField(auto_now_add=True)
    # modified_time = models.DateTimeField(auto_now=True)

    # class Meta:
        # abstract = True

# class Student(AbstractUser, BaseModel):
    # middle_name = models.CharField(max_length=30, null=True, blank=True)

    # def __str__(self):
        # return f'{self.last_name} {self.first_name} {self.middle_name}'

    # class Meta:
        # verbose_name = 'Student'
        # verbose_name_plural = 'Students'






# TASK
# class Zadania(models.Model):
    # number = models.IntegerField("Theme number: ")
    # variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    # exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    # question = models.TextField()
    # type = models.IntegerField(default = 1)
    # answer1 = models.IntegerField(blank=True, null=True)
    # answer2 = models.IntegerField(blank=True, null=True)
    # answer3 = models.IntegerField(blank=True, null=True)
    # answer4 = models.IntegerField(blank=True, null=True)
    # answer5 = models.TextField(max_length=200, blank=True, null=True)
    # answer_self = models.TextField(max_length=200, blank=True, null=True)
    # answer_int = models.IntegerField(blank=True, null=True)
    # right_answer = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint=models.IntegerField( blank=True, null=True)

    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # created_date = models.DateTimeField(default=timezone.now)
    # published_date = models.DateTimeField(blank=True, null=True)

    # def publish(self):
        # self.published_date = timezone.now()
        # self.save()

############################################################################################






# class Text(models.Model):
    # number = models.IntegerField()
    # name = models.TextField()
    # material= models.TextField()
    # links = models.TextField()
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # created_date = models.DateTimeField(default=timezone.now)
    # published_date = models.DateTimeField(blank=True, null=True)

    # def publish(self):
        # self.published_date = timezone.now()
        # self.save()

# class Students_statistics(models.Model):
    # number_of_right_answers=models.IntegerField()
    # number_of_wrong_answers=models.IntegerField()
    # percent_of_variant=models.IntegerField()
    # pupil = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

# class Analysis(models.Model):
    # number = models.IntegerField()
    # question1 = models.TextField()
    # type1 = models.IntegerField(default = 1)
    # question_number1=models.IntegerField()
    # material1=models.TextField()
    # right_answer1 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint1=models.IntegerField( blank=True, null=True)
    # right_answertest1=models.IntegerField( blank=True, null=True)

    # question2 = models.TextField()
    # question_number2=models.IntegerField()
    # type2 = models.IntegerField(default = 1)
    # material2=models.TextField()
    # right_answer2 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint2=models.IntegerField( blank=True, null=True)
    # right_answertest2=models.IntegerField( blank=True, null=True)

    # question3 = models.TextField()
    # question_number3=models.IntegerField()
    # type3 = models.IntegerField(default = 1)
    # material3=models.TextField()
    # right_answer3 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint3=models.IntegerField( blank=True, null=True)
    # right_answertest3=models.IntegerField( blank=True, null=True)

    # question4 = models.TextField()
    # question_number4=models.IntegerField()
    # type4 = models.IntegerField(default = 1)
    # material4=models.TextField()
    # right_answer4 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint4=models.IntegerField( blank=True, null=True)
    # right_answertest4=models.IntegerField( blank=True, null=True)

    # question5 = models.TextField()
    # question_number5=models.IntegerField()
    # type5 = models.IntegerField(default = 1)
    # material5=models.TextField()
    # right_answer5 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint5=models.IntegerField( blank=True, null=True)
    # right_answertest5=models.IntegerField( blank=True, null=True)

    # question6 = models.TextField()
    # question_number6=models.IntegerField()
    # type6 = models.IntegerField(default = 1)
    # material6=models.TextField()
    # right_answer6 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint6=models.IntegerField( blank=True, null=True)
    # right_answertest6=models.IntegerField( blank=True, null=True)

    # question7 = models.TextField()
    # question_number7=models.IntegerField()
    # type7 = models.IntegerField(default = 1)
    # material7=models.TextField()
    # right_answer7 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint7=models.IntegerField( blank=True, null=True)
    # right_answertest7=models.IntegerField( blank=True, null=True)

    # question8 = models.TextField()
    # question_number8=models.IntegerField()
    # type8 = models.IntegerField(default = 1)
    # material8=models.TextField()
    # right_answer8 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint8=models.IntegerField( blank=True, null=True)
    # right_answertest8=models.IntegerField( blank=True, null=True)

    # question9 = models.TextField()
    # question_number9=models.IntegerField()
    # type9 = models.IntegerField(default = 1)
    # material9=models.TextField()
    # right_answer9 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint9=models.IntegerField( blank=True, null=True)
    # right_answertest9=models.IntegerField( blank=True, null=True)

    # question10 = models.TextField()
    # question_number10=models.IntegerField()
    # type10 = models.IntegerField(default = 1)
    # material10=models.TextField()
    # right_answer10 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint10=models.IntegerField( blank=True, null=True)
    # right_answertest10=models.IntegerField( blank=True, null=True)

    # question11 = models.TextField()
    # question_number11=models.IntegerField()
    # type11 = models.IntegerField(default = 1)
    # material11=models.TextField()
    # right_answer11 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint11=models.IntegerField( blank=True, null=True)
    # right_answertest11=models.IntegerField( blank=True, null=True)

    # question12 = models.TextField()
    # question_number12=models.IntegerField()
    # type12 = models.IntegerField(default = 1)
    # material12=models.TextField()
    # right_answer12 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint12=models.IntegerField( blank=True, null=True)
    # right_answertest12=models.IntegerField( blank=True, null=True)

    # question13 = models.TextField()
    # question_number13=models.IntegerField()
    # type13 = models.IntegerField(default = 1)
    # material13=models.TextField()
    # right_answer13 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint13=models.IntegerField( blank=True, null=True)
    # right_answertest13=models.IntegerField( blank=True, null=True)

    # question14 = models.TextField()
    # question_number14=models.IntegerField()
    # type14 = models.IntegerField(default = 1)
    # material14=models.TextField()
    # right_answer14 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint14=models.IntegerField( blank=True, null=True)
    # right_answertest14=models.IntegerField( blank=True, null=True)

    # question15 = models.TextField()
    # question_number15=models.IntegerField()
    # type15 = models.IntegerField(default = 1)
    # material15=models.TextField()
    # right_answer15 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint15=models.IntegerField( blank=True, null=True)
    # right_answertest15=models.IntegerField( blank=True, null=True)

    # question16 = models.TextField()
    # question_number16=models.IntegerField()
    # type16 = models.IntegerField(default = 1)
    # material16=models.TextField()
    # right_answer16 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint16=models.IntegerField( blank=True, null=True)
    # right_answertest16=models.IntegerField( blank=True, null=True)

    # question17 = models.TextField()
    # question_number17=models.IntegerField()
    # type17 = models.IntegerField(default = 1)
    # material17=models.TextField()
    # right_answer17 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint17 = models.IntegerField( blank=True, null=True)
    # right_answertest17 = models.IntegerField( blank=True, null=True)

    # question18 = models.TextField()
    # question_number18 = models.IntegerField()
    # type18 = models.IntegerField(default = 1)
    # material18=models.TextField()
    # right_answer18 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint18=models.IntegerField( blank=True, null=True)
    # right_answertest18=models.IntegerField( blank=True, null=True)

    # question19 = models.TextField()
    # question_number19=models.IntegerField()
    # type19 = models.IntegerField(default = 1)
    # material19=models.TextField()
    # right_answer19 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint19=models.IntegerField( blank=True, null=True)
    # right_answertest19=models.IntegerField( blank=True, null=True)

    # question20 = models.TextField()
    # question_number20=models.IntegerField()
    # type20 = models.IntegerField(default = 1)
    # material20=models.TextField()
    # right_answer20 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint20=models.IntegerField( blank=True, null=True)
    # right_answertest20=models.IntegerField( blank=True, null=True)

    # question21 = models.TextField()
    # question_number21=models.IntegerField()
    # type21 = models.IntegerField(default = 1)
    # material21=models.TextField()
    # right_answer21 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint21 = models.IntegerField( blank=True, null=True)
    # right_answertest21 = models.IntegerField( blank=True, null=True)

    # question22 = models.TextField()
    # question_number22=models.IntegerField()
    # type22 = models.IntegerField(default = 1)
    # material22=models.TextField()
    # right_answer22 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint22=models.IntegerField( blank=True, null=True)
    # right_answertest22=models.IntegerField( blank=True, null=True)

    # question23 = models.TextField()
    # question_number23=models.IntegerField()
    # type23 = models.IntegerField(default = 1)
    # material23=models.TextField()
    # right_answer23 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint23=models.IntegerField( blank=True, null=True)
    # right_answertest23=models.IntegerField( blank=True, null=True)

    # question24 = models.TextField()
    # question_number24=models.IntegerField()
    # type24 = models.IntegerField(default = 1)
    # material24=models.TextField()
    # right_answer24 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint24=models.IntegerField( blank=True, null=True)
    # right_answertest24=models.IntegerField( blank=True, null=True)

    # question25 = models.TextField()
    # question_number25=models.IntegerField()
    # type25 = models.IntegerField(default = 1)
    # material25=models.TextField()
    # right_answer25 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint25=models.IntegerField( blank=True, null=True)
    # right_answertest25=models.IntegerField( blank=True, null=True)

    # question26 = models.TextField()
    # question_number26=models.IntegerField()
    # type26 = models.IntegerField(default = 1)
    # material26=models.TextField()
    # right_answer26 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint26=models.IntegerField( blank=True, null=True)
    # right_answertest26=models.IntegerField( blank=True, null=True)

    # question27 = models.TextField()
    # question_number27=models.IntegerField()
    # type27 = models.IntegerField(default = 1)
    # material27=models.TextField()
    # right_answer27 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint27=models.IntegerField( blank=True, null=True)
    # right_answertest27=models.IntegerField( blank=True, null=True)

    # question28 = models.TextField()
    # question_number28=models.IntegerField()
    # type28 = models.IntegerField(default = 1)
    # material28=models.TextField()
    # right_answer28 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint28=models.IntegerField( blank=True, null=True)
    # right_answertest28=models.IntegerField( blank=True, null=True)

    # question29 = models.TextField()
    # question_number29=models.IntegerField()
    # type29 = models.IntegerField(default = 1)
    # material29=models.TextField()
    # right_answer29 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint29=models.IntegerField( blank=True, null=True)
    # right_answertest29=models.IntegerField( blank=True, null=True)

    # question30 = models.TextField()
    # question_number30=models.IntegerField()
    # type30 = models.IntegerField(default = 1)
    # material30=models.TextField()
    # right_answer30 = models.TextField(max_length=200, blank=True, null=True)
    # right_answerint30=models.IntegerField( blank=True, null=True)
    # right_answertest30=models.IntegerField( blank=True, null=True)

    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # created_date = models.DateTimeField(default=timezone.now)
    # published_date = models.DateTimeField(blank=True, null=True)

    # def publish(self):
        # self.published_date = timezone.now()
        # self.save()

