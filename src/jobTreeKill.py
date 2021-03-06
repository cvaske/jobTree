#!/usr/bin/env python

#Copyright (C) 2011 by Benedict Paten (benedictpaten@gmail.com)
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

"""Kills any running jobs trees in a rogue jobtree.
"""

import os

import xml.etree.ElementTree as ET
from jobTree.src.bioio import logger
from jobTree.src.bioio import getBasicOptionParser
from jobTree.src.bioio import parseBasicOptions

from jobTree.src.jobTreeRun import loadTheBatchSystem

def main():
    parser = getBasicOptionParser("usage: %prog [options]", "%prog 0.1")
    
    parser.add_option("--jobTree", dest="jobTree", 
                      help="Directory containing the job tree to kill")
    
    options, args = parseBasicOptions(parser)
    logger.info("Parsed arguments")
    assert len(args) == 0 #This program takes no arguments
    assert options.jobTree != None #The jobtree should not be null
    assert os.path.isdir(options.jobTree) #The job tree must exist if we are going to kill it.
    logger.info("Starting routine to kill running jobs in the jobTree: %s" % options.jobTree)
    config = ET.parse(os.path.join(options.jobTree, "config.xml")).getroot()
    batchSystem = loadTheBatchSystem(config) #This should automatically kill the existing jobs.. so we're good.
    for job in batchSystem.getIssuedJobIDs(): #Just in case we do it again.
        batchSystem.killJobs(job)
    logger.info("All jobs SHOULD have been killed")

def _test():
    import doctest
    return doctest.testmod()

if __name__ == '__main__':
    _test()
    main()
