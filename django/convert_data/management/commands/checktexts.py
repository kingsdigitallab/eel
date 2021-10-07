# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from optparse import make_option
# from editions.models import *
from editions.models import (
    Commentary, Edition, Folio_Image, Witness, Hyparchetype,
    Witness_Transcription, Witness_Translation
)
import sys
import re
from whoosh.fields import *


class Command(BaseCommand):

    requires_model_validation = False

    def handle(self, *test_labels, **options):
        print '%-25s|%6s|%10s' % ('Ref', 'Depth', 'Size')
        for edition in Edition.objects.all().order_by('id'):
            self.check_text(
                'Ed #%5s %s' %
                (edition.id, edition.version.slug),
                edition.text
            )

    def check_text(self, label, text):
        msg = []

        # calculate the max nesting depth of the xml elements
        from editions.text_views import get_divs_tree, get_dom_from_text
        node = get_dom_from_text(text)

        nodes = [[node, 0]]
        max_nesting_depth = 0
        while len(nodes):
            node, lvl = nodes.pop(0)
            nodes.extend([[anode, lvl + 1] for anode in node.childNodes])
            if lvl > max_nesting_depth:
                max_nesting_depth = lvl

        if max_nesting_depth > 20:
            msg.append('DEEP')

        print '%-25s|%6s|%10s|%s' % (label, max_nesting_depth, len(text), ' '.join(msg))
