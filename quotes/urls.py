from django.urls import path
from .views import Main, AddAuthor, AddTag, AddQuote, AuthorInformation, TagQuote, PopularQuotes

app_name = 'quotes'

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('add-author/', AddAuthor.as_view(), name='add_author'),
    path('add-tag/', AddTag.as_view(), name='add_tag'),
    path('add-quote/', AddQuote.as_view(), name='add_quote'),
    path('author/<int:author_pk>', AuthorInformation.as_view(), name='author_information'),
    path('tag/<str:tag_name>', TagQuote.as_view(), name='quotes_with_tag'),
    path('popular/', PopularQuotes.as_view(), name='popular_quotes'),
]
