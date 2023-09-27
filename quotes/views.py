from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from .models import Quote, Tag, Author
from .forms import AuthorForm, TagForm, QuoteForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class Main(View):

    def get(self, request):
        quotes = Quote.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(quotes, 10)

        try:
            quotes = paginator.page(page)
        except PageNotAnInteger:
            quotes = paginator.page(1)
        except EmptyPage:
            quotes = paginator.page(paginator.num_pages)

        return render(request, 'quotes/index.html', context={'quotes': quotes})


class AddAuthor(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        form = AuthorForm()
        return render(request, 'quotes/add_author.html', context={'form': form})

    def post(self, request):
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:main')
        return render(request, 'quotes/add_author.html', {'form': form})


class AddTag(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        form = TagForm()
        return render(request, 'quotes/add_tag.html', context={'form': form})

    def post(self, request):
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:main')
        return render(request, 'quotes/add_tag.html', {'form': form})


class AddQuote(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        form = QuoteForm()
        tags = Tag.objects.all()
        return render(request, 'quotes/add_quote.html', context={'form': form, "tags": tags})

    def post(self, request):
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()
            tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in tags.iterator():
                new_quote.tags.add(tag)
            return redirect(to='quotes:main')
        return render(request, 'quotes/add_quote.html', {'form': form})


class AuthorInformation(View):

    def get(self, request, author_pk):
        author = get_object_or_404(Author, pk=author_pk)

        return render(request, 'quotes/author.html', context={"author": author})


class TagQuote(View):

    def get(self, request, tag_name):
        quotes = Quote.objects.filter(tags__name=tag_name)
        return render(request, 'quotes/index.html', context={'quotes': quotes})


class PopularQuotes(View):

    def get(self, request):
        quotes = Quote.objects.annotate(t_count=Count('tags')).order_by('-t_count')[:10]
        return render(request, 'quotes/index.html', context={'quotes': quotes})


