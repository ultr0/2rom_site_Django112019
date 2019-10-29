"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from oge2020 import views

# from oge2020.views import TextDetailView


# urlpatterns = [
#    
# ]

urlpatterns = [
    # АДМИНКА
    path('admin/', admin.site.urls),

    # MAIN MENU
    path('', views.index),
    path('index/', views.index, name='index'),
    # THEMES
    url(r'^themes/$', views.ThemeListView.as_view(), name='themes'),
    url(r'^theme/(?P<pk>\d+)$', views.ThemeDetailView.as_view(), name='theme-detail'),
    path('bank/', views.bank, name='bank'),
    path('statistics/', views.statistics, name='statistics'),

    ## ЛИЧНЫЙ КАБИНЕТ
    path('accounts/', include('django.contrib.auth.urls')),
    # path('registration/', views.registration, name='registration'),
    # path(r'^registration/$', views.RegisterFormView.as_view(), name='registration'),
    path('register/', views.MyRegisterFormView.as_view(), name="register"),
    # path('/accounts/profile/', views.theory, name="profile"),
    path('profile/', views.profile, name='profile'),
    path('mode/', views.mode, name='mode'),
    path('mystatistics/', views.mystatistics, name='mystatistics'),

    # path('test/<int:pk>/question/<int:q>/', views.test_view, name='test'),
    # path('test/<int:pk>/finish/', views.finish, name='finish'),

    # path('exercise/<int:pk>/zadanie/<int:q>/', views.test_view, name='test'),
    # path('exercise/<int:pk>/finish/', views.finish, name='finish'),

    # path('exercise/<int:pk>/question/<int:q>/', views.question_view, name='question'),
    # exercise/1/question/1
    url(r'^exercises/$', views.ExerciseListView.as_view(), name='exercises'),
    url(r'^exercise/(?P<pk>\d+)$', views.ExerciseDetailView.as_view(), name='exercise-detail'),
    path('exercise_result/', views.exersice_result, name='exersice_result'),

    url(r'^variants/$', views.VariantListView.as_view(), name='variants'),
    url(r'^variant/(?P<pk>\d+)$', views.VariantDetailView.as_view(), name='variant-detail'),

    # SOLUTIONS
    url(r'^analysis/$', views.AnalysisListView.as_view(), name='analysis'),
    url(r'^analise/(?P<pk>\d+)$', views.AnalysisDetailView.as_view(), name='analise-detail'),

    # path('exercises/', views.exercise_list_view, name='exercises'),
    # path('exercise/<int:pk>/', views.question_view, name='exercise'),
    # url(r'^tests/$', views.TestListView.as_view(), name='tests'),

    # url(r'^zadania/$', views.ZadaniaListView.as_view(), name='zadania'),
    # url(r'^zadanie/(?P<pk>\d+)$', views.ZadaniaDetailView.as_view(), name='zadanie-detail'),

    # url(r'^test/(?P<pk>\d+)$', views.TestDetailView.as_view(), name='test-detail'),

    # url('tests/', views.TestListView.as_view(), name='tests'),

    # path('exersices.html',views.exersices, name='exersices'),
    path('enter.html', views.enter, name='enter'),
    # path('register.html', views.register, name='register'),

    path('allstatistics.html', views.allstatistics, name='allstatistics'),
    # path(r'text/(?P<pk>\d+)/',TextDetailView.as_view(), name='text'),
    # path('<slug:slug>/', TextDetailView.as_view(), name='theme_detail'),

    # path('zadania.html',views.zadania,name='zadania')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
