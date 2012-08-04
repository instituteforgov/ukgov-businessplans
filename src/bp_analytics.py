'''
Created on Jul 20, 2012

@author: petrbouchal
'''
# switch for offline debugging without downloading new data

offline = 0

#from BusinessPlans import datestring, datetimestring, deptdict
#from BusinessPlans import alldata, deptsJ
import csv
from datetime import datetime

# setup structure for assigning abbreviations to department names
deptdict = {}
deptdict['Department for Communities and Local Government'] = 'DCLG'
deptdict['Ministry of Justice'] = 'MoJ'
deptdict['Ministry of Defence'] = 'MoD'
deptdict['Cabinet Office'] = 'CO'
deptdict['Department of Energy and Climate Change'] = 'DECC'
deptdict['Department for Education'] = 'DfE'
deptdict['Department for Business, Innovation and Skills'] = 'BIS'
deptdict['Department for Transport'] = 'DfT'
deptdict['Her Majesty\'s Revenue and Customs'] = 'HMRC'
deptdict['Department for Work and Pensions'] = 'DWP'
deptdict['Department of Health'] = 'DH'
deptdict['Foreign and Commonwealth Office'] = 'FCO'
deptdict['Her Majesty\'s Treasury'] = 'HMT'
deptdict['Department for Environment, Food and Rural Affairs'] = 'Defra'
deptdict['Department for International Development'] = 'DfID'
deptdict['Department for Culture, Media and Sport'] = 'DCMS'
deptdict['Home Office'] = 'HO'


from latestfile import openlatestfile

alldata0 = csv.reader(openlatestfile('../output/', 'rU', 'csv'))
alldata = []
for line in alldata0:
    alldata.append(line)
# remove header
alldata.remove(alldata[0])

# build date and time strings
now = datetime.strptime(alldata[1][-2], '%Y-%m-%d %H:%M:%S')
today = datetime.strptime(alldata[1][-1], '%Y-%m-%d')

datestring = datetime.strftime(today, '%Y-%m-%d')
datetimestring = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
filedatestring = datetime.strftime(now, '%Y%m%d_%H%M')

n_actions = float(len(alldata))
n_started = float(0)
n_ended = float(0)
n_duetostartthismonth = float(0)
n_duetoendthismonth = float(0)
n_duetostartwithin30days = float(0)
n_duetoendwithin30days = float(0)
n_startedthismonth = float(0)
n_endedthismonth = float(0)
n_startedinlast30days = float(0)
n_endedinlast30days = float(0)


# TODO: create separate overall reports for actions starting/ending and started/ended in this/past month
# TODO: create separate departmental reports for subsets of actions starting/ending and started/ended in this/past month

n_notduestart = 0
n_carriedoverstart = 0

earlystartlist = []
latestartlist = []
overduestartlist = []

earlyendlist = []
lateendlist = []
overdueendlist = []

# look at start status codes
startcodeslist = []
# create a list of start in all lines
for line in alldata:
    startcodeslist.append(line[29])
    # create set

# make a set of them - only one of each
startcodesset = set(startcodeslist)

# create empty dictionary
startcodesdict = dict()

# create dictionary keys and assign 0 as value to each
for code in startcodesset:
    startcodesdict[code] = 0

# raise value of each key for each line with a code equal to the key
for code in startcodesdict:
    for line in alldata:
        if line[29] == code:
            startcodesdict[code] += 1

# now run through end codes - documented above
endcodeslist = []
for line in alldata:
    endcodeslist.append(line[30])

endcodesset = set(endcodeslist)

endcodesdict = dict()

for code in endcodesset:
    endcodesdict[code] = 0

for code in endcodesdict:
    for line in alldata:
        if line[30] == code:
            endcodesdict[code] += 1

