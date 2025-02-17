from django.contrib import admin
from .models import Course, Instructor, Lesson

# Register your models here.

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5

#Makes it so these only show up when making a course in admin
class CourseAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'name', 'description']
    inlines = [LessonInline]

class InstructorAdmin(admin.ModelAdmin):
    fields = ['user', 'full_time']

admin.site.register(Course, CourseAdmin)
admin.site.register(Instructor, InstructorAdmin)



