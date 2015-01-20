UK Government Business Plan data retrieval & analytics
====================

 The code in this repository collects and analyses data on the UK Government's progress against its own Structural Reform Plan actions. This was used in several [Whitehall Monitor](http://instituteforgoverment.org.uk/our-work/whitehall-monitor) bulletins and Whitehall Monitor 2013 and 2014 annual reports published by the [Institute for Government](http://instituteforgoverment.org.uk).

Latest data and analysis from the Institute for Government using this dataset: http://www.instituteforgovernment.org.uk/publication/measuring-performance 
 
Code by [@petrbouchal](http://github.com/petrbouchal).

This repository consists of

1. a script that collects data from the UK government's Business Plans API and makes basic calculations, e.g. on overdue and missed actions

2. a script that takes the resulting data and produces overall and departmental analytics reports

Currently, only the basic data collection and per-subaction analytics are done.

Where the data come from
-----------
 
 * API base URL: http://transparency.number10.gov.uk/api/
 * API documentation: http://transparency.number10.gov.uk/developers
 * Number 10 front end: http://transparency.number10.gov.uk/

The data comes in JSON format and is nested as follows:

```
Department
 Priority
  Action
   Subaction
```
Only subactions consistently have information attached to them on dates, comments, etc.
 
What it does
------------
It loops through departments, priorities, actions and subactions, then calculates time overdue etc. The key variable that it produces is `subaction_[start|end]_status`.

The code is [hosted on Morph](http://morph.io/petrbouchal/GovBusinessPlans). It is scheduled to run every day but programmed to only scrape & save data every week.

# Codebook:

Columns used for analysis in bold.

|  Column name | Description | Unprocessed data |
| --------------- | ------------ | -------- |
|  **dept_abb** | Department abbreviation | N
|  dept_name | Department name | Y
|  dept_id | Department ID in API | Y
|  dept_url | Department URL | Y
|  priority_body | Name of priority | Y
|  priority_id | Priority ID | Y
|  priority_strapline | Priority strapline. May contain pointless HTML | Y
|  action_id | Action ID | Y
|  action_body | Name of action | Y
|  action_notes | Notes on action | Y
|  schedule_start_date | Action scheduled start date. Ignore. | N
|  schedule_end_date | Action scheduled end date. Ignore. | N
|  actual_start_date | Action actual start date. Ignore. | N 
|  actual_end_date | Action actual end date. Ignore. | N
|  **subaction_id** | Subaction ID. | N
|  **subaction_body** | Name of subaction. | N
|  **subaction_notes** | Typically contains explanations of missed due dates etc. | N
|  **subaction_schedule_start_date** | Schedule start date for subaction. | N
|  **subaction_schedule_end_date** | Scheduled end date for subaction | N
|  act_start | Action actual start date. Ignore. | N
|  act_end | Action actual end date. Ignore. | N
|  **sched_start_endmonth** | Date at end of month in which subaction is due to start. Created to introduce some leeway into overdue calculations. | N
|  **sched_end_endmonth** | Date at end of month in which subaction is due to end. Created to introduce some leeway into overdue calculations. | N
|  started | Did subaction start? | N
|  ended | Did subaction end? | N
|  **start_status** | Start status of subaction. | N
|  **end_status** | End status of subaction. | N
|  startearlyby | How long ahead of schedule did subaction start? Treat with caution/ignore. | N
|  startedlateby | How long behind schedule did subaction start? Treat with caution/ignore. | N
|  startoverdueby | Treat with caution/ignore. | N
|  endearlyby | How long ahead of schedule did subaction end? Treat with caution/ignore. | N
|  endedlateby | How much overdue did subaction end? Treat with caution/ignore. | N
|  endedoverdueby | Treat with caution/ignore. | N
|  carriedover | If no start date, start date will be 'Carried over' and this column will=1 | N
|  subaction_schedule_start_orig | Unprocessed scheduled start date of subaction.  | Y
|  subaction_schedule_end_orig | Unprocessed scheduled end date of subaction. | Y
|  subaction_actual_start_orig | Unprocessed actual end date of subaction. | Y
|  subaction_actual_end_orig | Unprocessed actual end date of subaction. | Y
|  **datetime** | Date and time of data collection. Use this, not `date` - to get entries from one run of the scraper rather than whole day | N
|  date | Date of data collection. | N


How to get the data out
------

The data can be downloaded from [Morph](http://morph.io/petrbouchal/GovBusinessPlans) as CSV or SQLite in one piece or as a subset in JSON, XML or CSV via the Morph API, which requires writing a bit of SQL.

To get data out of Morph, you need to login using a Github account.

Caveats
------

This is a very suboptimally structured piece of code - but it works.

Ideally, it would not loop around every action, but first collect the data (with the option of saving it as a raw text file), then save it into a table, and then, optionally, do some analytics on the whole table at once, ideally saving into another table to preserve the distinction between data collection and data processing.
