getwd()
setwd("C:/Users/user/Desktop/Rpro")
busan<-read.csv("busan.csv",header = T)

library(dplyr)
library(Hmisc)
library(prettyR)
library(psych)
library(agricolae) 
library(corrplot)

#임금근로자 근로여건 만족도(문항7) 평균/ 숫자가 클수록 긍정으로 변환 / 결측치 제거후 w7_na에 저장
busan$w70<-(busan$w7_1+busan$w7_2+busan$w7_3+busan$w7_4+busan$w7_5)/5
busan$w7<-6-busan$w70          
busan$w7<-ifelse(busan$w7==0,NA,busan$w7)   
w7_na<-busan %>% filter(!is.na(w7))     
busan$w7

#정주의사(문항23) 클수록 긍정으로 변환
busan$opinion2<-6-busan$opinion
busan$opinion2


#삶에대한만족도
busan$s31<-(busan$s31_1+busan$s31_2)/2
busan$s31

#연령대
busan$age2[busan$age>=15 & busan$age<20] <- "10s"
busan$age2[busan$age>=20 & busan$age<30] <- "20s"
busan$age2[busan$age>=30 & busan$age<40] <- "30s"
busan$age2[busan$age>=40 & busan$age<50] <- "40s"
busan$age2[busan$age>=50 & busan$age<60] <- "50s"
busan$age2[busan$age>=60] <- "over 60s"

#w1(취업경쟁력요인)
busan$w1 <- ifelse(busan$w1==7 | busan$w1==8, NA, busan$w1)   #결측치==7,8

w1_na<-busan %>% filter(!is.na(w1))     #결측치 제거해서 저장
w1_na$w1
w1_na$gender
w1_na$opinion2

#w2(취업애로요인)
busan$w2 <- ifelse(busan$w2==9, NA, busan$w2) #결측치==9

w2_na<-busan %>% filter(!is.na(w2))     #결측치 제거해서 저장
w2_na$w2

#w4_0(직업선택요인)
busan$w4_0 <- ifelse(busan$w4_0==9 | busan$w4_0==10, NA, busan$w4_0) #결측치==9,10

w4_0_na<-busan %>% filter(!is.na(w4_0))     #결측치 제거해서 저장
w4_0_na$w4_0



##opinion3/w7/s31 상관관계#######################

w7_na$s31<-(w7_na$s31_1+w7_na$s31_2)/2
w7_na$opinion2<-6-w7_na$opinion
s31 <- w7_na$s31
opinion3 <- w7_na$opinion2
w7 <- w7_na$w7
w7;s31;opinion3

main_relation <- data.frame(s31,w7, opinion3)
main_relation
str(main_relation)

main_relation.cor <- cor(main_relation)
main_relation.cor
str(main_relation.cor)

cor.test(~ s31+w7,main_relation)
cor.test(~ s31+opinion3,main_relation)
cor.test(~ w7+opinion3,main_relation)

corrplot(main_relation.cor, method = "shade", addshade = "all",shade.col = FALSE, tl.col = "red",
         tl.srt = 30, diag = FALSE, addCoef.col = "white", order = "FPC") #약한/뚜렷한 양의 상관관계

#1-gender 성별에 따른 삶의만족도#############################
#s31
busan$gender;busan$s31
male <- subset(busan, gender==1)
male
female <- subset(busan, gender==2)
female
malecount <- length(male$gender)
femalecount <- length(female$gender)
malecount;femalecount

malemean <- round(mean(male$s31),2)
femalemean <- round(mean(female$s31),2)
malemean;femalemean
mfcount <- c(malecount,femalecount)
mfmean <- c(malemean,femalemean)
mftable <- data.frame(Freq=mfcount, Mean=mfmean)
mftable
var.test(male$s31, female$s31)
wilcox.test(male$s31, female$s31)

male$s31
female$s31

#성별에 따른 근로여건만족도
w7_na$gender;w7_na$w7
w7_male <-subset(w7_na, gender==1) 
w7_female <-subset(w7_na, gender==2) 
w7_male;w7_female
w7_malecount <- length(w7_male$gender)
w7_femalecount <- length(w7_female$gender)
w7_malecount;w7_femalecount

