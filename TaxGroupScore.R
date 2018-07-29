require("ggplot2")

args = commandArgs(TRUE)

infile = args[1]
#outfile_tripl = args[2]
outfile_quart = args[2]

d = read.table(infile,header=T)
d$level <- factor(d$level,levels = c("kingdom","phylum","class","order","family","genus","species","strain"))


#ggplot(d[!d$level %in% c("kingdom","strain"),],aes(x="",y=..count..)) + 
#  geom_bar(aes(fill=cut(tripl,c(0,0.95,1,1.001),right = F))) +
#  scale_fill_brewer(labels=c("<95","95..<100","Monophyletic"),palette = 3,name="Triplet score",direction = -1)+theme_classic()+
#  facet_wrap(~level,scales = "free",ncol=6) + 
#  theme(legend.position = "bottom")

#ggplot(d[!d$level %in% c("kingdom","strain"),],aes(x="",y=..count..)) + 
#  geom_bar(aes(fill=cut(tripl,c(0,0.5,0.9,0.95,1,1.001),right = F))) +
#  scale_fill_brewer(palette = "Reds",name="Triplet score",direction = -1)+theme_classic()+
#  facet_wrap(~level,scales = "free",ncol=6) + 
#  theme(legend.position = "bottom")

#ggsave(outfile_tripl)

ggplot(d[!d$level %in% c("kingdom","strain"),],aes(x="",y=..count..)) + 
  geom_bar(aes(fill=cut(quart,c(0,0.5,0.9,0.95,1,1.001),right = F))) +
  #geom_bar(aes(fill=cut(quart,c(0,0.95,1,1.001),right = F))) +
  scale_fill_brewer(palette = "Reds",name="Quartet score",direction = -1)+theme_classic()+
  #scale_fill_brewer(labels=c("<95","95..<100","Monophyletic"),palette = 3,name="Quartet Score",direction = -1)+theme_classic()+
  facet_wrap(~level,scales = "free",ncol=6) + theme(legend.position = "bottom")
ggsave(outfile_quart)
