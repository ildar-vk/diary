from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Entry
from .forms import EntryForm

class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'diary/entry_list.html'
    context_object_name = 'entries'
    paginate_by = 10

    def get_queryset(self):
        queryset = Entry.objects.filter(author=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query) | queryset.filter(content__icontains=query)
        return queryset

class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = 'diary/entry_detail.html'
    context_object_name = 'entry'

    def get_queryset(self):
        return Entry.objects.filter(author=self.request.user)

class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'diary/entry_form.html'
    success_url = reverse_lazy('entry_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = 'diary/entry_form.html'
    success_url = reverse_lazy('entry_list')

    def get_queryset(self):
        return Entry.objects.filter(author=self.request.user)

class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = 'diary/entry_confirm_delete.html'
    success_url = reverse_lazy('entry_list')

    def get_queryset(self):
        return Entry.objects.filter(author=self.request.user)