w7_malemean <- round(mean(w7_male$w7),2)
w7_femalemean <- round(mean(w7_female$w7),2)
w7_malemean;w7_femalemean
w7_mfcount <- c(w7_malecount,w7_femalecount)
w7_mfmean <- c(w7_malemean,w7_femalemean)
w7_mftable <- data.frame(Freq=w7_mfcount, Mean=w7_mfmean)
w7_mftable
var.test(w7_male$w7, w7_female$w7)
wilcox.test(w7_male$w7, w7_female$w7)

#성별에 따른 부산시정주의사

var.test(male$opinion2, female$opinion2)
wilcox.test(male$opinion2, female$opinion2)

#2-age2 anova############################


#연령대별 삶의만족도
busan$age2;busan$s31
tapply(busan$s31, busan$age2, nortest::ad.test)
bartlett.test(busan$s31, busan$age2, data=busan)

as.ano <- oneway.test(s31~age2, busan, var.equal=F)
as.ano
as.model <- aov(s31~age2, busan)
as.comparison <- LSD.test(as.model, "age2", p.adj = "bonferroni", group = T)
as.comparison

#연령대별 근로여건만족도
w7_na$age2[w7_na$age>=15 & w7_na$age<20] <- "10s"
w7_na$age2[w7_na$age>=20 & w7_na$age<30] <- "20s"
w7_na$age2[w7_na$age>=30 & w7_na$age<40] <- "30s"
w7_na$age2[w7_na$age>=40 & w7_na$age<50] <- "40s"
w7_na$age2[w7_na$age>=50 & w7_na$age<60] <- "50s"
w7_na$age2[w7_na$age>=60] <- "over 60s"

w7_na$age2;w7_na$w7
tapply(w7_na$w7, w7_na$age2, nortest::ad.test)
bartlett.test(busan$w7, busan$age2, data=w7_na)

aw.ano <- oneway.test(w7~age2, w7_na, var.equal=F)
aw.ano
aw.model <- aov(w7~age2, w7_na)
aw.comparison <- LSD.test(aw.model, "age2", p.adj = "bonferroni", group = T)
aw.comparison

#연령대별 부산시 정주의사
busan$age2;busan$opinion2
tapply(busan$opinion2, busan$age2, nortest::ad.test)
bartlett.test(busan$opinion2, busan$age2, data=busan)

ao.ano <- oneway.test(opinion2~age2, busan, var.equal=F)
ao.ano
ao.model <- aov(opinion2~age2, busan)
ao.comparison <- LSD.test(ao.model, "age2", p.adj = "bonferroni", group = T)
ao.comparison



#3-f42_2 anova#######################
#월평균 가구소득에 따른 삶의만족도 
busan$f42_2[busan$f42==1 | busan$f42==2] <- "0~200만원미만"
busan$f42_2[busan$f42==3 | busan$f42==4] <- "200~400만원미만"
busan$f42_2[busan$f42==5 | busan$f42==6] <- "400~600만원미만"
busan$f42_2[busan$f42==7 | busan$f42==8] <- "600~800만원미만"
busan$f42_2[busan$f42==9] <- "800만원이상"

busan$f42_2;busan$s31
tapply(busan$s31, busan$f42_2, nortest::ad.test)
bartlett.test(busan$s31, busan$f42_2, data=busan)

fs.ano <- oneway.test(s31~f42_2, busan, var.equal=F)
fs.ano
fs.model <- aov(s31~f42_2, busan)
fs.comparison <- LSD.test(fs.model, "f42_2", p.adj = "bonferroni", group = T)
fs.comparison

#월평균 가구소득에 따른 근로여건만족도
w7_na$f42_2[w7_na$f42==1 | w7_na$f42==2] <- "0~200만원미만"
w7_na$f42_2[w7_na$f42==3 | w7_na$f42==4] <- "200~400만원미만"
w7_na$f42_2[w7_na$f42==5 | w7_na$f42==6] <- "400~600만원미만"
w7_na$f42_2[w7_na$f42==7 | w7_na$f42==8] <- "600~800만원미만"
w7_na$f42_2[w7_na$f42==9] <- "800만원이상"

w7_na$f42_2;w7_na$w7
tapply(w7_na$w7, w7_na$f42_2, nortest::ad.test)
bartlett.test(w7_na$w7, w7_na$f42_2, data=w7_na)

fw.ano <- oneway.test(w7~f42_2, w7_na, var.equal=F)
fw.ano
fw.model <- aov(w7~f42_2, w7_na)
fw.comparison <- LSD.test(fw.model, "f42_2", p.adj = "bonferroni", group = T)
fw.comparison

