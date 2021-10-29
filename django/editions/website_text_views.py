# Authors: Geoffroy Noel, King's College London, 2009-2020
#
import re
from django.conf import settings
from cch.views.utils import get_template, get_json_response
from models import Version_Witness, Version
from views_utils import get_page_not_found


def text_view(request, slug, left_code='', right_code=''):
    codes = [left_code, right_code]

    if request.REQUEST.get('zoom', 0):
        return text_view_zoom(request, slug)

    if len(request.REQUEST.get('action', '')) > 0:
        return text_view_ajax(request, slug)

    versions = Version.objects.filter(slug=slug)
    if versions.count() > 0:
        version = versions[0]
        context = {'version': version}
        edition = version.get_an_edition(show_all=settings.DEBUG)

        if edition:
            context['edition'] = edition
            set_context_documents(context, codes)

        context['base_url'] = re.sub(
            ur'(/view).*$', r'\1/', request.build_absolute_uri())
        import time
        context['unique_number'] = time.time()

        return get_template('website/text_view', context, request)
    else:
        return get_page_not_found(request)


def text_view_zoom(request, slug):
    context = {}
    context['image_url'] = request.REQUEST.get('src', '')
    context['image_server_url'] = settings.IMAGE_SERVER_URL
    return get_template('website/folio_zoom', context, request)


def text_view_ajax(request, slug):
    action = request.REQUEST.get('action', '')
    json_list = {'error': 'unknown action (%s)' % action}

    if action == 'load_doc':
        doc_key = request.REQUEST.get('doc_key', None)
        json_list = {'doc_info': {}}
        json_list['doc'] = get_document(
            slug, doc_key, request.REQUEST.get(
                'panel', 0), json_list['doc_info'], request)

    if action == 'post_comment':
        doc_key = request.REQUEST.get('doc_key', None)
        json_list['error'] = 'user not logged in'
        if request.user and request.user.is_authenticated():
            json_list['error'] = 'referenced text not found'
            from models import User_Comment
            from django.contrib.contenttypes.models import ContentType
            record = get_record_from_doc_key(slug, doc_key, request)
            edition = get_edition_from_version_slug(slug)
            if record:
                del json_list['error']
                comment = User_Comment()
                comment.userid = request.user.id
                comment.comment = request.REQUEST.get('comment', '')
                comment.content_type = ContentType.objects.get_for_model(
                    record.__class__).id
                comment.objectid = record.id
                comment.editionid = edition.id
                comment.division = re.sub(
                    '-r-.*$', '', request.REQUEST.get('refid', ''))
                private = request.REQUEST.get('private', '0')
                comment.private = ((private == '1') or (private == 1))
                comment.archived = False
                comment.save()

                json_list = {'doc_info': {}}
                # TODO: remove hard-coded 2
                json_list['doc'] = get_document(
                    slug, 'user-comments', 2, json_list['doc_info'], request)

    return get_json_response(json_list)


def get_edition_from_version_slug(slug):
    ret = None
    versions = Version.objects.filter(slug=slug)
    if versions.count():
        ret = versions[0].get_an_edition(show_all=settings.DEBUG)
    return ret


def get_record_from_doc_key(slug, doc_key, request=None):
    ret = None
    edition = get_edition_from_version_slug(slug)
    if edition:
        if doc_key == 'edition':
            ret = edition
        if doc_key == 'translation':
            ret = edition.edition_translation
        if ret is None:
            parts = doc_key.split('-')
            version_witnesses = Version_Witness.objects.filter(
                witness__manuscript__sigla__iexact=parts[0], version=edition.version)
            if version_witnesses.count():
                witness = version_witnesses[0].witness
                if len(parts) == 1:
                    ret = witness.witness_transcription
                else:
                    if parts[1] == 'translation':
                        ret = witness.witness_transcription.witness_translation
                    if parts[1] == 'image':
                        ret = witness

    return ret


