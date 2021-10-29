# Authors: Geoffroy Noel, King's College London, 2009-2020
#
from graph import Graph
import random

# DB -> timeline -> dynamic image coordinates (x only)
# -> layout -> serialise and save in DB
# regenerate at night 

class Layout(object):
    
    def __init__(self):
        self.m_graphs = []
        self.m_maxIteration = 1000
        self.m_minFitness = 1
        
        self.m_indices = []
        self.m_scaleFactor = 0.8
        # between 0 and 1. 0 means no crossover, 1 means that the trial vector is always preserved. 
        self.m_crossOverRate = 0.05
        self.m_trialGraph = None

    def computeLayout(self, graph, popSize=5, maxIteration=1000):
        self.m_maxIteration = maxIteration
        self.initPopulation(graph, popSize)
        bestFitness = self.m_minFitness + 1
        iteration = 1
        bestIndex = 0
        bestFitness = 1e6
        
        while (iteration <= self.m_maxIteration) and (bestFitness >= self.m_minFitness):
            bestFitness = 1e6
            #print 'Iteration %s' % iteration
            for i in range(0, len(self.m_graphs)):
                g = self.m_graphs[i]
                fitness = g.computeFitness()
                
                # mutation
                u = self.mutate(i)
                # crossover
                self.crossOver(g, u)
                
                # selection
                newFitness = u.computeFitness(fitness)
                if newFitness < fitness:
                    for i2 in u.m_bubbles:
                        g.m_bubbles[i2]['y'] = u.m_bubbles[i2]['y']
                    fitness = newFitness
                    g.invalidateFitness()
                    
                # best individual
                if fitness < bestFitness:
                    bestFitness = fitness
                    bestIndex = i
                                
            #print '\tFitness = %s' % bestFitness
            iteration += 1
        
        return self.m_graphs[bestIndex].clone()

    def initPopulation(self, graph, popSize=5):
        graph.computeNeighbours()
        self.m_graphs.append(graph.clone())
        self.m_trialGraph = graph.clone()
        for i in range(1, popSize):
            self.m_graphs.append(graph.clone())
            self.m_graphs[i].randomizeYs()
        for i in range(0, popSize):
            pass
            #print self.m_graphs[i].m_bubbles
            #print self.m_graphs[i].computeFitness()
            
        self.m_indices = range(0, popSize)
    
    def mutate(self, index):
        # pick three distinct random individuals other than index
        random.shuffle(self.m_indices)
        other_indices = []
        for i in self.m_indices:
            if self.m_indices[i] != index:
                other_indices.append(self.m_indices[i])
                if len(other_indices) >= 3: break
        
        # mutate
        ret = self.m_trialGraph
        for i in ret.m_bubbles:
            ret.m_bubbles[i]['y'] = self.m_graphs[other_indices[0]].m_bubbles[i]['y'] + self.m_scaleFactor * (self.m_graphs[other_indices[1]].m_bubbles[i]['y'] - self.m_graphs[other_indices[2]].m_bubbles[i]['y'])
        ret.invalidateFitness()
        return ret
    
    # we cross graph with trialGraph and put the result in trialGraph
    def crossOver(self, graph, trialGraph):
        indices = graph.m_bubbles.keys()
        random.shuffle(indices)
        first = True
        for i in indices:
            if not(first or random.random() < self.m_crossOverRate):
                trialGraph.m_bubbles[i]['y'] = graph.m_bubbles[i]['y']
            first = False
        trialGraph.invalidateFitness()

    def test(self):
        #random.seed(0.10)
        graph = Graph()
        graph.randomizeState(10)
        graph.saveImage('start')
        graph.computeFitness()
        graph2 = self.computeLayout(graph, 20)
        graph2.saveImage('end')
