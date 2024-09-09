from django.contrib import admin
from django.core.checks import messages
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext

from women.models import Women, Category


class MarriedFiler(admin.SimpleListFilter):
    title = 'Статус женщин'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [('married', 'Замужем'),
            ('single', 'Не замужем'),]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        if self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'photo', 'post_photo', 'content', 'cat', 'husband', 'tags']
    readonly_fields = ['post_photo']
    prepopulated_fields = {'slug': ['title'], }
    filter_horizontal = ('tags',)
    list_display = ('title', 'time_create', 'cat', 'post_photo', 'is_published')
    list_display_links = ('title',)
    ordering = ['-time_create', 'title']
    list_editable = ['is_published']
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = [MarriedFiler, 'is_published', 'cat']
    save_on_top = True

    @admin.display(description='Изображение')
    def post_photo(self, women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return 'Без фото'


    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, ngettext("%d запись опубликовано", "%d записей опубликовано", count) % count)

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, ngettext("%d запись снята с публикации",
                                            "%d записи(ей) сняты с публикации", count) % count,
                          messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')