#월평균 가구소득에 따른 부산시 정주의사
busan$f42_2;busan$opinion2
tapply(busan$opinion2, busan$f42_2, nortest::ad.test)
bartlett.test(busan$opinion2, busan$f42_2, data=busan)

fo.ano <- oneway.test(opinion2~f42_2, busan, var.equal=T)
fo.ano
fo.model <- aov(opinion2~f42_2, busan)
fo.comparison <- LSD.test(fo.model, "f42_2", p.adj = "bonferroni", group = T)
fo.comparison


#4-w1 anova#######################

busan$w1 <- ifelse(busan$w1==7 | busan$w1==8, NA, busan$w1)
busan$w2 <- ifelse(busan$w2==9, NA, busan$w2)
busan$w4_0 <- ifelse(busan$w4_0==9 | busan$w4_0==10, NA, busan$w4_0)

#취업 경쟁력 요인에 따른 삶의 만족도
w1_na$w1;w1_na$s31
tapply(w1_na$s31, w1_na$w1, nortest::ad.test)
bartlett.test(w1_na$s31, w1_na$w1, data=w1_na)

ws.ano <- oneway.test(s31~w1, w1_na, var.equal=F)
ws.ano
ws.model <- aov(s31~w1, w1_na)
ws.comparison <- LSD.test(ws.model, "w1", p.adj = "bonferroni", group = T)
ws.comparison

#취업 경쟁력 요인에 따른 근로여건만족도
w1w7_na<-busan %>% filter(!is.na(w1+w7))     #w1,w7 결측치 제거해서 저장
w1w7_na$w1
w1w7_na$w7

w1w7_na$w1;w1w7_na$w7
tapply(w1w7_na$w7, w1w7_na$w1, nortest::ad.test)
bartlett.test(w1w7_na$w7, w1w7_na$w1, data=w1w7_na)

w17.ano <- oneway.test(w7~w1, w1w7_na, var.equal=F)
w17.ano
w17.model <- aov(w7~w1, w1w7_na)
w17.comparison <- LSD.test(w17.model, "w1", p.adj = "bonferroni", group = T)
w17.comparison

#취업경쟁 요인에 따른 정주의사
w1_na$w1;w1_na$opinion2
tapply(w1_na$opinion2, w1_na$w1, nortest::ad.test)
bartlett.test(w1_na$opinion2, w1_na$w1, data=w1_na)  #>0.05

w1o.ano <- oneway.test(opinion2~w1, w1_na, var.equal=T)  ##통계적 유의한 차이X 
w1o.ano
w1o.model <- aov(opinion2~w1, w1_na)
w1o.comparison <- LSD.test(w1o.model, "w1", p.adj = "bonferroni", group = T)
w1o.comparison


#5-w2 anova#######################

#취업애로요인에 따른 삶의만족도
w2_na$s31;w2_na$w2
tapply(w2_na$s31, w2_na$w2, nortest::ad.test)
bartlett.test(w2_na$s31, w2_na$w2, data=w2_na)

w2s.ano <- oneway.test(s31~w2, w2_na, var.equal=F)
w2s.ano
w2s.model <- aov(s31~w2, w2_na)
w2s.comparison <- LSD.test(w2s.model, "w2", p.adj = "bonferroni", group = T)
w2s.comparison

#취업애로요인에 따른 근로여건 만족도
w2w7_na<-busan %>% filter(!is.na(w2+w7))     #w1,w7 결측치 제거해서 저장
w2w7_na$w2
w2w7_na$w7

w2w7_na$w2;w2w7_na$w7
tapply(w2w7_na$w7, w2w7_na$w2, nortest::ad.test)
bartlett.test(w2w7_na$w7, w2w7_na$w1, data=w2w7_na)

w27.ano <- oneway.test(w7~w2, w2w7_na, var.equal=F)
w27.ano
w27.model <- aov(w7~w2, w2w7_na)
w27.comparison <- LSD.test(w27.model, "w2", p.adj = "bonferroni", group = T)
w27.comparison

##취업애로요인에 따른 부산시 정주의사
w2_na$w2;w2_na$opinion2
tapply(w2_na$opinion2, w2_na$w2, nortest::ad.test)
bartlett.test(w2_na$opinion2, w2_na$w2, data=w2_na)

