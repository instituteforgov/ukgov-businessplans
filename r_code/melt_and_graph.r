require(reshape)
# need to also get rid of id var so it won't iterate over it
molten <- melt(report_snapshots_dept)

dev.new()
ggplot() +
	geom_bar(aes(y = value,x = dept_abbrev,fill = variable),data=molten) +
	facet_grid(facets = variable ~ ., scales = 'free') +
	opts(plot.background = theme_blank(),axis.line = theme_blank(),axis.ticks = theme_blank(),axis.title.x = theme_blank(),axis.text.x = theme_text(),axis.title.y = theme_blank(),axis.text.y = theme_text(),legend.background = theme_blank(),legend.position = 'right',
legend.direction = 'vertical',panel.background = theme_blank(),strip.background = theme_blank(),strip.text.x = theme_blank(),strip.text.y = theme_blank()) +
	scale_fill_brewer(guide = guide_legend(),name = 'Legend',breaks = c("1","2","3","4","5","6","7"),labels = c("Blaf","Blaf","Blaf","Blaf","Blaf","Blaf","Blaf"),palette = 'Paired')