for line in alldata:
    if int(line[27]) == 1:
        n_started += 1
    if int(line[28]) == 1:
        n_ended += 1
    # FIXME: all these generate 0
    if line[37] == 1:
        n_duetostartthismonth += 1
    if line[38] == 1:
        n_duetoendthismonth += 1
    if line[39] == 1:
        n_duetostartwithin30days += 1
    if line[40] == 1:
        n_duetoendwithin30days += 1
    if line[41] == 1:
        n_startedthismonth += 1
    if line[42] == 1:
        n_endedthismonth += 1
    if line[43] == 1:
        n_startedinlast30days += 1
    if line[44] == 1:
        n_endedinlast30days += 1

    if ((line[30] == 'Early') & (line[34] != 'NA')):
        earlyendlist.append(float(line[34]))

    if ((line[30] == 'Late') & (line[35] != 'NA')):
        lateendlist.append(float(line[35]))

    if ((line[30] == 'Overdue') & (line[36] != 'NA')):
        overdueendlist.append(float(line[36]))

    if (line[29] == 'Not due'):
        n_notduestart += 1

    if (line[29] == 'Carried over'):
        n_carriedoverstart += 1

    if ((line[29] == 'Early') & (line[31] != 'NA')):
        earlystartlist.append(float(line[31]))

    if ((line[29] == 'Late') & (line[32] != 'NA')):
        latestartlist.append(float(line[32]))

    if ((line[29] == 'Overdue') & (line[33] != 'NA')):
        overduestartlist.append(float(line[33]))

# amount/average of late/early/overdue starts

try:
    m_daysearlystart = sum(earlystartlist) / len(earlystartlist)
except ZeroDivisionError:
    m_daysearlystart = 'NA'

try:
    m_dayslatestart = sum(latestartlist) / len(latestartlist)
except ZeroDivisionError:
    m_dayslatestart = 'NA'

try:
    m_daysoverduestart = sum(overduestartlist) / len(overduestartlist)
except ZeroDivisionError:
    m_daysoverduestart = 'NA'

# amount/average of late/early/overdue ends

try:
    m_daysearlyend = sum(earlyendlist) / len(earlyendlist)
except ZeroDivisionError:
    m_daysearlyend = 'NA'

try:
    m_dayslateend = sum(lateendlist) / len(lateendlist)
except ZeroDivisionError:
    m_dayslateend = 'NA'

try:
    m_daysoverdueend = sum(overdueendlist) / len(overdueendlist)
except ZeroDivisionError:
    m_daysoverdueend = 'NA'

n_notdueend = 0
for line in alldata:
    if (line[30] == 'Not due'):
        n_notdueend += 1

n_earlystart = len(earlystartlist)
n_earlyend = len(earlyendlist)

#TODO: add on time end/start

# TODO: add aggregate durations (scheduled, so far, completed)

n_overduestart = len(overduestartlist)
n_overdueend = len(overdueendlist)

n_latestart = len(latestartlist)
n_lateend = len(lateendlist)

t_daysoverduestart = sum(overduestartlist)
t_daysoverdueend = sum(overdueendlist)

t_dayslatestart = sum(latestartlist)
t_dayslateend = sum(lateendlist)

p_earlystart = float(n_earlystart) / float(n_started)
p_earlyend = float(n_earlyend) / float(n_ended)

n_netstarted = n_started - n_carriedoverstart

p_latestart = float(n_latestart) / float(n_started)
p_lateend = float(n_lateend) / float(n_ended)

p_overduestart = float(n_overduestart) / (float(n_started) + float(n_overduestart))
p_netoverduestart = float(n_overduestart) / (float(n_started) + float(n_overduestart) - float(n_carriedoverstart))
p_overdueend = float(n_overdueend) / (float(n_ended) + float(n_overdueend))

# TODO: calculate late/overdue start/end as percentage of duration

# calculated and percentage indicators

n_ongoing = (float(n_started) - float(n_ended))
p_ended = (float(n_ended) / float(n_actions))
p_started = (float(n_started) / float(n_actions))
p_ongoing = (float(n_ongoing) / float(n_actions))
p_startedofthoseduetostart = (float((n_started)) / (float(n_started) + float(n_overduestart)))
p_netstartedofthoseduetostart = (float((n_started) - float(n_carriedoverstart)) / (float(n_started) + float(n_overduestart) - float(n_carriedoverstart)))
p_endedofthoseduetoend = (float((n_ended)) / (float(n_ended) + float(n_overdueend)))

