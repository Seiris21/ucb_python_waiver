#!/usr/bin/env python
"""
Derrick Hee
Assignment 6

Makeplot()
    Makes 3 plots. Data file must be in same folder as program. The 3 plots will be generated in the same folder. Will make a boxplot, a scatter plot and a heatmap. Will also print out linreg analysis for scatterplot
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

#read dataframe in
data = pd.read_csv('serotonin_data.txt')

def makePlot():
    #make box plots in same image file
    fig = plt.figure()
    fig, axes = plt.subplots(1,2)
    #Boxplot 1 , mem by gene1
    data.boxplot(column='mem', by='gene1', ax=axes[0], return_type='axes')
    #boxplot 2, mem by depr
    data.boxplot(column='mem', by='depr', ax=axes[1], return_type='axes')
    fig.suptitle('')
    #save figure
    fig.savefig('mem_gene1_depr.png',format='png')
    plt.close()
    
    #Subset to remove non-continuous, before correlation
    l_continuous=['par','sfc','aci','pci','u1','cau','th','put','mid','u2','mem','u','age','eta','day','T']
    #Make correlation matrix from subset
    correlation = data[l_continuous].corr()
    #print correlation.keys()
    #Set index for tick marks such that they line up with the squares in the heatmap
    index=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    index=[i-.5 for i in index]
    #Make heatmap
    heatmap,ax = plt.subplots()
    heatmap=ax.pcolor(correlation,cmap='RdBu')
    #Add X and Y labels to ticks, using index
    plt.xticks(index,correlation.keys(),rotation=90)
    plt.yticks(index,correlation.keys())
    #Add legend bar
    plt.colorbar(heatmap)
    #save figure
    plt.savefig('heatmap.png',format='png')
    plt.close()
    
    #Find highest correlation to mem, if highest is mem, set to a low number and try again
    not_mem=False
    l_mem_corr = list(correlation['mem'])
    while not_mem == False:
        highest = l_mem_corr.index(max(l_mem_corr))
        if l_continuous[highest] != 'mem':
            not_mem=True
        else:
            l_mem_corr[highest]=-30
    print "The Variable with the highest correlation with mem is "+l_continuous[highest]
    
    
    #Lin Reg Model
    model = smf.ols(formula='mem~eta',data=data)
    res=model.fit()
    #Print summary of statistics
    print res.summary()
    #Make scatterplot
    scatter = plt.figure()
    data.plot(x='eta',y='mem',kind='scatter')
    #Set up points to make line plot from
    X_plot=np.linspace(-8,6,100)
    #Add linear equation to scatter plot
    plt.plot(X_plot,res.params[1]*X_plot + res.params[0])
    #Set limits
    plt.xlim(xmin=-8,xmax=6)
    #Save figure
    plt.savefig('scatter.png',format='png')
    plt.close()
    
    
    