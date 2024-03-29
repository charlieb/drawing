import numpy as np
from math import sqrt
from copy import deepcopy

class Lines:
    '''Line Manager Class
    Data:
        Lines.points holds an array of 2D points
        Lines.conns holds pairs of point indeces to indicate which points are connected
        Lines.lines holds a list of lines
        Lines.conns holds pairs of point indeces to indicate which points are connected
        Lines.lines holds a list of lines. Each line is a list of connections which in sequence form a line to be drawn
        Lines.point_metadata holds one float value for each point

    Methods:
        Lines.add_line(self, conns)
            Adds a line to the drawing. A line is defined as an ordered list of connections 
            i.e. a list of indeces into Lines.conns.
        Lines.gen_metadata(self, method, init=0, start=0)
            Initializes each element in Lines.point_metadata to init value
            Walks each line assigning values Lines.point_metadata for each point in every line.
            The first point in the line is always assigned the start value
            The values are generated by calling method for each connection
            method must be a function that takes a Lines object and a connection (array of 2 point indeces) and must return a float
        Lines.transform(self, transform):
            Generates a new Lines object which is the result of transforming self with a function.
            Every line in Lines.lines is walked and transform is called on each point is transformed with transform and the new point or points 



    Usage:
    Generate and assign Lines.points and Lines.conns using whatever algorithm you like.
    Call Lines.gen_metadata with 
    '''
    def __init__(self, npoints=1000, nconnections=500):
        self.points = np.zeros((npoints, 2), dtype=np.float)
        self.point_metadata = np.zeros(npoints, dtype=np.float)
        self.conns = np.empty((nconnections, 2), dtype=np.int)
        self.lines = []
    def __repr__(self):
        res = ''
        for line in self.lines:
            res += '----------------------------------------\n'
            for conn in [self.conns[c] for c in line]:
                res += '%s => %s -> %s\n'%(conn, str(self.points[conn[0]]), str(self.points[conn[1]]))
        return res
    def add_line(self, conns):
        self.lines.append(np.array(conns, dtype=np.int))
    def count(self, conn): # gives each point the smallest possible number
        return min(self.point_metadata[conn[0]] + 1, self.point_metadata[conn[1]])
    def dist(self, conn): # gives each point the smallest possible number
        p0 = self.points[conn[0]]
        p1 = self.points[conn[1]]
        d = sqrt(np.sum((p1 - p0)**2))
        return min(self.point_metadata[conn[0]] + d, self.point_metadata[conn[1]])
    def gen_metadata(self, method, init=0, start=0):
        for i in range(self.point_metadata.size):
            self.point_metadata[i] = init
        #np.fill(self.point_metadata, init)
        for line in self.lines:
            self.point_metadata[self.conns[line[0]][0]] = start
            for conn in line:
                self.point_metadata[self.conns[conn][1]] = method(self, self.conns[conn])
    def transform(self, transformer, npoints=None, nconnections=None):
        lines = Lines(npoints=npoints, nconnections=nconnections)
    def subdivide(self):
        lines = Lines()
        
        lines.points = np.copy(self.points)
        lines.points.resize((self.points.shape[0] * 2, 2))

        lines.conns = np.copy(self.conns)
        lines.conns.resize((self.conns.shape[0] * 2, 2))

        pid = self.points.shape[0]
        cid = self.conns.shape[0]

        cmap = {}

        for i, c in enumerate(self.conns):
            lines.points[pid] = (self.points[c[0]] + self.points[c[1]]) / 2

            lines.conns[i][1] = pid
            lines.conns[cid][0] = pid
            lines.conns[cid][1] = c[1]
        
            cmap[i] = [i, cid]

            cid += 1
            pid += 1

        for line in self.lines:
            lines.lines.append([])
            for conn in line:
                lines.lines[-1].extend(cmap[conn])

        return lines

import unittest as ut

class LinesTest(ut.TestCase):
    def test_gen_metadata_square(self):
        lines = Lines(npoints=4, nconnections=4)
        lines.points[0] = [0,0]
        lines.points[1] = [0,1]
        lines.points[2] = [1,1]
        lines.points[3] = [1,0]
        lines.conns[0] = [0,1]
        lines.conns[1] = [1,2]
        lines.conns[2] = [2,3]
        lines.conns[3] = [3,0]
        lines.add_line([0,1,2,3])
        lines.gen_metadata(Lines.count, 9, 0)
        self.assertEqual(lines.point_metadata[0], 0)
        self.assertEqual(lines.point_metadata[1], 1)
        self.assertEqual(lines.point_metadata[2], 2)
        self.assertEqual(lines.point_metadata[3], 3)

    def test_gen_metadata_tree(self):
        lines = Lines(npoints=5, nconnections=4)
        lines.points[0] = [0,0]
        lines.points[1] = [0,1]
        lines.points[2] = [1,1]
        lines.points[3] = [1,0]
        lines.points[3] = [1,2]
        lines.conns[0] = [0,1]
        lines.conns[1] = [0,2]
        lines.conns[2] = [0,3]
        lines.conns[3] = [2,4]
        lines.add_line([0])
        lines.add_line([1,3])
        lines.add_line([2])
        lines.gen_metadata(Lines.count, 9, 0)
        self.assertEqual(lines.point_metadata[0], 0)
        self.assertEqual(lines.point_metadata[1], 1)
        self.assertEqual(lines.point_metadata[2], 1)
        self.assertEqual(lines.point_metadata[3], 1)
        self.assertEqual(lines.point_metadata[4], 2)

if __name__ == '__main__':

    lines = Lines(npoints=4, nconnections=4)
    lines.points[0] = [0,0]
    lines.points[1] = [0,1]
    lines.points[2] = [1,1]
    lines.points[3] = [1,0]
    lines.conns[0] = [0,1]
    lines.conns[1] = [1,2]
    lines.conns[2] = [2,3]
    lines.conns[3] = [3,0]
    lines.add_line([0,1,2,3])
    lines.gen_metadata(Lines.dist, 9, 0)
    print(lines)
    sub = lines.subdivide()
    print(lines)

    print(sub)

    ut.main()
