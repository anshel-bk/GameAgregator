from django.contrib import admin

from game_info_part.models import AuthorArticle, Article


@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    list_display = ('author', 'name_game', 'title', 'preview_picture', 'rating',)
    list_display_links = ('title',)
    search_fields = ('title', 'loot')
    prepopulated_fields = {"slug": ("title",)}


@admin.register(AuthorArticle)
class AdminAuthorArticle(admin.ModelAdmin):
    list_display = ('author',)
    search_fields = ('author',)
