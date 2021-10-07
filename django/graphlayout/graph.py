import random
import math
from copy import deepcopy

class Graph(object):  
    
    def __init__(self):
        self.m_boundaries = {'x0': 0, 'y0': 0, 'x1': 600, 'y1': 400}
        self.m_bubbles = {}
        self.m_links = {}
        self.m_radius = 25
        self.m_radiusPadding = self.m_radius * 1.75
        self.m_fitness = -1
        
    def init(self, bubbles, links, boundaries, radius):
        self.m_bubbles = bubbles
        self.m_links = links
        self.m_boundaries = boundaries
        self.m_radius = radius
        self.computeNeighbours()
        
    def invalidateFitness(self):
        self.m_fitness = -1
        
    def computeNeighbours(self):
        # compute all the pairs of bubbles which intersect when placed on a horizontal line.
        # the layout will have to move the individual bubbles up or down to prevent intersection.
        self.m_neighbours = []
        # 1. sort the bubbles by x coordinate
        indices = []
        for i in self.m_bubbles:
            indices.append((i, self.m_bubbles[i]['x']))
        indices = sorted(indices, key=lambda item: item[1])
        # 2. for each bubble find its neighbours on the right hand side
        for i in range(0, len(indices)):
            for i2 in range(i + 1, len(indices)):
                # *2 because the radius is around each bubble in a pair
                if indices[i2][1] - indices[i][1] < self.m_radiusPadding * 2:
                    self.m_neighbours.append((indices[i][0], indices[i2][0]))
                else:
                    break
        # extra
        # 3. for each link find the bubble located between both ends
        for i in range(0, len(indices)): indices[i] = indices[i][0]
        for i in self.m_links:
            link = self.m_links[i]
            link['covers'] = []
            (i0, i1) = (indices.index(link['from']), indices.index(link['to']))
            if i0 > i1: (i0, i1) = (i1, i0)
            link['covers'] = indices[i0+1:i1]
            
    def computeFitness(self, refFitness=1e6):
        # stop early if the fitness > refFitness
        if self.m_fitness == -1:
            self.m_fitness = 0
            self.m_fitness += self.fitnessCompactness()
            if self.m_fitness < refFitness: 
                self.m_fitness += self.fitnessIntersection()
            if self.m_fitness < refFitness: 
                self.m_fitness += self.fitnessHorizontal()
            if self.m_fitness < refFitness: 
                self.m_fitness += self.fitnessLinkCrossBubble()
        return self.m_fitness

    def fitnessHorizontal(self):
        ret = 0
        height = (self.m_boundaries['y1'] - self.m_boundaries['y0'])
        # 1. we want horizontal lines as much as possible
        # this layout is more elegant and compact and it also tends to avoid lines crossing each other.
        # penalty = the sum of all the angles (in degrees). 0 being horizontal.
        for i in self.m_links:
            link = self.m_links[i]
            xdiff = self.m_bubbles[link['to']]['x'] - self.m_bubbles[link['from']]['x']
            if xdiff == 0: xdiff = 1e-6
            #angle = math.degrees(math.fabs(math.atan((self.m_bubbles[link['to']]['y'] - self.m_bubbles[link['from']]['y']) / xdiff))) / 45 * height / 2
            angle = math.fabs(self.m_bubbles[link['to']]['y'] - self.m_bubbles[link['from']]['y']) * 2 * 2
            ret += angle
        return ret
    
    def fitnessCompactness(self):
        height = (self.m_boundaries['y1'] - self.m_boundaries['y0'])
        ret = 0        
        # 2. 1 is not enough for two reasons:
        # a) because even a small angle can be very visible for long link streching across the whole diagram
        # b) because the diagram can be made of two groups of horizontal lines equally separated from the center
        #    so the mean is the center.
        # => we give a penalty for the deviation for the cummulative deviation of each bubble from the center
        centery = (self.m_boundaries['y1'] + self.m_boundaries['y0']) / 2
        for i in self.m_bubbles:
            ret += math.fabs(self.m_bubbles[i]['y'] - centery) / 2
        return ret        
    
    def fitnessCenterDeprecated(self):
        ret = 0
        # 3. we want the graph to be centered vertically
        # ymean = [0, 90], with 90 being as far as the boundaries and 0 being in the middle
        ymean = 0
        for i in self.m_bubbles:
            ymean += self.m_bubbles[i]['y']
        ymean /= len(self.m_bubbles)
        ymean -= (self.m_boundaries['y1'] + self.m_boundaries['y0']) / 2.0
        ymean = math.fabs(ymean)
        ymean *= (1.0 / ((self.m_boundaries['y1'] - self.m_boundaries['y0']) / 2)) * 90
        ret += ymean
        return ret
    
    def fitnessIntersection(self):
        ret = 0        
        height = (self.m_boundaries['y1'] - self.m_boundaries['y0'])
        maxSmallPenalty = len(self.m_bubbles) * height / 2
        # 4. we don't want the bubbles to intersect.
        # penalty is the sum, for each pair of bubbles, of the normalised diameter of their intersection * 90 + 90
        intersection = 0
        for pair in self.m_neighbours:
            distance = math.hypot(self.m_bubbles[pair[0]]['x'] - self.m_bubbles[pair[1]]['x'], self.m_bubbles[pair[0]]['y'] - self.m_bubbles[pair[1]]['y'])
            if distance < (self.m_radiusPadding * 2):
                intersection += ((self.m_radiusPadding * 2) - distance) / (self.m_radiusPadding * 2) * maxSmallPenalty + maxSmallPenalty
                # print 'penalty = %s' % (self.m_radius - distance)
        ret += intersection
        return ret
        
    def fitnessLinkCrossBubble(self):
        ret = 0
        height = (self.m_boundaries['y1'] - self.m_boundaries['y0'])
        maxSmallPenalty = len(self.m_bubbles) * height / 2
        # 4. we don't want a line to cross a bubble
        for i in self.m_links:
            link = self.m_links[i]
            (x1, y1) = (self.m_bubbles[link['from']]['x'], self.m_bubbles[link['from']]['y']) 
            (x2, y2) = (self.m_bubbles[link['to']]['x'], self.m_bubbles[link['to']]['y']) 
            for j in link['covers']:
                y0 = self.m_bubbles[j]['y']
                if (y0 < y1 - self.m_radiusPadding and y0 < y2 - self.m_radiusPadding) or (y0 > y1 + self.m_radiusPadding and y0 > y2 + self.m_radiusPadding): continue
                x0 = self.m_bubbles[j]['x']
                distance = math.fabs((x2-x1)*(y1-y0) - (x1-x0)*(y2-y1)) / math.hypot(x2 - x1, y2 - y1)  
                if distance < self.m_radiusPadding:
                    ret += (self.m_radiusPadding - distance) / self.m_radiusPadding * maxSmallPenalty + maxSmallPenalty
        return ret
    
    def randomizeState(self, bubbleCount=5):
        for i in range(0, bubbleCount):
            self.m_bubbles[i] = {'x': self.m_boundaries['x0'] + random.random() * (self.m_boundaries['x1'] - self.m_boundaries['x0']), 
                                 'y': self.m_boundaries['y0'] + random.random() * (self.m_boundaries['y1'] - self.m_boundaries['y0']), 
                                 'title': i}
        
        
        # create random links
        ids = self.m_bubbles.keys()
        for i in range(0, int(bubbleCount * 1.5)):
            link = {'from': random.randint(0, bubbleCount - 1), 'to': None}
            while link['to'] is None or link['to'] == link['from']:
                link['to'] = random.randint(0, bubbleCount - 1)
            link['from'] = ids[link['from']]
            link['to'] = ids[link['to']]
            self.m_links[i] = link
            
        self.computeNeighbours()
        
    def clone(self):
        ret = Graph()
        ret.m_boundaries = deepcopy(self.m_boundaries.copy())
        ret.m_bubbles = deepcopy(self.m_bubbles.copy())
        ret.m_links = deepcopy(self.m_links.copy())
        ret.m_neighbours = deepcopy(self.m_neighbours)
        ret.m_radius = self.m_radius
        ret.m_radiusPadding = self.m_radiusPadding
        return ret
    
    def randomizeYs(self):
        for i in self.m_bubbles.keys():
            self.m_bubbles[i]['y'] = self.m_boundaries['y0'] + random.random() * (self.m_boundaries['y1'] - self.m_boundaries['y0'])
    
    def computeError(self):
        pass
    
    def saveImage(self, name='graph'):
        import Image, ImageDraw
        (x0, y0) = (self.m_boundaries['x0'], self.m_boundaries['y0'])
        (xl, yl) = (self.m_boundaries['x1'] - self.m_boundaries['x0'], self.m_boundaries['y1'] - self.m_boundaries['y0'])
        image = Image.new('RGB', [xl, yl])
        draw = ImageDraw.Draw(image)
        # show the links
        draw.rectangle([0, 0, xl, yl], fill='#ffffff')
        for i in self.m_links:
            l = self.m_links[i]
            middle = [(self.m_bubbles[l['from']]['x'] + self.m_bubbles[l['to']]['x']) / 2 - x0, 
                      (self.m_bubbles[l['from']]['y'] + self.m_bubbles[l['to']]['y']) / 2 - y0]
            draw.line([(self.m_bubbles[l['from']]['x'] - x0, self.m_bubbles[l['from']]['y'] - y0), 
                       (self.m_bubbles[l['to']]['x'] - x0, self.m_bubbles[l['to']]['y'] - y0)], 
                      fill='#00ff00')
            draw.text(middle, '%s' % i, fill='#00ff00')
            #self.m_bubbles[i] link = {'from': random.randint(0, bubbleCount - 1), 'to': None}
        # show the bubbles
        for i in self.m_bubbles:
            b = self.m_bubbles[i]
            #draw.point([b['x'] - x0, b['y'] - y0], fill='#000000')
            draw.arc([int(b['x'] - x0 - self.m_radius), int(b['y'] - y0 - self.m_radius), int(b['x'] - x0 + self.m_radius), int(b['y'] - y0 + self.m_radius)], 0, 360, fill='#000000')
            draw.text([b['x'], b['y']], '%s' % i, fill='#000000')
        image.save('%s.png' % name)
    

