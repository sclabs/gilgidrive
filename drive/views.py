from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import DeleteView as GenericDeleteView
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from .models import Category, File
from .forms import FileForm, SearchForm
from .search import normalize_query, get_query

# context needed by all views (e.g., because navbar)
def common_context(view_instance):
    context = {}
    # needed for dropdown
    context['categories'] = Category.objects.all()
    context['search_form'] = SearchForm()
    return context

class AllView(ListView):
    def get_queryset(self):
        files = File.objects.all()
        for file in files:
            file.info = file.get_info()
        return files
        
    def get_context_data(self, **kwargs):
        context = super(AllView, self).get_context_data(**kwargs)
        context = dict(context.items() + common_context(self).items())
        context['page_title'] = 'all files'
        context['all_active'] = 'active'
        context['categories_active'] = 'active'
        return context

class RecentView(ListView):
    def get_queryset(self):
        files = File.objects.all()[:20]
        for file in files:
            file.info = file.get_info()
        return files

    def get_context_data(self, **kwargs):
        context = super(RecentView, self).get_context_data(**kwargs)
        context = dict(context.items() + common_context(self).items())
        context['page_title'] = 'recent files'
        context['recent_active'] = 'active'
        return context

class CategoryView(ListView):
    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs['name'])
        files = File.objects.filter(category=category)
        for file in files:
            file.info = file.get_info()
        return files

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context = dict(context.items() + common_context(self).items())
        context['page_title'] = 'category: ' + self.kwargs['name']
        context['categories_active'] = 'active'
        for category in context['categories']:
            if category.name == self.kwargs['name']:
                category.active = 'active'
        return context

class SearchView(ListView):
    template_name = 'drive/file_list.html'

    def get_queryset(self):
        query_string = ''
        files = None
        if ('query' in self.request.GET) and self.request.GET['query'].strip():
            query_string = self.request.GET['query']
            file_query = get_query(query_string, ['title', 'description', 'user__username', 'category__name'],)
            files = File.objects.filter(file_query)
        if files:
            for file in files:
                file.info = file.get_info()
        return files
        
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context = dict(context.items() + common_context(self).items())
        context['page_title'] = 'Search Results'
        context['search'] = True
        return context
        
class AddView(CreateView):
    form_class = FileForm
    template_name = 'drive/file_form.html'
    
    def get_context_data(self, **kwargs):
        context = super(AddView, self).get_context_data(**kwargs)
        context = dict(context.items() + common_context(self).items())
        context['add_active'] = 'active'
        context['add_or_edit'] = 'add'
        context['add_or_save'] = 'add'
        return context
    
    #def post(self, request, *args, **kwargs):
    #    super(AddView, self).post(request, *args, **kwargs)
    #    print 'poast'
    #    form = request.form
    #    context = self.get_context_data(form=form)
    #    return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class EditView(UpdateView):
    form_class = FileForm
    model = File
    template_name = 'drive/file_form.html'
    
    def get(self, request, *args, **kwargs):
        file = get_object_or_404(File, pk=self.kwargs['pk'])
        if file.user != self.request.user:
            raise Http404
        return super(EditView, self).get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)
        context = dict(context.items() + common_context(self).items())
        context['add_or_edit'] = 'edit'
        context['add_or_save'] = 'save'
        return context

class DeleteView(GenericDeleteView):
    model = File
    success_url = reverse_lazy('recent')
    
    def get(self, request, *args, **kwargs):
        file = get_object_or_404(File, pk=self.kwargs['pk'])
        if file.user != self.request.user:
            raise Http404
        return super(DeleteView, self).get(request, *args, **kwargs)

class FileView(DetailView):
    model = File
    
    def get_context_data(self, **kwargs):
        context = super(FileView, self).get_context_data(**kwargs)
        context = dict(context.items() + common_context(self).items())
        self.object.info = self.object.get_info()
        if self.object.user == self.request.user:
            context['owned'] = True
        return context
        
class ChangelogView(TemplateView):
    template_name = 'changelog.html'
    
    def get_context_data(self, **kwargs):
        context = super(ChangelogView, self).get_context_data(**kwargs)
        context = dict(context.items() + common_context(self).items())
        context['changelog_active'] = 'active'
        return context