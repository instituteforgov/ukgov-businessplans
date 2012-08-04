# create two datasets, one with actual and one with scheduled dates
bp2 <- bp
bp1 <- bp
bp2$measure = "actual"
bp$measure = "schedule"

bp2$enddate <- bp$end_actual
bp2$startdate <- bp$start_actual
bp2$dept_id2 <- bp$dept_id + .5

bp1$enddate <- bp$end_schedule
bp1$startdate <- bp$start_schedule
bp1$dept_id2 <- bp$dept_id + .5

bp_comp = rbind(bp1, bp2)

# create dataset with dept name linked to dept ID, for plotting
nameid <- ddply(bp, .(dept_name, dept_id), "nrow")
nameid$deptname <- nameid$dept_name
nameid$deptid <- nameid$dept_id
nameid$position <- as.Date("01/01/2012", format= '%d/%m/%Y')