# print a basic summary

print "SUMMARY OF PROGRESS ON ALL ACTIONS FOR WHOLE OF GOVERNMENT"
print
print 'Total actions in business plans: ' + str(int(n_actions))
print 'Number started: ' + str(int(n_started))
print 'Number started, excluding those carried over from last business plans: ' + str(int(n_started) - int(n_carriedoverstart))
print 'Total carried over: ' + str(int(n_carriedoverstart))
print
print 'Number completed: ' + str(int(n_ended))
print 'Percent completed of total: ' + str(round(p_ended * 100, 2)) + '%'
print
print 'Percent started of total: ' + str(round(p_started * 100, 2)) + '%'
print 'Percent started of those due to start: ' + str(round(p_startedofthoseduetostart * 100, 2)) + '%'
print 'Percent started of those due to start, excluding those carried over from previous business plans: ' + str(round(p_netstartedofthoseduetostart * 100, 2)) + '%'
print
print 'Percent completed of those due to complete: ' + str(round(p_endedofthoseduetoend * 100, 2)) + '%'
print 'Percent ongoing: ' + str(round(p_ongoing * 100, 2)) + '%'
print

print 'Total number of actions which are overdue to start:',
print n_overduestart
print 'This is',
print str(round(p_overduestart * 100, 1)) + '%',
print 'of actions which are due to start.'
print 'Excluding those started before the business plans were refreshed, this percentage is',
print str(round(p_netoverduestart * 100, 1)) + '%.'
print 'On average, they are overdue by',
print int(m_daysoverduestart),
print 'days.'
print

print 'Total number of actions whose completion is overdue:',
print n_overdueend
print 'This is',
print str(round(p_overdueend * 100, 1)) + '%',
print 'of actions which are due to end.'
print 'On average, they are overdue by',
print int(round(m_daysoverdueend, 0)),
print 'days.'
print

print 'Total number of actions which started late:',
print n_latestart
print 'This is',
print str(round(p_latestart * 100, 1)) + '% of all started actions.'
print 'On average, they were late by',
print int(round(m_dayslatestart, 0)),
print 'days.'
print

print 'Total number of actions which were completed late:',
print n_lateend
print 'This is',
print str(round(p_lateend * 100, 1)) + '% of all completed actions.'
print 'On average, they were late by',
print int(round(m_dayslateend, 0)),
print 'days.'
print

print 'Number of actions not due to start:',
print int(round(n_notduestart, 0))
print 'Number of actions not due to end:',
print int(round(n_notdueend, 0))
print

print 'Accumulated late start days:',
print int(round(t_dayslatestart, 0)),
print 'days.'
print 'Accumulated late end days:',
print int(round(t_dayslateend, 0)),
print 'days.'
print

print 'Accumulated overdue start days:',
print int(round(t_daysoverduestart, 0)),
print 'days.'
print 'Accumulated overdue end days:',
print int(round(t_daysoverdueend, 0)),
print 'days.'
print

# prepare for writing report data to CSV

reportfile_all = '../output/reports/report_snapshots_all.csv'
reportfile_dept = '../output/reports/report_snapshots_dept.csv'

reportfile_status_all = '../output/reports/report_statusmatrix_all.csv'
reportfile_status_dept = '../output/reports/report_statusmatrix_dept.csv'

deptfilenotexists = False
try:
    with open(reportfile_dept) as f: pass
except IOError as e:
    deptfilenotexists = True

allfilenotexists = False
try:
    with open(reportfile_all) as f: pass
except IOError as e:
    allfilenotexists = True

allstatusfilenotexists = False
try:
    with open(reportfile_status_all) as f: pass
except IOError as e:
    allstatusfilenotexists = True

deptstatusfilenotexists = False
try:
    with open(reportfile_status_dept) as f: pass
except IOError as e:
    deptstatusfilenotexists = True

report_snapshot_all = open(reportfile_all, 'ab')
report_snapshot_dept = open(reportfile_dept, 'ab')

