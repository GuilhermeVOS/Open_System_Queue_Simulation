library(ggplot2)

F1 = read.csv("Stats_ServidorFixo20000jobs.csv")
F2 = read.csv("Stats_ServidorFixo100000jobs.csv")
F3 = read.csv("Stats_ServidorFixo1000000jobs.csv")
F4 = read.csv("Stats_ServidorUniforme20000jobs.csv")
F5 = read.csv("Stats_ServidorUniforme100000jobs.csv")
F6 = read.csv("Stats_ServidorExponencial20000jobs.csv")
F7 = read.csv("Stats_ServidorExponencial100000jobs.csv")

F1 = F1[10000:20001,]
F2 = F2[50000:100001,]
F3 = F3[500000:1000001,]
F4 = F4[10000:20001,]
F5 = F5[50000:100001,]
F6 = F6[10000:20001,]
F7 = F7[50000:100000,]

m1 = mean(F1$Tempo_Total_Sistema)
m2 = mean(F2$Tempo_Total_Sistema)
m3 = mean(F3$Tempo_Total_Sistema)
m4 = mean(F4$Tempo_Total_Sistema)
m5 = mean(F5$Tempo_Total_Sistema)
m6 = mean(F6$Tempo_Total_Sistema)
m7 = mean(F7$Tempo_Total_Sistema)

sd1 = sd(F1$Tempo_Total_Sistema)
sd2 = sd(F2$Tempo_Total_Sistema)
sd3 = sd(F3$Tempo_Total_Sistema)
sd4 = sd(F4$Tempo_Total_Sistema)
sd5 = sd(F5$Tempo_Total_Sistema)
sd6 = sd(F6$Tempo_Total_Sistema)
sd7 = sd(F7$Tempo_Total_Sistema)

metricas = data.frame(Media = c(m1, m2, m3, m4, m5, m6, m7), DesvioPadrao = c(sd1,sd2,sd3,sd4,sd5,sd6,sd7))
rownames(metricas) = c("Fixo 20k","Fixo 100k","Fixo 1m","Uniforme 20k","Uniforme 100k","Exp 20k","Exp 100k")

plottable <- as.data.frame(metricas)

library(gridExtra)
png("test.png", height = 50*nrow(plottable), width = 200*ncol(plottable))
grid.table(plottable)
dev.off()
