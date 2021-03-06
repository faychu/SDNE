import numpy as np
from utils.utils import *

class Graph(object):
    def __init__(self, file_path, ng_sample_ratio):
        suffix = file_path.split('.')[-1]
        self.st = 0
        self.is_epoch_end = False
        if suffix == "txt":
            fin = open(file_path, "r")
            firstLine = fin.readline().strip().split(" ")
            self.N = int(firstLine[0])
            self.E = int(firstLine[1])
            self.__is_epoch_end = False
            self.adj_matrix = np.zeros([self.N, self.N], np.int_)
            self.__links = np.zeros([self.E + ng_sample_ratio*self.N,3], np.int_)
            count = 0
            for line in fin.readlines():
                line = line.strip().split(' ')
                self.adj_matrix[int(line[0]),int(line[1])] += 1
                self.adj_matrix[int(line[1]),int(line[0])] += 1
                self.__links[count][0] = int(line[0])
                self.__links[count][1] = int(line[1])
                self.__links[count][2] = 1
                count += 1
            fin.close()
            if (ng_sample_ratio > 0):
                self.__negativeSample(ng_sample_ratio * self.N, count, edges.copy())
            self.__order = np.arange(self.N)
            print("getData done")
            print("Vertexes : %d  Edges : %d ngSampleRatio: %f" % (self.N, self.E, ng_sample_ratio))
        else:
            pass
            #TODO read a mat file or something like that.
        
    def __negativeSample(self, ngSample, count, edges):
        print("negative Sampling")
        size = 0
        while (size < ngSample):
            xx = random.randint(0, self.N-1)
            yy = random.randint(0, self.N-1)
            if (xx == yy or edges[xx][yy] != 0):
                continue
            edges[xx][yy] = -1
            edges[yy][xx] = -1
            self.links[size + count] = [xx, yy, -1]
            size += 1
        print("negative Sampling done")
        
        
    def sample(self, batch_size, do_shuffle = True):
        if self.is_epoch_end:
            if do_shuffle:
                np.random.shuffle(self.__order)
            else:
                self.__order = np.sort(self.__order)
            self.st = 0
            self.is_epoch_end = False 
        
        mini_batch = Dotdict()
        en = min(self.N, self.st + batch_size)
        index = self.__order[self.st:en]
        mini_batch.X = self.adj_matrix[index]
        mini_batch.adjacent_matriX = self.adj_matrix[index][:,index]
        if (en == self.N):
            en = 0
            self.is_epoch_end = True
        self.st = en
        return mini_batch
    
