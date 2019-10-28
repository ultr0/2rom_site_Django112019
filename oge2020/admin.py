# Register your models here.
from django.contrib import admin

from .models import Theme
admin.site.register(Theme)

from .models import Exercise
admin.site.register(Exercise)

from .models import Question
admin.site.register(Question)

from .models import Variant
admin.site.register(Variant)

#from .models import ExerciseResult
#admin.site.register(ExerciseResult)





# from .models import Zadania
# admin.site.register(Zadania)



# from .models import Analysis
# admin.site.register(Analysis)