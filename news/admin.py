from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory


class PostCategoryInLine(admin.TabularInline):
    model = PostCategory
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'author', 'created_at',)
    list_filter = ('created_at', 'rating', 'categories')
    search_fields = ('title', 'categories')
    ordering = ('-created_at',)
    inlines = [PostCategoryInLine]
    actions = ['reset_rating']

    def reset_rating(self, request, queryset):
        queryset.update(rating=0)
        self.message_user(request, 'Рейтинг выбранных постов обнулен')

    reset_rating.short_descriptions = 'Обнулить рейтинг у выбранных постов'


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)



    