'''
Created on Jul 15, 2012

@author: petrbouchal
'''

from datetime import datetime
import calendar
import csv

now = datetime.now()
today = datetime.today()
alldata = []

# setup dummy dates
fakejson = []
fakejsonrow1 = ['May 2012', 'June 2012', '2012-06-12 00:00:00', '2012-07-06 00:00:00', '1', 'Ministry of Justice']
#started and ended on time
fakejson.append(fakejsonrow1)

fakejsonrow2 = ['Started', 'June 2012', '', '2012-06-21 00:00:00', '2', 'Ministry of Justice']
# started who knows when, ended on time.
fakejson.append(fakejsonrow2)

fakejsonrow3 = ['Oct 2012', 'Jan 2013', '', '', '3', 'Ministry of Defence']
# start not due
fakejson.append(fakejsonrow3)

fakejsonrow4 = ['Started', 'Feb 2013', '', '', '4', 'Department for Energy and Climate Change']
# started who knows when, not due
fakejson.append(fakejsonrow4)

fakejsonrow5 = ['May 2012', 'Jan 2014', '2012-04-15 00:00:00', '', '5', 'Home Office']
# started on time, end not due
fakejson.append(fakejsonrow5)

fakejsonrow6 = ['June 2012', 'Feb 2015', '2012-07-15 00:00:00', '', '6', 'Cabinet Office']
# started late, end not due
fakejson.append(fakejsonrow6)

fakejsonrow7 = ['May 2012', 'Jun 2015', '', '', '7', 'Cabinet Office']
# started late, end not due
fakejson.append(fakejsonrow7)

fakejsonrow8 = ['May 2012', 'Jun 2012', '', '', '8', 'Department for Communities and Local Government']
# start overdue, end overdue
fakejson.append(fakejsonrow8)

# setup structure for assigning abbreviations to department names
deptdict = {}
deptdict['Department for Communities and Local Government'] = 'DCLG'
deptdict['Ministry of Justice'] = 'MoJ'
deptdict['Ministry of Defence'] = 'MoD'
deptdict['Cabinet Office'] = 'CO'
deptdict['Department for Energy and Climate Change'] = 'DECC'
deptdict['Home Office'] = 'HO'

for call in fakejson:
    # assign abbreviations:
    deptabbrev = deptdict[call[5]]
#    print deptabbrev

    # create emulated data
    subaction_schedule_start_date = call[0]
    subaction_schedule_end_date = call[1]
    subaction_actual_start_date = call[2]
    subaction_actual_end_date = call[3]

    # process scheduled dates
    sched_start_text = 0
    sched_end_text = 0
    try:
        # trying if the date is in Apr 13 type format ...
        #
        # NOTE dates whose name end in 0 are date objects, other date variables are strings
        #
        sched_end0 = datetime.strptime(subaction_schedule_end_date, '%b %Y')
        sched_end = datetime.strftime(sched_end0, '%Y-%m-%d')
    except ValueError:
        # ... or in April 14 format.
        try:
            sched_end0 = datetime.strptime(subaction_schedule_end_date, '%B %Y')
            sched_end = datetime.strftime(sched_end0, '%Y-%m-%d')
        except ValueError:
            sched_end = 'NA'
            sched_end_text = 1
    try:
    # same for start date - turn into real data and format correctly
        sched_start0 = datetime.strptime(subaction_schedule_start_date, '%b %Y')
        sched_start = datetime.strftime(sched_start0, '%Y-%m-%d')
    except ValueError:
        try:
            sched_start0 = datetime.strptime(subaction_schedule_start_date, '%B %Y')
            sched_start = datetime.strftime(sched_start0, '%Y-%m-%d')
        except ValueError:
            sched_start = 'NA'
            sched_start_text = 1

    if sched_start_text != 1:
        sched_start_day = sched_start0.day
        sched_start_month = sched_start0.month
        sched_start_year = sched_start0.year
        sched_start_numberofdays = int(calendar.monthrange(sched_start_year, int(sched_start_month))[1])
        sched_start_endmonth0 = sched_start0.replace(day=sched_start_numberofdays)
        sched_start_endmonth = datetime.strftime(sched_start_endmonth0, '%Y-%m-%d')
    else:
        sched_start_endmonth = 'NA'

    if sched_end_text != 1:
        sched_end_day = sched_end0.day
        sched_end_month = sched_end0.month
        sched_end_year = sched_end0.year
        sched_end_numberofdays = int(calendar.monthrange(sched_end_year, int(sched_end_month))[1])
        sched_end_endmonth0 = sched_end0.replace(day=sched_end_numberofdays)
        sched_end_endmonth = datetime.strftime(sched_end_endmonth0, '%Y-%m-%d')
    else:
        sched_end_new = 'NA'

    # process actual dates - turn into real dates and get rid of time
    try:
        act_start0 = datetime.strptime(subaction_actual_start_date, '%Y-%m-%d %H:%M:%S')
        act_start = datetime.strftime(act_start0, '%Y-%m-%d')
    except TypeError:
        act_start = 'NA'
        act_start_text = 1
    except ValueError:
        act_start = 'NA'
        act_start_text = 1

    try:
        act_end0 = datetime.strptime(subaction_actual_end_date, '%Y-%m-%d %H:%M:%S')
        act_end = datetime.strftime(act_end0, '%Y-%m-%d')
    except ValueError:
        act_end = 'NA'
        act_end_text = 1
    except TypeError:
        act_end = 'NA'
        act_end_text = 1

    # print results
    print
    print 'Case: ' + str(call[4])
