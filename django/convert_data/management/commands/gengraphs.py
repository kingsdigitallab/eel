# Authors: Geoffroy Noel, King's College London, 2009-2020
#
from django.core.management.base import BaseCommand
from optparse import make_option
from eel.editions.models import *
import sys
import re
import urllib2
from graphlayout.graph import Graph
from graphlayout.layout import Layout
from django.db.models import Q
from datetime import date, timedelta
import math


class Command(BaseCommand):
    '''
        Pre-compute the graph representing the filiatin among the versions.
        These graph will be displayed on the website as SVG. 
    '''
#    option_list = BaseCommand.option_list + (
#        make_option('--verbosity', action='store', dest='verbosity', default='1',
#            type='choice', choices=['0', '1', '2'],
#            help='Verbosity level; 0=minimal output, 1=normal output, 2=all output'),
#        make_option('--noinput', action='store_false', dest='interactive', default=True,
#            help='Tells Django to NOT prompt the user for input of any kind.'),
#    )
#    help = 'Generate work.indexed_title and work.indexed_english_title for all work records.'
#    args = '[appname ...]'

    requires_model_validation = False
    
    def __init__(self):
        self.m_image_width = 750
        self.m_image_height = 400
        self.m_radius = 25
        self.m_image_width_padding = self.m_radius + 5
        
        self.m_population = 20
        self.m_iterations = 1000
        
        self.m_version_regen_count = 0
        self.m_version_with_graph = 0
    
    def handle(self, *test_labels, **options):
        print 'Pop = %s; Iterations = %s; radius = %s' % (self.m_population, self.m_iterations, self.m_radius)
        self.generateGraphs()
        
    def generateGraphs(self):
        
        versions = Version.objects.all()
        for version in versions:
            # TODO: remove this
            #if version.id == 612:
            self.generateGraph(version)
        
        print '%s version, %s with graphs, %s regenerated.' % (versions.count(), self.m_version_with_graph, self.m_version_regen_count)

    def generateGraph(self, version):
        print 'Version %s, %s' % (version.id, version.slug)

        # 1. general relationships data from the database
        rel_data = self.get_rel_data_from_version(version, self.m_radius)
        print '\tsig = %s' % rel_data['signature']
        
        # 2. generate the layouts if necessary
        rel_data_old = version.get_graph()
        #rel_data_old = None
        if rel_data_old is None or rel_data_old['signature'] != rel_data['signature']:
            links_count = len(rel_data['links'].keys())
            if links_count:
                print '\t%s links' % links_count
                graph = Graph()
                graph.init(rel_data['texts'], rel_data['links'], {'x0': 0, 'y0': 0, 'x1': self.m_image_width - self.m_image_width_padding * 2, 'y1': self.m_image_height}, self.m_radius)
                layout = Layout()
                graph.randomizeYs()
                #graph.saveImage('v-%s-0' % version.id)
                f0 = graph.computeFitness()            
                graph = layout.computeLayout(graph, self.m_population, self.m_iterations)
                f1 = graph.computeFitness()            
                #graph.saveImage('v-%s-1' % version.id)
                #print graph
                # copy the Ys
                for id in graph.m_bubbles:
                    rel_data['texts'][id]['y'] = graph.m_bubbles[id]['y']
                print '\tfitness: %s -> %s' % (f0, f1)
                
                self.m_version_regen_count += 1
                
                self.crop_vertically(rel_data)
                        
            version.set_graph(rel_data)
            version.save()
        
        if len(rel_data['links']) > 0:
            self.m_version_with_graph += 1

    def crop_vertically(self, rel_data):
        # crop and recenter Ys
        (miny, maxy) = (-1, -1)
        for id in rel_data['texts']:
            text = rel_data['texts'][id]
            y = text['y']
            if miny == -1 or y < miny: miny = y
            if maxy == -1 or y > maxy: maxy = y
        miny = miny - 2 * self.m_radius
        maxy = maxy + 2 * self.m_radius + 2 * self.m_radius
        for id in rel_data['texts']:
            text = rel_data['texts'][id]
            text['y'] = text['y'] - miny
        rel_data['image']['height'] = maxy - miny
        rel_data['image']['width'] = rel_data['timeline']['maxp'] + 2 * self.m_radius

    def get_rel_data_from_version(self, version, max_depth=2, radius=25):
        rel_data = {
                'texts': {},
                'links': {},
                'languages': {},
                'rel_types': {},
                'signature': 0,
                'image': {'height': self.m_image_height, 'width': self.m_image_width, 'padding': self.m_image_width_padding, 'radius': self.m_radius}, 
                }
        self._add_version_to_rel_data(version, rel_data, max_depth)
        
        (min, max) = (-1, -1)
        padding_period = 10 * timedelta(days=365)
        # resolve None dates. We pick the middle of the date range [a, b].
        # Where a = max(all preceding versions)
        # Where b = min(all following versions)
        for id in rel_data['texts']:
            text = rel_data['texts'][id]
            ret = text['x']
            if ret is None:
                ret = date(1000, 1, 1)
                range = [self._get_closest_date_from_rel(text['id'], rel_data, -1), self._get_closest_date_from_rel(text['id'], rel_data, 1)]
                #print text['short_title']
                #print range
                if range[0] is None and range[1] is not None:
                    range[0] = range[1] - padding_period
                if range[0] is not None and range[1] is None:
                    range[1] = range[0] + padding_period
                if range[0] is not None and range[1] is not None:
                    ret = range[0] + (range[1] - range[0]) / 2
                text['x'] = ret
                #print ret
                                
            if min == -1 or ret < min: min = ret
            if max == -1 or ret > max: max = ret
        
        # pad the overall date range and round it up/down
        min = min - padding_period
        min = date(int(math.floor(min.year / 10.0) * 10), 1, 1)
        max = max + padding_period
        max = date(int(math.ceil(max.year / 10.0) * 10), 1, 1)
        
        # convert all the dates into pixels
        range_in_days = max.toordinal() - min.toordinal()
        width_in_pixels_max = self.m_image_width - self.m_image_width_padding * 2 
        width_in_pixels = 4 * radius * len(rel_data['texts'].keys())
        if width_in_pixels > width_in_pixels_max: width_in_pixels = width_in_pixels_max
        
        rel_data['timeline'] = {'minp': self.m_image_width_padding, 'maxp': self.m_image_width_padding + width_in_pixels, 'mint': min.year, 'maxt': max.year} 

        padding_pixels = self.m_image_width_padding
        for id in rel_data['texts']:
            text = rel_data['texts'][id]
            text['x'] = padding_pixels + (text['x'].toordinal() - min.toordinal()) * 1.0 / range_in_days * width_in_pixels
            
        # compute signature
        rel_data['signature'] = self.m_image_width + self.m_image_height + self.m_image_width_padding + self.m_radius
        for id in rel_data['texts']:
            text = rel_data['texts'][id]
            rel_data['signature'] += text['id'] * text['x']
        for id in rel_data['links']:
            link = rel_data['links'][id]
            rel_data['signature'] += int(id) * link['from'] * link['to']
        
        return rel_data
            
    def _get_closest_date_from_rel(self, text_id, rel_data, dir=1):
        '''
            eg.     1 (None), 2 (10), 3 (None), 4 (5)
                    1 -> 2, 1 -> 3, 3 -> 4 
                    dir = 1 (to the right)
                    text_id = 1
                    We should return 5 because it is the minimum of all the dates of the neighbours
                        on the right hand side.
                    Basically we recursively follow all the paths to the neighbours and stop a path
                        when the date is not None. We return the minimum along that path.
        '''
        ret = None
        dirs = {1: 'from', -1: 'to'}
        dir_key = dirs[dir]
        other_key = dirs[-dir]
        for id in rel_data['links']:
            link = rel_data['links'][id]
            if link[dir_key] == text_id: 
                other_text = rel_data['texts'][link[other_key]]
                val = other_text['x']
                if val is None:
                    val = self._get_closest_date_from_rel(link[other_key], rel_data, dir)
                if val is not None:
                    if ret is None:
                        ret = val
                    else:
                        if dir == 1 and val < ret: ret = val
                        if dir == -1 and val > ret: ret = val                        
                    
        return ret
                    
    
    def _add_version_to_rel_data(self, version, rel_data, max_depth=2, direction=0):
        # direction: -1: find only sources, 0: find both, 1: find only targets 
        king_name = ''
        king = version.get_a_king()
        if king is not None: 
            king_name = king.name
                       
        x = version.date
        if x is not None:
            diff = x.getDateTo() - x.getDateFrom()
            diff = diff / 2
            #print diff
            x = x.getDateFrom() + diff
        
        #print '%s -> %s' % (version.date, x)
        
        rel_data['texts'][version.id] = {
                                        'short_title': version.standard_abbreviation, 
                                        'title': version.version_name(), 
                                        'slug': version.slug, 
                                        'id': version.id,
                                        'languageid': version.get_a_language().id,
                                        'king': king_name,
                                        'x': x,
                                        'y': 0,
                                        }

        # now find all the relationships to/from this version
        if max_depth > 0:
            if direction == 0:
                rels = Version_Relationship.objects.filter(Q(source=version) | Q(target=version))
            if direction == -1:
                rels = Version_Relationship.objects.filter(target=version)
            if direction == 1:
                rels = Version_Relationship.objects.filter(source=version)
            
            #print version
            
            for rel in rels:
                related_version = rel.target
                dir = 1
                if related_version == version:
                    dir = -1
                    related_version = rel.source
                #print '\t#%s: %s -> %s (dir: %s)' % (rel.id, rel.source, rel.target, dir)
                rel_data['links'][rel.id] = {
                                             'from': rel.source.id, 
                                             'to': rel.target.id,
                                             'description': rel.description,
                                             'typeid': rel.version_relationship_type.id,
                                             }
                self._add_version_to_rel_data(related_version, rel_data, max_depth - 1, dir)
        
        return rel_data

    def writeFile(self, filename, text):
        ret = True
        try:
            f = open(filename, 'w')
            f.write(text.encode('utf-8'))
            f.close()
            ret = True
        except IOError:
            print 'Error writing %s' % filename
        return ret

    def readXMLFile(self, filepath):
        ret = self.readFile(filepath)
        ret = re.sub('<?xml version="1.0"?>', '', ret)
        return ret
        
    def readFile(self, filepath):
        import codecs
        f = codecs.open(filepath, 'r', "utf-8")
        ret = f.read()
        f.close()
        return ret
    
    def replace(self, str, start, length, new):
        return str[:start]+new+str[start+length:]
    
    def warning(self, message):
        war = 'WARNING:' + message
        self.bib_tei = self.bib_tei + '<!--' + war + "-->\n"
        if message not in self.errors:
            self.errors[message] = 0
        self.errors[message] = self.errors[message] + 1
        #print war
        
    def reFind(self, pattern, string):
        ret = None
        items = re.findall(pattern, string)
        if len(items) > 0:
            ret = items[0]
        return ret
            
    def report_errors(self):
        ret = ''
        for message in self.errors:
            ret = ret + "%s x %s\n" % (self.errors[message], message)
        ret = '<!-- %s -->' % ret
        return ret
