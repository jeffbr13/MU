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

    EachWorkerGets = len(WordList)/NumberOfWorkers
    print "Length of WordList:", len(WordList)
    print "Each worker gets:", EachWorkerGets
    
    Derivations = []
    
    for Worker in range(0,NumberOfWorkers):
        
        WorkerWords = WordList[(Worker*EachWorkerGets):(Worker*(EachWorkerGets+1))]
        
        DoWork = JobServer.submit(ApplyRules, (WorkerWords,), (Transform, Rules.Transform,), ("Rules",))
        
        WhatWorkerFinds = DoWork()
        
        Derivations.extend(WhatWorkerFinds)
     
    return Derivations




def Run (MaxCycles=10, StartWord='MI', EndWord='MU', Workers=1):
    
    print StartWord
    WordList = []

    for Process in range(0,Workers):
        WordList.append(StartWord)
    
    print WordList

    ppservers = ()
    JobServer = pp.Server(Workers, ppservers=ppservers)
    print 'Job server started with %s worker processes.' % str(JobServer.get_ncpus())	
    
    Cycles = 0
    
    while EndWord not in WordList:
    
        Cycles += 1
        
        if Cycles > MaxCycles:
            return "Could not derive '%s' in %s cycles." % (EndWord,MaxCycles)

        else:
            WordList += DoleOutJobs(WordList, JobServer, Workers)

    return ("Success!", Cycles, EndWord, 2)
	
	

if __name__ == '__main__':
    print Run(20, 'MI', 'MIUIU', 2)
