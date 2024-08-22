from django.shortcuts import render
from django.views.generic.base import View

#base.html
class BaseView(View):
    def get(self, request):
        return render(request, 'base.html')
    
#index.html
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
from django.views.generic.base import TemplateView
from django.apps import apps

class HomeView( TemplateView ):
    template_name = 'index.html'

    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dictVerbose={}

        # for app in apps.get_app_configs():
        #     if 'site-packages' not in app.path:
        #         dictVerbose[ app.label ] = app.verbose_name

        # context['verbose_dict'] = dictVerbose

        context[ 'app_list'] = ['account', 'board', 'recommend', 'search']

        return context
