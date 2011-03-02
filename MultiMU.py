#!/usr/bin/python
# Copyright (C) 2011 Ben Jeffrey. All Rights Reserved.
import Rules
import pp
import sys

Transform = Rules.Transform

def ApplyRules (WordList):
    Derivations = []
    for Word in WordList:
        WordDerivatives = Transform(Word)
        Derivations.extend(WordDerivatives)
    return Derivations




def DoleOutJobs (WordList, JobServer, NumberOfWorkers):

    EachWorkerGets = len(WordList/NumberOfWorkers)
    
    WorkedWords = []
    
    for Worker in range(0,NumberOfWorkers):
        
        WorkerWords = Wordlist[(Worker*EachWorkerGets):(Worker*(EachWorkerGets+1))]
        
        DoWork = JobServer.submit(ApplyRules, (WorkerWords,), (Transform, Rules.Transform,), (Rules,))
        
        WhatWorkerFinds = DoWork()
        
        WorkedWords += WhatWorkerFinds
     
     WordList += WorkedWords
     
     return WordList




def DoCycles (EndWord, WordList, MaxCycles, Workers=1):

    ppservers = ()
    JobServer = pp.Server(Workers, ppservers=ppservers)
    print 'Job server started with %s worker processes.' % str(JobServer.get_ncpus())	
    int (Workers)
    
    #Words = len(WordList)
    #ChunkSize= Words/Workers
    #print ChunkSize
    
    Marker = 0
    Count = 1
    
    Cycles = 0
    
    while EndWord not in WordList:
    
        
        Cycles += 1
        print "Cycles:",Cycles
        print "List length:", str(len(WordList))
        #print WordList
        
        if Cycles >= MaxCycles:
            return "Could not derive in %s cycles." % MaxCycles
            
        else:
            WordList = DoleOutJobs(WordList, JobServer, Workers)

    return ("Success!", Cycles, EndWord,)


def Run (MaxCycles=10, StartWord='MI', EndWord='MIU'):

    Derivatives = [StartWord]   # List of words

    return DoCycles (EndWord, Derivatives, MaxCycles, 2)
	
	

if __name__ == '__main__':
    print Run(10, 'MI' 'MIU')