#    print call

    print 'Final edited scheduled start ' + str(sched_start)
    print 'Final edited scheduled end ' + str(sched_end)
    print 'Final edited scheduled start, end of month ' + str(sched_start_endmonth)
    print 'Final edited scheduled end, end of month ' + str(sched_end_endmonth)
    print 'Actual start date: ' + str(act_start)
    print 'Actual end date: ' + str(act_end)


    #===============================================================================
    # BASIC ANALYTICS: MARK EACH ITEM WITH STATUS CODES
    #===============================================================================

    duetostart = ((sched_start_endmonth0 < today) | (subaction_schedule_start_date == 'Started'))
#    print 'Due to start: ' + str(duetostart)

    duetocomplete = sched_end_endmonth0 < today
#    print 'Due to complete: ' + str(duetocomplete)

    started = False
    if(subaction_schedule_start_date == 'Started') | (act_start != 'NA'):
        started = True
#    print 'Started: ' + str(started)

    completed = False
    if(act_end != 'NA'):
        completed = True
#    print 'Completed: ' + str(completed)

    # condition so startedontime is empty if duetostart is false 
    if duetostart & started:
        startedontime = ((act_start0 < sched_start_endmonth0) | (subaction_schedule_start_date == 'Started'))
    else:
        startedontime = 'NA'
#    print 'Started on time: ' + str(startedontime)

    if duetocomplete & completed:
        completedontime = act_end0 <= sched_end_endmonth0
    else:
        completedontime = 'NA'
#    print 'Completed on time: ' + str(completedontime)

    overduestart = (started == False) & (duetostart == True)
#    print 'Overdue start: ' + str(overduestart)
    # this measure disregards the fact that some are not due to start, marking them as false for overdue

    overdueend = (completed == False) & (duetocomplete == True)
#    print 'Overdue end: ' + str(overdueend)
    # this measure disregards the fact that some are not due to end, marking them as false for overdue    

    if duetostart == False:
        duetostartthismonth = (sched_start_endmonth0.month == today.month)
        duetostartwithin30days = (sched_start_endmonth0 < today.replace(month=today.month + 1))

    else:
        duetostartthismonth = 'NA'
        duetostartwithin30days = 'NA'

    print 'Due to start this month: ' + str(duetostartthismonth)
    print 'Due to start within 30 days: ' + str(duetostartwithin30days)

    if duetocomplete == False:
        duetoendthismonth = (sched_end_endmonth0.month == today.month)
        duetoendwithin30days = (sched_end_endmonth0 < today.replace(month=today.month + 1))
    else:
        duetoendthismonth = 'NA'
        duetoendwithin30days = 'NA'

    print 'Due to end this month: ' + str(duetoendthismonth)
    print 'Due to end within 30 days: ' + str(duetoendwithin30days)


    outputline = [sched_start, sched_end, sched_start_endmonth, sched_end_endmonth, act_start, act_end, call[4], \
                  deptabbrev, started, completed, startedontime, completedontime, duetostart, duetocomplete, \
                  overduestart, overdueend]
    alldata.append(outputline)
