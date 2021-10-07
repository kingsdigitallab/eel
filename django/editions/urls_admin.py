from django.conf.urls.defaults import *
from editions import text_views, admin_views

urlpatterns = patterns(
    '',
    (r'^(editions/)$', admin_views.editions),
    (r'^editions/edition/(\d+)/download/$',
     text_views.edition_download_view),
    (r'^editions/edition/(\d+)/text/$',
     text_views.edition_text_view),
    (r'^editions/edition/(\d+)/text/preview/$',
     text_views.edition_text_preview_view),
    (r'^editions/edition/(\d+)/translation/preview/$',
     text_views.edition_translation_preview_view),
    (r'^editions/edition/(\d+)/text/test/$',
     text_views.edition_text_test_view),
    (r'^editions/edition/(\d+)/translation/$',
     text_views.edition_trans_text_view),
    (r'^editions/witness/(\d+)/transcription/$',
     text_views.witness_transc_text_view),
    (r'^editions/witness/(\d+)/translation/$',
     text_views.witness_transl_text_view),
    (r'^editions/witness/(\d+)/transcription/preview/$',
     text_views.edition_witness_transcription_preview_view),
    (r'^editions/witness/(\d+)/translation/preview/$',
     text_views.edition_witness_translation_preview_view),
)
