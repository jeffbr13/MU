#!/usr/bin/python
# Copyright (C) 2011 Ben Jeffrey. All Rights Reserved.

import Rules
import pp
import sys
import time
 # Import some stuff (including the rules to mutate the strings).
Transform = Rules.Transform

def ApplyRules (WordList):
    """
    Takes the word list and returns all the derivations
    according to the rules file.
    """
    Derivations = []
    for Word in WordList:
        WordDerivatives = Transform(Word)
        Derivations.extend(WordDerivatives)
    return Derivations


def DoleOutJobs (WordList, JobServer, NumberOfWorkers):
    """
    Takes the word list, the job server object, and the
    number of workers to use; distributes words to workers,
    collects the derivations, and returns them at the end.
    """

    EachWorkerGets = len(WordList)/NumberOfWorkers
    Derivations = []
    ListOfWorkers = []
 # Sort out how the word list is distributed, then
 # set up worker processes to be run, in a list.
    for Worker in range(0,NumberOfWorkers):
        StartMarker = (Worker*EachWorkerGets)
        EndMarker = ((Worker+1)*EachWorkerGets)        
        WorkerWords = WordList[StartMarker:EndMarker]
        ActualWorker = JobServer.submit(ApplyRules, (WorkerWords,), (Transform, Rules.Transform,), ("Rules",))
        ListOfWorkers.append(ActualWorker)

 # Run all the worker processes in the list,
 # and collect their results.
    for Worker in ListOfWorkers:
        WhatWorkerFinds = Worker()
        Derivations.extend(WhatWorkerFinds)
     
    return Derivations


def Run (MaxCycles=10, StartWord='MI', EndWord='MU', Workers=1):
    
 # Create list to hold strings, with a copy for each processor.
    WordList = []
    for Process in range(0,Workers):
        WordList.append(StartWord)
 # Set up the environment with: a job server for multiple
 # worker processes, a cycle counter, and a timer.
    ppservers = ()
    JobServer = pp.Server(Workers, ppservers=ppservers)
    #print 'Job server started with %s worker processes.' % str(JobServer.get_ncpus())	
    Cycles = 0
    InitialiseTime = time.time()

    while EndWord not in WordList:  
        
        if Cycles >= MaxCycles:
            return "Sorry. '%s' wasn't found in %s cycle(s); took %s seconds on %s core(s)." %(EndWord, Cycles, str(time.time()-InitialiseTime)[:6], Workers)
            
        else:
            StartTime = time.time()
 # If we haven't found the word, and haven't reached
 # the max no. of cycles yet, set the word list to all
 # the derivations of the previous one.
            WordList = DoleOutJobs(WordList, JobServer, Workers)
            Cycles += 1
            #print "Cycle %s completed: %s words in WordList after %s seconds." %(Cycles, len(WordList), (time.time()-StartTime))

 # If the string ends up in the word list, the loop ends,
 # and we get to this return statement.
    return "Success! '%s' found in %s cycle(s); took %s seconds on %s core(s)." %(EndWord, Cycles, str(time.time()-InitialiseTime)[:6], Workers)
	
 # If this script is run alone (ie, not imported by
 # another) then this bit is run.
if __name__ == '__main__':

 # These IF statements just use the command line
 # arguments given to figure out what to do next.
 
    if len(sys.argv)<2:
 # If only the script name is given, prints the contents
 # of the INSTRUCTIONS file.
        InstructionsFile = open('INSTRUCTIONS', 'r')
        Instructions = InstructionsFile.read()
        InstructionsFile.close()
        print Instructions

    elif sys.argv[1] == 'a':
        print Run(20, 'MI', 'MU')
    
    elif len(sys.argv)<5:
        print Run(int(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
    
    else:
        print Run(int(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), int(sys.argv[4]))

