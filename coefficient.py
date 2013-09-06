#!/usr/bin/python

#Lingyi Lu
#lingyics@gmail.com

#Homework 1
#CSE 411
#09/01/2013

from math import sqrt
from numpy import*
from operator import itemgetter
from itertools import combinations
#get the data into x_list and y_list from the file
def readfile(fname):
    """This function read the file as input"""
    try:
        file=open(fname,'r+')
        all_lines=file.readlines()
    except:
        print "Could not find the file to open."
    x_list=[]
    y_list=[]
    for each_line in all_lines:
        x=each_line.strip().split()[0]                
        y=each_line.strip().split()[1]
        x_list.append(int(x))
        y_list.append(int(y))
    file.close()
    return x_list, y_list

#Pearson's Correlation Coefficient

#Reference of Algorithm:
#http://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient

def pearson(x_list, y_list):
    """This function computes Pearson Coefficient between two lists"""
    x=sum(x_list)
    y=sum(y_list)
    xx=0
    yy=0
    xy=0
    n=len(x_list)  #the same as n=len(y_list)
    for i in range(n):
        xy+=x_list[i]*y_list[i]
        xx+=x_list[i]*x_list[i]
        yy+=y_list[i]*y_list[i]              
    #calculate the Pearon's cofficient
    pearson_r=((n*xy)-(x*y))/math.sqrt((n*xx-(x*x))*(n*yy-(y*y)))
    return pearson_r
#Spearman's Rank Correlation Cofficient
#Reference of Algorithm:
#http://en.wikipedia.org/wiki/Spearman's_rank_correlation_coefficient
def rank_index(data):
    """This ranking function calculates the rank for each item in the list"""
    #In this case I take both the tie situation and the unique number situation
    #into consideration
    (m_data, n_data)=zip(*sorted(list(enumerate(data)),key=itemgetter(1)))
    #the algorithm for aver_rank is from WiKi
    sum_ranks=0
    tie_count=0
    new_list=[0]*len(data)
    for i in range(len(data)):
        sum_ranks +=i
        tie_count +=1
        if i==len(data) -1 or n_data[i] != n_data[i+1]:
            aver_rank=sum_ranks/float(tie_count) +1
            for j in range(i+1-tie_count, i+1):
                new_list[m_data[j]]=aver_rank
            sum_ranks=0
            tie_count=0
    return new_list
        
def spearman(x_list, y_list):
    """This function computes Spearman's Coefficient between two lists"""
    x_rank=rank_index(x_list)
    y_rank=rank_index(y_list)
    n=len(x_list)
    dd=0
    for i in range(n):
        dd+=(x_rank[i]-y_rank[i])*(x_rank[i]-y_rank[i])
    spearman_r=float(1-((6*dd)/(n*(n*n-1))))
    return spearman_r

#Kendall's Rank Correlation Coefficient
#Reference of Algorithm:
#http://en.wikipedia.org/wiki/Kendall_tau_rank_correlation_coefficient
#http://stamash.org/calculating-kendalls-tau-rank-correlation-coefficient/

#In this coefficient we should take the "tie situation" into considieration
def kendall(x_list, y_list):
    """This function computes the Kendall rank coefficient"""
    N_x=0
    N_y=0
    tau_up=0
    for (i,j) in combinations(xrange(len(x_list)), 2):
        #I use the combinations for iteration:
        #e.g:combinations('ABCD', 2) -->AB AC AD BC BD CD
        tie_s=(x_list[i]-x_list[j])*(y_list[i]-y_list[j])
        #if there is no tie
        if tie_s:
            N_x+=1
            N_y+=1
            #if two items in x_list and y_list are concordant
            if tie_s>0:
                tau_up+=1
            # if two items in x_list and y_list are discordant
            elif tie_s<0:
                tau_up -=1
        #when tie exists in either x_list or y_list, the tie_s will be 0
        else:
            if x_list[i]-x_list[j]:
                N_x+=1
            elif y_list[i]-y_list[j]:
                N_y+=1
    tau=tau_up/sqrt(N_x*N_y)
    return tau

def main():
    x_list, y_list=readfile('data')
    pearson_r=pearson(x_list, y_list)
    print "Pearson's Correlation Coefficient: ", pearson_r 
    spearman_r=spearman(x_list, y_list)
    print "Spearman's Rank Correlation Coefficient: ", spearman_r
    kendall_tau=kendall(x_list, y_list)
    print "Kendall's Rankd Correlation Coefficient: ", kendall_tau

if __name__=="__main__":
    main()