report_status_all = open(reportfile_status_all, 'ab')
report_status_dept = open(reportfile_status_dept, 'ab')

writer_all = csv.writer(report_snapshot_all, csv.QUOTE_ALL)
writer_dept = csv.writer(report_snapshot_dept, csv.QUOTE_ALL)

writer_matrix = csv.writer(report_status_all, csv.QUOTE_ALL)
writer_deptmatrix = csv.writer(report_status_dept, csv.QUOTE_ALL)


statusheader_dept = ['Date', 'Time', 'Dept', 'Start Status', 'End Status', 'Count', 'StartConcern', 'EndConcern', 'TotalConcern']

if deptstatusfilenotexists:
    writer_deptmatrix.writerow(statusheader_dept)

# build line for overall report

report_line_all0 = [datestring, datetimestring, \
                   n_actions, n_started, n_netstarted, n_ended, n_ongoing, n_carriedoverstart, \
                   n_duetostartthismonth, n_duetoendthismonth, n_duetostartwithin30days, n_duetoendwithin30days, \
                   n_startedthismonth, n_endedthismonth, n_startedinlast30days, n_endedinlast30days, \
                   p_startedofthoseduetostart, p_netstartedofthoseduetostart, p_ended, p_ongoing, \
                   n_earlystart, n_earlyend, p_earlystart, p_earlyend, n_latestart, n_lateend, \
                   n_overduestart, n_overdueend, \
                   p_latestart, p_lateend, p_overduestart, p_overdueend, p_netoverduestart, \
                   m_daysearlystart, m_daysearlyend, m_dayslatestart, m_dayslateend, \
                   m_daysoverduestart, m_daysoverdueend, \
                   t_dayslatestart, t_dayslateend, t_daysoverduestart, t_daysoverdueend]

# round numbers

report_line_all = []
for i in report_line_all0:
    if ((type(i) is float) & (i <= 1)):
        i2 = round(i, 4)
    else:
        i2 = i
    report_line_all.append(i2)

# build header for overall report

report_header_all = ['datestring', 'datetimestring', \
                   'n_actions', 'n_started', 'n_netstarted', 'n_ended', 'n_ongoing', 'n_carriedoverstart', \
                   'n_duetostartthismonth', 'n_duetoendthismonth', 'n_duetostartwithin30days', 'n_duetoendwithin30days', \
                   'n_startedthismonth', 'n_endedthismonth', 'n_startedinlast30days', 'n_endedinlast30days', \
                   'p_startedofthoseduetostart', 'p_netstartedofthoseduetostart', 'p_ended', 'p_ongoing', \
                   'n_earlystart', 'n_earlyend', 'p_earlystart', 'p_earlyend', 'n_latestart', 'n_lateend', \
                   'n_overduestart', 'n_overdueend', \
                   'p_latestart', 'p_lateend', 'p_overduestart', 'p_overdueend', 'p_netoverduestart', \
                   'm_daysearlystart', 'm_daysearlyend', 'm_dayslatestart', 'm_dayslateend', \
                   'm_daysoverduestart', 'm_daysoverdueend', \
                   't_dayslatestart', 't_dayslateend', 't_daysoverduestart', 't_daysoverdueend']

# write header if file was just created

if allfilenotexists:
    writer_all.writerow(report_header_all)



# write data

writer_all.writerow(report_line_all)

# build header for departmental report

report_header_dept = ['date', 'time', \
                        'dept_id', 'dept_abbrev', 'dept_name', \
                        'n_actions', 'n_started', 'n_netstarted', 'n_ended', 'n_ongoing', 'n_carriedoverstart', \
                        'n_duetostartthismonth', 'n_duetoendthismonth', 'n_duetostartwithin30days', 'n_duetoendwithin30days', \
                        'n_startedthismonth', 'n_endedthismonth', 'n_startedinlast30days', 'n_endedinlast30days', \
                        'p_startedofthoseduetostart', 'p_netstartedofthoseduetostart', 'p_endedofthoseduetoend', 'p_ended', 'p_ongoing', \
                        'n_earlystart', 'n_earlyend', 'p_earlystart', 'p_earlyend', 'n_latestart', 'n_lateend', \
                        'n_overduestart', 'n_overdueend', \
                        'p_latestart', 'p_lateend', 'p_overduestart', 'p_overdueend', 'p_netoverduestart', \
                        'm_daysearlystart', 'm_daysearlyend', 'm_dayslatestart', 'm_dayslateend', \
                        'm_daysoverduestart', 'm_daysoverdueend', \
                        't_dayslatestart', 't_dayslateend', 't_daysoverduestart', 't_daysoverdueend']

