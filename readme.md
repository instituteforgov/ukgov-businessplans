Readme: UK Government Business Plan data retrieval & analytics
====================

This package consists of

1. a script that collects data from the UK government's Business Plans API and makes basic calculations, e.g. on overdue and missed actions

2. a script that takes the resulting data and produces overall and departmental analytics reports

Data Sources
-----------
 
 * API base URL: http://transparency.number10.gov.uk/api/
 * API documentation: http://transparency.number10.gov.uk/developers
 * Number 10 front end: http://transparency.number10.gov.uk/
 
Process
------------

Outputs
----------- 
1.

2.

3.

4.

Todo
------

### Critical fixes
* counting of this/last/next month actions in analytics - now returns all 0s

### Nice to have fixes
* more robust date parsing via dateparse
* change overdue/late counting to months

### Improvements
* separate reports at action level
* link resolution of department names with OKFN's Nomenklatura API
* lists of overdue and late actions with explanations
* MAJOR: reformulate for use on scraperwiki