w2o.ano <- oneway.test(opinion2~w2, w2_na, var.equal=F) 
w2o.ano
w2o.model <- aov(opinion2~w2, w2_na)
w2o.comparison <- LSD.test(w2o.model, "w2", p.adj = "bonferroni", group = T)
w2o.comparison


#6-w4 anova#######################
#직업선택요인에 따른 삶의만족도 
w4_0_na$s31;w4_0_na$w4_0
tapply(w4_0_na$s31, w4_0_na$w4_0, nortest::ad.test)
bartlett.test(w4_0_na$s31, w4_0_na$w4_0, data=w4_0_na)

w4s.ano <- oneway.test(s31~w4_0, w4_0_na, var.equal=F)
w4s.ano
w4s.model <- aov(s31~w4_0, w4_0_na)
w4s.comparison <- LSD.test(w4s.model, "w4_0", p.adj = "bonferroni", group = T)
w4s.comparison

##직업선택요인에 따른 근로여건만족도
w4w7_na<-busan %>% filter(!is.na(w4_0+w7))     #w4,w7 결측치 제거해서 저장
w4w7_na$w4_0
w4w7_na$w7

w4w7_na$w4;w4w7_na$w7
tapply(w4w7_na$w7, w4w7_na$w4_0, nortest::ad.test)
bartlett.test(w4w7_na$w7, w4w7_na$w4_0, data=w4w7_na)

w47.ano <- oneway.test(w7~w4_0, w4w7_na, var.equal=F)
w47.ano
w47.model <- aov(w7~w4_0, w4w7_na)
w47.comparison <- LSD.test(w47.model, "w4_0", p.adj = "bonferroni", group = T)
w47.comparison

##직업선택요인에 따른 부산시 정주의사
w4_0_na$w4_0;w4_0_na$opinion2
tapply(w4_0_na$opinion2, w4_0_na$w4_0, nortest::ad.test)
bartlett.test(w4_0_na$opinion2, w4_0_na$w4_0, data=w4_0_na)

w4o.ano <- oneway.test(opinion2~w4_0, w4_0_na, var.equal=F) 
w4o.ano
w4o.model <- aov(opinion2~w4_0, w4_0_na)
w4o.comparison <- LSD.test(w4o.model, "w4_0", p.adj = "bonferroni", group = T)
w4o.comparison





##민희##

#그룹A=타지거주경험없음  그룹B=타지거주경험있음
groupA<-subset(busan,busan$sl22==1)
groupB<-subset(busan,busan$sl22==2)

#타지거주경험에 따른 삶의만족도
var.test(groupA$s31,groupB$s31)    
wilcox.test(groupA$s31,groupA$s31,alter="two.sided",conf.int = TRUE,conf.level = 0.95)

#타지거주경험에 따른 근로여건만족도
groupA_w7na<-subset(w7_na,w7_na$sl22==1)  
groupB_w7na<-subset(w7_na,w7_na$sl22==2)
var.test(groupA_w7na$w7,groupB_w7na$w7)    
wilcox.test(groupA_w7na$w7,groupB_w7na$w7,alter="two.sided",conf.int = TRUE,conf.level = 0.95)

#타지 거주 경험에 따른 부산시 정주의사
var.test(groupA$opinion2,groupB$opinion2)  
wilcox.test(groupA$opinion2,groupB$opinion2,alter="two.sided",conf.int = TRUE,conf.level = 0.95)





#이야기상대 존재여부에 따른 삶의만족도
var.test(groupA_s$s31,groupB_s$s31)    
wilcox.test(groupA_s$s31,groupB_s$s31,alter="two.sided",conf.int = TRUE,conf.level = 0.95)

#이야기상대 존재여부에 따른 근로여건만족도
groupA_s_w7na<-subset(w7_na,w7_na$s29_3==1)   #그룹A=이야기상대있음 #그룹B=이야기상대없음
groupB_s_w7na<-subset(w7_na,w7_na$s29_3==2)
var.test(groupA_s_w7na$w7,groupB_s_w7na$w7)    
wilcox.test(groupA_s_w7na$w7,groupB_s_w7na$w7,alter="two.sided",conf.int = TRUE,conf.level = 0.95)

#이야기상대 존재여부에 따른 부산시 정주의사
groupA_s<-subset(busan,busan$s29_3==1)   
groupB_s<-subset(busan,busan$s29_3==2)

var.test(groupA_s$opinion2,groupB_s$opinion2)    
wilcox.test(groupA_s$opinion2,groupB_s$opinion2,alter="two.sided",conf.int = TRUE,conf.level = 0.95)