# TODO: create and write codebook

# write departments header if file was just created

if deptfilenotexists:
    writer_dept.writerow(report_header_dept)

### CREATING MATRIX OF CODES AND COUNTS WITHIN THEM

statusheader_all = ['Date', 'Time', 'Start Status', 'End Status', 'Count', 'StartConcern', 'EndConcern', 'TotalConcern']

if allstatusfilenotexists:
    writer_matrix.writerow(statusheader_all)

for startcode in startcodesset:
    for endcode in endcodesset:
        countincell = 0
        startconcern = 0
        endconcern = 0
        totalconcern = 0
        if startcode == 'Late':
            startconcern = 1
        elif startcode == 'Overdue':
            startconcern = 2
        if endcode == 'Late':
            endconcern = 3
        elif endcode == 'Overdue':
            endconcern = 4
        totalconcern = startconcern + endconcern
        for line in alldata:
            if ((line[29] == startcode) & (line[30] == endcode)):
                countincell += 1
        matrixrow = [datestring, datetimestring, startcode, endcode, countincell, startconcern, endconcern, totalconcern]
        writer_matrix.writerow(matrixrow)


#===============================================================================
# #===============================================================================
# #  ADVANCED ANALYTICS 2: DEPARTMENTAL SUMMARIES
# #===============================================================================
#===============================================================================

# build iterable list of departments

deptcodeslist = []
# create a list of start in all lines
for line in alldata:
    deptcodeslist.append(line[2])
    # create set

# make a set of them - only one of each
deptcodesset = set(deptcodeslist)

# summary by department, iterating over original department call to make things match

