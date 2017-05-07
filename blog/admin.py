from django.contrib import admin
from .models import Post_blog, Author


class Post_blog_Admin(admin.ModelAdmin):
    list_display = ('title', 'time')
    search_fields = ('title', 'time')
    list_filter = ('time',)
    date_hierarchy = 'time'
    # fields = ['title', 'image']  # Add new Post
    # raw_id_fields = ('title',)  # (<input type="text">) instead of a <select>

admin.site.register(Post_blog, Post_blog_Admin)
admin.site.register(Author)


# class ChoiceInline(admin.TabularInline):  # or admin.StackedInline
#     model = Choice
#     extra = 2
#
#
# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('Text infoooooooo', {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date']}),
#     ]
#
#     inlines = [ChoiceInline]
#     list_display = ('question_text', 'pub_date', 'was_published_recently')
#     list_filter = ['pub_date', 'question_text']
#     search_fields = ['question_text', 'pub_date']
#
#     list_per_page = 2
#     date_hierarchy = 'pub_date'
#
#
# admin.site.register(Question, QuestionAdmin)
