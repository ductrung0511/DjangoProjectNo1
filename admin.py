from django.contrib import admin
from .models import Blog, ContactRequest, ModelCourse, ModelSession, Question, Category, Section

admin.site.register(Blog)
admin.site.register(ContactRequest)
admin.site.register(ModelSession)
admin.site.register(ModelCourse)
admin.site.register(Question)
admin.site.register(Category)
admin.site.register(Section)


