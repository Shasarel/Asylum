class PageModel:

    def __init__(self, page_name, user):
        self.user = user
        self.page_name = page_name
        self.breadcrumb = [
            {
                'name': 'Strona główna',
                'href': '/home'
            }
        ]
        self.tabs = []

    def add_breadcrumb_page(self, name, href):
        self.breadcrumb.append(
            {
                'name': name,
                'href': href
            }
        )
        return self

    def add_tab(self, name):
        self.tabs.append(name)
        return self

    def to_dict(self):
        self_dict = vars(self)
        self_dict['breadcrumb'] = self.breadcrumb
        return self_dict
