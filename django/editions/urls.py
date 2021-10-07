from django.conf.urls.defaults import *
import website_views
import website_text_views

urlpatterns = patterns('',
    # synopsis_urls
    # X http://localhost:8000/laws/texts/synopsis/Quadr.html
    (r'^laws/texts/synopsis/([^/]*)/$', website_views.synopsis_view),
    # laws_urls
    (r'^laws/manuscripts/([^/]+)/$', website_views.manuscript_view),
    # http://localhost:8000/laws/texts/index/
    (r'^laws/texts/index/$', website_views.text_index_view),
    # http://localhost:8000/laws/texts/cons-cn/relationships/
    (r'^laws/texts/([^/]+)/relationships/$', website_views.relationships_view),
    # http://localhost:8000/laws/texts/abt/view/
    (r'^laws/texts/([^/]+)/view/?([^/]+)?/?([^/]+)?/$', website_text_views.text_view),
    # http://localhost:8000/laws/texts/Abt/
    (r'^laws/texts/([^/]+)/$', website_views.introduction_view),
    # reference_urls
    # http://localhost:8000/reference/bibliography/?tp=a
    (r'^reference/bibliography/', website_views.bibliography_view),
    # http://localhost:8000/reference/glossary/
    (r'^reference/glossary/', website_views.glossary_view),
    # search_urls
    (r'^laws/search/?$', website_views.search_view),
)
