'''
Created on Jul 20, 2012

@author: petrbouchal
'''

from BusinessPlans import *

#===============================================================================
# #===============================================================================
# # ADVANCED ANALYTICS 3: TIME SERIES
# #===============================================================================
#===============================================================================

#TODO: build time-series analytics

# the snapshot data for this is in alldata and in the output of the previous section
# other data will need to be taken from previous reports - need a system for iteration
# need to adapt if 'static' things actually change over time [scheduled dates, ids, actions coming in and out]

# first step will be to build time series of aggregates and see if changes are real or noise from changes in units
# checks should include
#     all subactions present in previous period are present in this one
#     subactions with the same ID have the same titles
#     subactios belong to the same actions, actions to the same priorities, priorities to the same departments
#        in other words, the hypothetical linking indices haven't been broken by a change in the underlying data structure
# this would ideally be done by querying things from relational database
