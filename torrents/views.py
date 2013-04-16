from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect

from .models import Category, Torrent
from .forms import AddForm, EditForm

class AllView(ListView):
    def get_queryset(self):
        return Torrent.objects.all()
        
    def get_context_data(self, **kwargs):
        context = super(AllView, self).get_context_data(**kwargs)
        context['page_title'] = 'all torrents'
        context['all_active'] = 'active'
        context['categories_active'] = 'active'
        context['categories'] = Category.objects.all()
        return context

class RecentView(ListView):
    def get_queryset(self):
        return Torrent.objects.order_by('added')[:20]

    def get_context_data(self, **kwargs):
        context = super(RecentView, self).get_context_data(**kwargs)
        context['page_title'] = 'recent torrents'
        context['recent_active'] = 'active'
        context['categories'] = Category.objects.all()
        return context

class CategoryView(ListView):
    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs['name'])
        return Torrent.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['page_title'] = 'category: ' + self.kwargs['name']
        context['categories_active'] = 'active'
        context['categories'] = Category.objects.all()
        for category in context['categories']:
            if category.name == self.kwargs['name']:
                category.active = 'active'
        return context

class AddView(CreateView):
    form_class = AddForm
    template_name = 'torrents/torrent_form.html'
    
    def get_context_data(self, **kwargs):
        context = super(AddView, self).get_context_data(**kwargs)
        context['add_active'] = 'active'
        context['categories'] = Category.objects.all()
        return context
        
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class EditView(UpdateView):
    form_class = EditForm
    model = Torrent
    template_name = 'torrents/torrent_update.html'
    
    def get(self, request, *args, **kwargs):
        torrent = get_object_or_404(Torrent, pk=self.kwargs['pk'])
        if torrent.user != self.request.user:
            raise Http404
        return super(EditView, self).get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class TorrentView(DetailView):
    model = Torrent
    
    def get_context_data(self, **kwargs):
        context = super(TorrentView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        torrent = get_object_or_404(Torrent, pk=self.kwargs['pk'])
        if torrent.user == self.request.user:
            context['owned'] = True
        return context

class ChangelogView(TemplateView):
    template_name = 'changelog.html'
    
    def get_context_data(self, **kwargs):
        context = super(ChangelogView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['categories'] = Category.objects.all()
        context['changelog_active'] = 'active'
        return context