#print alldata

#===========================================================================
# ADVANCED ANALYTICS I: GETTING THE TOP-LEVEL AGGREGATE FIGURES
#===========================================================================
numberofactions = len(alldata)
numberstarted = 0
numbercompleted = 0
numberstartedontime = 0
numbercompletedontime = 0
numberoverdueend = 0
numberoverduestart = 0

for line in alldata:
    if line[8] == True:
        numberstarted += 1
    if line[9] == True:
        numbercompleted += 1
    if line[10] == True:
        numberstartedontime += 1
    if line[11] == True:
        numbercompletedontime += 1
    if line[14] == True:
        numberoverduestart += 1
    if line[15] == True:
        numberoverdueend += 1

print "SUMMARY"
print 'Total actions in business plans: ' + str(numberofactions)
print 'Number started: ' + str(numberstarted)
print 'Number completed: ' + str(numbercompleted)
print 'Number started on time: ' + str(numberstartedontime)
print 'Number completed on time: ' + str(numbercompletedontime)
print 'Number with start overdue: ' + str(numberoverduestart)
print 'Number with end overdue: ' + str(numberoverdueend)
print

# prepare for writing report data to CSV

reportfile_all = '../output/reports/anal_snapshot_all.csv'
reportfile_dept = '../output/reports/anal_snapshot_dept.csv'

report_snapshot_all = open(reportfile_all, 'ab')
report_snapshot_dept = open(reportfile_dept, 'ab')

writer_all = csv.writer(report_snapshot_all, csv.QUOTE_ALL)
writer_dept = csv.writer(report_snapshot_dept, csv.QUOTE_ALL)

# write overall data

# build date and time strings
datestring = datetime.strftime(today, '%Y-%m-%d')
datetimestring = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')

report_line_all = [datestring, datetimestring, numberofactions, numberstarted, numbercompleted, numberstartedontime, numbercompletedontime, \
                   numberoverduestart, numberoverdueend]

# build and write header for overall report
report_header_all = ['today', 'now', 'numberofactions', 'numberstarted', 'numbercompleted', 'numberstartedontime', 'numbercompletedontime', \
                   'numberoverduestart', 'numberoverdueend']
#writer_all.writerow(report_header_all)
writer_all.writerow(report_line_all)

# build and write header for departmental report
report_header_dept = ['dept', 'today', 'now', 'numberofactions', 'numberstarted', 'numbercompleted', 'numberstartedontime', 'numbercompletedontime', \
                   'numberoverduestart', 'numberoverdueend']
#writer_dept.writerow(report_header_dept)

# summary by department
listofdepts = ['MoJ', 'MoD', 'DECC', 'DCLG', 'HO', 'CO']
for dep in listofdepts:
    dnumberofactions = 0
    dnumberstarted = 0
    dnumbercompleted = 0
    dnumberstartedontime = 0
    dnumbercompletedontime = 0
    dnumberoverdueend = 0
    dnumberoverduestart = 0
    for line in alldata:
        if line[7] == dep:
            dnumberofactions += 1
            if line[8] == True:
                dnumberstarted += 1
            if line[9] == True:
                dnumbercompleted += 1
            if line[10] == True:
                dnumberstartedontime += 1
            if line[11] == True:
                dnumbercompletedontime += 1
            if line[14] == True:
                dnumberoverduestart += 1
            if line[15] == True:
                dnumberoverdueend += 1
    print "DEPARTMENTAL SUMMARY: " + dep
    print 'Total actions in business plans: ' + str(dnumberofactions)
    print 'Number started: ' + str(dnumberstarted)
    print 'Number completed: ' + str(dnumbercompleted)
    print 'Number started on time: ' + str(dnumberstartedontime)
    print 'Number completed on time: ' + str(dnumbercompletedontime)
    print 'Number with start overdue: ' + str(dnumberoverduestart)
    print 'Number with end overdue: ' + str(dnumberoverdueend)
    print

    # build report line for departmental report
    report_line_dept = [dep, datestring, datetimestring, numberofactions, numberstarted, numbercompleted, numberstartedontime, numbercompletedontime, \
                   numberoverduestart, numberoverdueend]

    # write line of departmental report
    writer_dept.writerow(report_line_dept)