for dept in deptcodesset:

    d_alldata = []
    for line in alldata:
        if line[2] == dept:
            d_alldata.append(line)

    dept_abbrev = d_alldata[0][0]

    dn_actions = float(len(d_alldata))
    dn_started = float(0)
    dn_ended = float(0)
    dn_duetostartthismonth = float(0)
    dn_duetoendthismonth = float(0)
    dn_duetostartwithin30days = float(0)
    dn_duetoendwithin30days = float(0)
    dn_startedthismonth = float(0)
    dn_endedthismonth = float(0)
    dn_startedinlast30days = float(0)
    dn_endedinlast30days = float(0)

    dn_notduestart = 0
    dn_carriedoverstart = 0

    d_earlystartlist = []
    d_latestartlist = []
    d_overduestartlist = []

    d_earlyendlist = []
    d_lateendlist = []
    d_overdueendlist = []

    # look at start status codes
    d_startcodeslist = []
    # create a list of start in all lines
    for line in d_alldata:
        d_startcodeslist.append(line[29])
        # create set

    # make a set of them - only one of each
    d_startcodesset = set(d_startcodeslist)

    # create empty dictionary
    d_startcodesdict = dict()

    # create dictionary keys and assign 0 as value to each
    for code in d_startcodesset:
        d_startcodesdict[code] = 0

    # raise value of each key for each line with a code equal to the key
    for code in d_startcodesdict:
        for line in d_alldata:
            if line[29] == code:
                d_startcodesdict[code] += 1

    # now run through end codes - documented above
    d_endcodeslist = []
    for line in d_alldata:
        d_endcodeslist.append(line[30])

    d_endcodesset = set(d_endcodeslist)

    d_endcodesdict = dict()

    for code in d_endcodesset:
        d_endcodesdict[code] = 0

    for code in d_endcodesdict:
        for line in d_alldata:
            if line[30] == code:
                d_endcodesdict[code] += 1

    for line in d_alldata:
        if int(line[27]) == 1:
            dn_started += 1
        if int(line[28]) == 1:
            dn_ended += 1
        # FIXME: all these generate 0
        if line[37] == 1:
            dn_duetostartthismonth += 1
        if line[38] == 1:
            dn_duetoendthismonth += 1
        if line[39] == 1:
            dn_duetostartwithin30days += 1
        if line[40] == 1:
            dn_duetoendwithin30days += 1
        if line[41] == 1:
            dn_startedthismonth += 1
        if line[42] == 1:
            dn_endedthismonth += 1
        if line[43] == 1:
            dn_startedinlast30days += 1
        if line[44] == 1:
            dn_endedinlast30days += 1

        if ((line[30] == 'Early') & (line[34] != 'NA')):
            d_earlyendlist.append(float(line[34]))

        if ((line[30] == 'Late') & (line[35] != 'NA')):
            d_lateendlist.append(float(line[35]))

        if ((line[30] == 'Overdue') & (line[36] != 'NA')):
            d_overdueendlist.append(float(line[36]))

        if (line[29] == 'Not due'):
            dn_notduestart += 1

        if (line[29] == 'Carried over'):
            dn_carriedoverstart += 1

        if ((line[29] == 'Early') & (line[31] != 'NA')):
            d_earlystartlist.append(float(line[31]))

        if ((line[29] == 'Late') & (line[32] != 'NA')):
            d_latestartlist.append(float(line[32]))

        if ((line[29] == 'Overdue') & (line[33] != 'NA')):
            d_overduestartlist.append(float(line[33]))

    # amount/average of late/early/overdue starts

    try:
        dm_daysearlystart = sum(d_earlystartlist) / len(d_earlystartlist)
    except ZeroDivisionError:
        dm_daysearlystart = 'NA'

    try:
        dm_dayslatestart = sum(d_latestartlist) / len(d_latestartlist)
    except ZeroDivisionError:
        dm_dayslatestart = 'NA'

    try:
        dm_daysoverduestart = sum(d_overduestartlist) / len(d_overduestartlist)
    except ZeroDivisionError:
        dm_daysoverduestart = 'NA'

    # amount/average of late/early/overdue ends

    try:
        dm_daysearlyend = sum(d_earlyendlist) / len(d_earlyendlist)
    except ZeroDivisionError:
        dm_daysearlyend = 'NA'

    try:
        dm_dayslateend = sum(d_lateendlist) / len(d_lateendlist)
    except ZeroDivisionError:
        dm_dayslateend = 'NA'

    try:
        dm_daysoverdueend = sum(d_overdueendlist) / len(d_overdueendlist)
    except ZeroDivisionError:
        dm_daysoverdueend = 'NA'

    dn_notdueend = 0
    for line in d_alldata:
        if (line[30] == 'Not due'):
            dn_notdueend += 1

    dn_earlystart = len(d_earlystartlist)
    dn_earlyend = len(d_earlyendlist)

    dn_overduestart = len(d_overduestartlist)
    dn_overdueend = len(d_overdueendlist)
    
    #TODO: start/end on time
    
    dn_netstarted = dn_started - dn_carriedoverstart

    dn_latestart = len(d_latestartlist)
    dn_lateend = len(d_lateendlist)

    dt_daysoverduestart = sum(d_overduestartlist)
    dt_daysoverdueend = sum(d_overdueendlist)

    dt_dayslatestart = sum(d_latestartlist)
    dt_dayslateend = sum(d_lateendlist)

    m_earlystart = float(dn_earlystart) / float(dn_started)
    try:
        dp_earlyend = float(dn_earlyend) / float(dn_ended)
    except ZeroDivisionError:
        dp_earlyend = 'NA'

    try:
        dp_earlystart = float(dn_earlystart) / float(dn_started)
    except ZeroDivisionError:
        dp_earlystart = 'NA'

    dp_latestart = float(dn_latestart) / float(dn_started)
    try:
        dp_lateend = float(dn_lateend) / float(dn_ended)
    except ZeroDivisionError:
        dp_lateend = 'NA'

    dp_overduestart = float(dn_overduestart) / (float(dn_started) + float(dn_overduestart))
    try:
        dp_netoverduestart = float(dn_overduestart) / (float(dn_started) + float(dn_overduestart) - float(dn_carriedoverstart))
    except ZeroDivisionError:
        dp_netoverduestart = 'NA'
    try:
        dp_overdueend = float(dn_overdueend) / (float(dn_ended) + float(dn_overdueend))
    except ZeroDivisionError:
        dp_overdueend = 'NA'
        
    # TODO: add aggregate durations (scheduled, so far, completed)

    # TODO: calculate late/overdue start/end as percentage of duration

    # calculated and percentage indicators

    dn_ongoing = (float(dn_started) - float(dn_ended))
    dp_ended = (float(dn_ended) / float(dn_actions))
    dp_started = (float(dn_started) / float(dn_actions))
    dp_ongoing = (float(dn_ongoing) / float(dn_actions))
    dp_startedofthoseduetostart = (float((dn_started)) / (float(dn_started) + float(dn_overduestart)))
    try:
        dp_netstartedofthoseduetostart = (float((dn_started) - float(dn_carriedoverstart)) / (float(dn_started) + float(dn_overduestart) - float(dn_carriedoverstart)))
    except ZeroDivisionError:
        dp_netstartedofthoseduetostart = 'NA'
    try:
        dp_endedofthoseduetoend = (float((dn_ended)) / (float(dn_ended) + float(dn_overdueend)))
    except ZeroDivisionError:
        dp_endedofthoseduetoend = 'NA'

    # print a basic summary

    print "SUMMARY OF PROGRESS ON ALL ACTIONS FOR DEPARTMENT " + line[1]
    print
    print 'Total actions in business plans: ' + str(int(dn_actions))
    print 'Number started: ' + str(int(dn_started))
    print 'Number started, excluding those carried over from last business plans: ' + str(int(dn_started) - int(dn_carriedoverstart))
    print 'Total carried over: ' + str(int(dn_carriedoverstart))
    print
    print 'Number completed: ' + str(int(dn_ended))
    print 'Percent completed of total: ' + str(round(dp_ended * 100, 2)) + '%'
    print
    print 'Percent started of total: ' + str(round(dp_started * 100, 2)) + '%'
    print 'Percent started of those due to start: ' + str(round(dp_startedofthoseduetostart * 100, 2)) + '%'
    if dp_netstartedofthoseduetostart != 'NA':
        print 'Percent started of those due to start, excluding those carried over from previous business plans: ' + str(round(dp_netstartedofthoseduetostart * 100, 2)) + '%'
    else:
        print 'Percent started of those due to start, excluding those carried over from previous business plans: ' + dp_netstartedofthoseduetostart + '%'
    print
    if dp_endedofthoseduetoend != 'NA':
        print 'Percent completed of those due to complete: ' + str(round(dp_endedofthoseduetoend * 100, 2)) + '%'
    else:
        print 'Percent completed of those due to complete: ' + dp_endedofthoseduetoend + '%'
    print 'Percent ongoing: ' + str(round(dp_ongoing * 100, 2)) + '%'
    print

    print 'Total number of actions which are overdue to start:',
    print dn_overduestart
    print 'This is',
    print str(round(dp_overduestart * 100, 1)) + '%',
    print 'of actions which are due to start.'
    print 'Excluding those started before the business plans were refreshed, this percentage is',
    if dp_netoverduestart != 'NA':
        print str(round(dp_netoverduestart * 100, 1)) + '%.'
    else:
        print dp_netoverduestart + '%.'
    print 'On average, they are overdue by',
    print dm_daysoverduestart,
    print 'days.'
    print

    print 'Total number of actions whose completion is overdue:',
    print dn_overdueend
    print 'This is',
    if dp_overdueend != 'NA':
        print str(round(dp_overdueend * 100, 1)) + '%',
    else:
        print dp_overdueend + '%',

    print 'of actions which are due to end.'
    print 'On average, they are overdue by',
    print dm_daysoverdueend,
    print 'days.'
    print

    print 'Total number of actions which started late:',
    print dn_latestart
    print 'This is',
    print str(round(dp_latestart * 100, 1)) + '% of all started actions.'
    print 'On average, they were late by',
    print dm_dayslatestart,
    print 'days.'
    print

    print 'Total number of actions which were completed late:',
    print dn_lateend
    print 'This is',
    if dp_lateend != 'NA':
        print str(round(dp_lateend * 100, 1)) + '% of all completed actions.'
    else:
        print dp_lateend + '% of all completed actions.'
    print 'On average, they were late by',
    print dm_dayslateend,
    print 'days.'
    print

    print 'Number of actions not due to start:',
    print int(round(dn_notduestart, 0))
    print 'Number of actions not due to end:',
    print int(round(dn_notdueend, 0))
    print

    print 'Accumulated late start days:',
    print int(round(dt_dayslatestart, 0)),
    print 'days.'
    print 'Accumulated late end days:',
    print int(round(dt_dayslateend, 0)),
    print 'days.'
    print

    print 'Accumulated overdue start days:',
    print int(round(dt_daysoverduestart, 0)),
    print 'days.'
    print 'Accumulated overdue end days:',
    print int(round(dt_daysoverdueend, 0)),
    print 'days.'
    print

    # build line for overall report

    report_line_dept0 = [datestring, datetimestring, \
                        line[2], line[0], line[1], \
                        dn_actions, dn_started, dn_netstarted, dn_ended, dn_ongoing, dn_carriedoverstart, \
                        dn_duetostartthismonth, dn_duetoendthismonth, dn_duetostartwithin30days, dn_duetoendwithin30days, \
                        dn_startedthismonth, dn_endedthismonth, dn_startedinlast30days, dn_endedinlast30days, \
                        dp_startedofthoseduetostart, dp_netstartedofthoseduetostart, dp_endedofthoseduetoend, dp_ended, dp_ongoing, \
                        dn_earlystart, dn_earlyend, dp_earlystart, dp_earlyend, dn_latestart, dn_lateend, \
                        dn_overduestart, dn_overdueend, \
                        dp_latestart, dp_lateend, dp_overduestart, dp_overdueend, dp_netoverduestart, \
                        dm_daysearlystart, dm_daysearlyend, dm_dayslatestart, dm_dayslateend, \
                        dm_daysoverduestart, dm_daysoverdueend, \
                        dt_dayslatestart, dt_dayslateend, dt_daysoverduestart, dt_daysoverdueend]

    # round numbers

    report_line_dept = []
    for i in report_line_dept0:
        if ((type(i) is float) & (i <= 1)):
            i2 = round(i, 4)
        else:
            i2 = i
        report_line_dept.append(i2)



    # write data

    writer_dept.writerow(report_line_dept)

    # generate counts in matrix of start and end codes

    for startcode in startcodesset:
        for endcode in endcodesset:
            dcountincell = 0
            startconcern = 0
            endconcern = 0
            totalconcern = 0
            if startcode == 'Late':
                startconcern = 1
            if startcode == 'Overdue':
                startconcern = 2
            if endcode == 'Late':
                endconcern = 3
            if endcode == 'Overdue':
                endconcern = 4
            totalconcern = startconcern + endconcern
            for line in d_alldata:
                if ((line[29] == startcode) & (line[30] == endcode)):
                    dcountincell += 1
                    dcountincell += 1
            dmatrixrow = [datestring, datetimestring, dept_abbrev, startcode, endcode, dcountincell, startconcern, endconcern, totalconcern]
            writer_deptmatrix.writerow(dmatrixrow)

# TODO: add per-priority table, same as with departments
# TODO: list of overdue/late actions: dept, id, name, priority, action group, start schedule, end schedule, act start, act end, status, explanation \
# make it write to one file so it's traceable over time \
# leave blank columns for manual assessment of the quality of the explanation