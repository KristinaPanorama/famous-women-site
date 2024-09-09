menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'addpost'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 5
    extra_context = {}
    title_page = None

    def __init__(self):

        if self.title_page:
            self.extra_context['title'] = self.title_page

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        context['cat_selected'] = None
        context.update(kwargs)
        return context