###################anova  점유형태(문항48), 정주의사(문항23)##########################################


#점유형태에 따른 삶의만족도
tapply(busan$s31, busan$f48,nortest::ad.test)  
bartlett.test(busan$s31, busan$f48, data=busan) 
fs.ano <- oneway.test(s31~f48, busan, var.equal=F)     
fs.ano                                                   

fs.model <- aov(s31~f48,busan)                  
fs.comparison <- LSD.test(fs.model, "f48", p.adj = "bonferroni", group = T)   
fs.comparison


#점유형태에 따른 근로여건만족도
tapply(w7_na$w7, w7_na$f48,nortest::ad.test)  
bartlett.test(w7_na$w7, w7_na$f48, data=w7_na)  
fw.ano <- oneway.test(w7~f48, w7_na, var.equal=T)    
fw.ano                                                  

fw.model <- aov(w7~f48,w7_na)                 
fw.comparison <- LSD.test(fw.model, "f48", p.adj = "bonferroni", group = T)   
fw.comparison

#점유형태에 따른 부산시 정주의사
tapply(busan$opinion2, busan$f48,nortest::ad.test)  
bartlett.test(busan$opinion2, busan$f48, data=busan)  
fo.ano <- oneway.test(opinion2~f48, busan, var.equal=F)   
fo.ano                                                 

fo.model <- aov(opinion2~f48,busan)       
fo.comparison <- LSD.test(fo.model, "f48", p.adj = "bonferroni", group = T)  
fo.comparison




#혼인상태에 따른 삶의만족도
tapply(busan$s31, busan$marry,nortest::ad.test)  
bartlett.test(busan$s31, busan$marry, data=busan)  
ms.ano <- oneway.test(s31~marry, busan, var.equal=F)    
ms.ano                                                   

ms.model <- aov(s31~marry,busan)                  
ms.comparison <- LSD.test(ms.model, "marry", p.adj = "bonferroni", group = T)   
ms.comparison


#혼인상태에 따른 근로여건만족도
tapply(w7_na$w7, w7_na$marry,nortest::ad.test)  
bartlett.test(w7_na$w7, w7_na$marry, data=w7_na)  
mw.ano <- oneway.test(w7~marry, w7_na, var.equal=F)   
mw.ano                                                   

mw.model <- aov(w7~marry,w7_na)                 
mw.comparison <- LSD.test(mw.model, "marry", p.adj = "bonferroni", group = T)  
mw.comparison

#혼인상태에 따른 정주의사
tapply(busan$opinion2, busan$marry,nortest::ad.test)
bartlett.test(busan$opinion2, busan$marry, data=busan)  
mo.ano <- oneway.test(opinion2~marry, busan, var.equal=F)    
mo.ano                                                   

mo.model <- aov(opinion2~marry,busan)                 
mo.comparison <- LSD.test(mo.model, "marry", p.adj = "bonferroni", group = T)  
mo.comparison



#직업 1.전문관리 2.사무 3.서비스판매 4.농어업 5.기능노무

#직업군에 따른 삶의만족도
tapply(busan$s31, busan$job,nortest::ad.test)  
bartlett.test(busan$s31, busan$job, data=busan)  
js.ano <- oneway.test(s31~job, busan, var.equal=F)    
js.ano                                                  

js.model <- aov(s31~job,busan)                
js.comparison <- LSD.test(js.model, "job", p.adj = "bonferroni", group = T)   
js.comparison


#직업군에 따른 근로여건만족도
tapply(w7_na$w7, w7_na$job,nortest::ad.test)  
bartlett.test(w7_na$w7, w7_na$job, data=w7_na)  
jw.ano <- oneway.test(w7~job, w7_na, var.equal=F)   
jw.ano                                                  

jw.model <- aov(w7~job,w7_na)                  
jw.comparison <- LSD.test(jw.model, "job", p.adj = "bonferroni", group = T)   
jw.comparison

#직업군에 따른 부산시 정주의사
tapply(busan$opinion2, busan$job,nortest::ad.test)
bartlett.test(busan$opinion2, busan$job, data=busan)  
jo.ano <- oneway.test(opinion2~job, busan, var.equal=T)     
jo.ano                                                   

jo.model <- aov(opinion2~job,busan)                  
jo.comparison <- LSD.test(jo.model, "job", p.adj = "bonferroni", group = T)   
jo.comparison



