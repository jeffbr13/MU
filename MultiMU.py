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
    #print "Length of WordList:", len(WordList)
    
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
    
    if len(sys.argv) == 1:     #Instructions!
        print
        print " MU finds whether you can derive 'MU' from 'MI' using the rules"
        print " printed in 'Godel, Escher, Bach' (hint - you can't) using a"
        print " breadth-first, brute-force method (now with added cores!)."
        print
        print " Arguments:"
        print "     1st argument is the number of derivation cycles to compute."
        print "     2nd argument is the starting string."
        print "     3rd argument is the string you want to achieve."
        print "     4th argument is the number of processors to use. Leave blank for auto."
        print " i.e.  To run 50 cycles with 2 cores and see if it produces 'MI' from 'MU',"
        print "       then at the command line, while in the right directory, type:"
        print
        print "     ./MU 50 'MU' 'MI' 2"
        print

    elif sys.argv[1] == 'a':
        print Run(20, 'MI', 'MU')
    
    elif len(sys.argv)<5:
        print Run(int(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
    
    else:
        print Run(int(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), int(sys.argv[4]))

