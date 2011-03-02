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
    #print "Each worker gets:", EachWorkerGets
    
    Derivations = []
    ListOfWorkers = []
    
    for Worker in range(0,NumberOfWorkers):
        
        StartMarker = (Worker*EachWorkerGets)
        EndMarker = ((Worker+1)*EachWorkerGets)
        
        WorkerWords = WordList[StartMarker:EndMarker]
        
        
        ActualWorker = JobServer.submit(ApplyRules, (WorkerWords,), (Transform, Rules.Transform,), ("Rules",))
        
        
        ListOfWorkers.append(ActualWorker)
        
    for Worker in ListOfWorkers:
        
        WhatWorkerFinds = Worker()
        Derivations.extend(WhatWorkerFinds)
     
    return Derivations




def Run (MaxCycles=10, StartWord='MI', EndWord='MU', Workers=1):
    
    #Create list to hold strings, with a copy for each processor.
    WordList = []
    for Process in range(0,Workers):
        WordList.append(StartWord)

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
    print Run(20, 'MI', 'MIIUIIUIUU', 2)
