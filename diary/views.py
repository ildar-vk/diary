from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Entry, Category
from .forms import EntryForm


class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'diary/entry_list.html'
    context_object_name = 'entries'
    paginate_by = 10

    def get_queryset(self):
        queryset = Entry.objects.filter(author=self.request.user)
        query = self.request.GET.get('q')
        category_name = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )

        if category_name:
            try:
                category = Category.objects.get(name=category_name)
                keywords = [
                    kw.strip().lower()
                    for kw in category.keywords.split(',')
                    if kw.strip()
                ]
                if keywords:
                    regex_pattern = '|'.join(keywords)
                    queryset = queryset.filter(
                        Q(title__iregex=regex_pattern) |
                        Q(content__iregex=regex_pattern)
                    )
            except Category.DoesNotExist:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


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
        response = super().form_valid(form)
        self.object.auto_assign_category()
        self.object.save()
        return response


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = 'diary/entry_form.html'
    success_url = reverse_lazy('entry_list')

    def get_queryset(self):
        return Entry.objects.filter(author=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.auto_assign_category()
        self.object.save()
        return response


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    template_name = 'diary/entry_confirm_delete.html'
    success_url = reverse_lazy('entry_list')

    def get_queryset(self):
        return Entry.objects.filter(author=self.request.user)