def get_document(slug, doc_key, panel_index, doc_info, request=None):
    ret = None

    doc_info['witnessid'] = 0
    doc_info['pagination'] = 1
    doc_info['chapterisation'] = 1

    edition = get_edition_from_version_slug(slug)
    if edition:
        if doc_key == 'edition':
            ret = edition.rendered_edition
        if doc_key == 'translation':
            ret = edition.rendered_translation
        if doc_key == 'commentary':
            doc_info['pagination'] = 0
            ret = edition.rendered_commentary
        if doc_key == 'apparatus':
            doc_info['pagination'] = 0
            ret = edition.rendered_apparatus
        if doc_key == 'user-comments':
            from django.contrib.auth.models import User
            users = {}
            for user in User.objects.all():
                users[user.id] = user
            from models import User_Comment
            doc_info['pagination'] = 0
            comments_xml = ur''
            division = ''
            for comment in User_Comment.objects.filter(
                    editionid=edition.id, archived=False).order_by('division', 'id'):
                private = ''
                private_label = ''
                current_user = 'current-user'
                if request is None or comment.userid != request.user.id:
                    current_user = ''
                if comment.private:
                    if request is None or comment.userid != request.user.id:
                        continue
                    private = 'private'
                    private_label = '<span class="private-label" title="Only you can see this comment.">[private]</span>'
                comment_xml = ur'''<div class="comment user-%s %s %s">
                    <p class="comment-heading"><span class="comment-user">%s</span> - %s %s</p>
                    <div class="comment-body">%s</div>
                </div>''' % (comment.userid, private, current_user, users[comment.userid], comment.timestamp.strftime('%a %d %b %Y at %I:%M %p'), private_label, comment.comment)
                if division != comment.division:
                    comment_xml = ur'<div id="a-%s-uc-%s-r-%s-%s" class="anchor anchor-uc">' % (
                        panel_index, comment.division, comment.content_type, comment.objectid) + comment_xml
                    if division != '':
                        comment_xml = ur'</div>' + comment_xml
                    division = comment.division
                comments_xml = comments_xml + comment_xml
            if division != '':
                comments_xml = comments_xml + ur'</div>'
            ret = ur'''<div class="comments">%s</div>''' % comments_xml
        if ret is None:
            parts = doc_key.split('-')
            version_witnesses = Version_Witness.objects.filter(
                witness__manuscript__sigla__iexact=parts[0], version=edition.version)
            if version_witnesses.count():
                witness = version_witnesses[0].witness
                doc_info['witnessid'] = witness.id
                if len(parts) == 1:
                    ret = witness.witness_transcription.rendered_text
                else:
                    if parts[1] == 'translation':
                        ret = witness.witness_transcription.witness_translation.rendered_text
                    if parts[1] == 'image':
                        doc_info['chapterisation'] = 0
                        ret = witness.rendered_facsimiles

    if ret is None:
        ret = '[NOT FOUND]'
    else:
        # insert the index of hte panel in the id of the element
        # to make the id are unique on the webpage
        ret = re.sub(ur'#p#', '%s' % panel_index, ret)
    return ret


def is_text_empty(text):
    return text is None or len(text) < 10


def set_context_documents(context, codes):
    default = ''

    context['documents'] = []

    if context['edition'].rendered_commentary and not is_text_empty(
            context['edition'].rendered_commentary):
        context['documents'].append(
            {'key': 'commentary', 'label': 'Commentary', 'default': ['edition', 'commentary']})
        if not default:
            default = 'commentary'

    if context['edition'].edition_translation and not is_text_empty(
            context['edition'].edition_translation.text):
        context['documents'].append({'key': 'translation',
                                     'label': 'Translation of the edition',
                                     'default': ['edition',
                                                 'translation']})
        if not default:
            default = 'translation'

    if context['edition'].rendered_apparatus and not is_text_empty(
            context['edition'].rendered_apparatus):
        context['documents'].append(
            {'key': 'apparatus', 'label': 'Critical apparatus', 'default': ['edition', 'apparatus']})
        if not default:
            default = 'apparatus'

    for witness in context['edition'].version.get_witnesses():
        transcription = witness.witness_transcription
        witness_label = witness.manuscript.sigla
        witness_slug = witness_label.lower()

        if transcription:
            if not is_text_empty(transcription.text):
                context['documents'].append({'key': witness_slug,
                                             'label': witness_label + ' (Transcription)',
                                             'default': [witness_slug, witness_slug + '-translation']})
            if transcription.witness_translation and not is_text_empty(
                    transcription.witness_translation.text):
                context['documents'].append({'key': witness_slug + '-translation',
                                             'label': witness_label + ' (Translation)',
                                             'default': [witness_slug, witness_slug + '-translation']})

        if not witness.hide_from_listings and not witness.manuscript.hide_from_listings \
                and witness.manuscript.checked_folios and witness.get_first_available_folio_image():
            context['documents'].append({'key': witness_slug + '-image',
                                         'label': witness_label + ' (Facsimiles)',
                                         'default': [witness_slug, witness_slug + '-image']})
            if not default:
                default = witness_slug + '-image'

    context['documents'].insert(
        0, {'key': 'edition', 'label': 'Edition', 'default': ['edition', default]})

    doc_keys = {}
    for doc in context['documents']:
        doc['key'] = doc['key'].lower()
        doc_keys[doc['key']] = doc

    # clean the codes
    context['documents_selected'] = []
    for i in range(0, len(codes)):
        code = codes[i]
        if code is None:
            code = ''
        code = code.lower()
        if code not in doc_keys:
            code = ''
        codes[i] = code
        context['documents_selected'].append(re.sub(r'\..*$', r'', code))

    if context['documents_selected'][0] == '':
        context['documents_selected'][0] = context['documents'][0]['key']
    if context['documents_selected'][1] == '':
        context['documents_selected'] = doc_keys[context['documents_selected'][0]]['default']
