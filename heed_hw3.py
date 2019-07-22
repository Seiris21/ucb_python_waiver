#Problem 1: Perceptron
import matplotlib.pyplot as plt
import random
import pandas as pd
from sklearn import svm
from sklearn.metrics import confusion_matrix
from sklearn.metrics import zero_one_loss
p_data=[
    [-1,-1,0],
    [2,0,0],
    [2,1,0],
    [0,1,0],
    [0.5,1.5,0],
    [3.5,2.5,1],
    [3,4,1],
    [5,2,1],
    [5.5,3,1]]
#Passed to predict should be one sample and classification (ex:[-1,-1,0]) and weight ([weight var1, weight var2,intercept]
def predict(l_sample, l_weight):
    value=l_weight[-1]
    for i in range(len(l_sample)-1):
        value+=l_sample[i]*l_weight[i]
    if value >= 0.0:
        return 1.0
    else:
        return 0.0
        
def w_train(ll_data,i_rate,i_rep):
    random.seed(a=42)
    #initialize weights with random numberse
    l_weight=[]
    for i in range(len(ll_data[0])):
        l_weight.append(random.uniform(-.5,.5))
    print l_weight
    #for loop for iterations through data
    for rep in range(i_rep):
        #iterate through each row of data
        for sample in ll_data:
            #get prediction using current weight
            pred = predict(sample,l_weight)
            #calculate error (+-1), last element in sample is actual
            error = sample[-1]-pred
            #adjust intercept
            l_weight[-1]=l_weight[-1]+i_rate*error
            #adjust rest of weights
            for i in range(len(sample)-1):
                l_weight[i]=l_weight[i]+i_rate*error*sample[i]
    return l_weight
    
def plot_percep(ll_data,l_weight):
    #Split x and y coordinates
    x=[]
    y=[]
    for i in ll_data:
        x.append(i[0])
        y.append(i[1])
    fig = plt.figure()
    ax1=fig.add_subplot(111)
    ax1.set_xlim([-2,6])
    ax1.set_ylim([-2,6])
    ax1.scatter(x[0:5],y[0:5],c="r",label="Class 1")
    ax1.scatter(x[5:],y[5:],c="b",label="Class 2")
    #Calculate decision boundary
    ax1.plot([0,-l_weight[2]/l_weight[1]],[-l_weight[2]/l_weight[0],0])
    plt.show()
    
def calc_percep(iter):
    weight=w_train(p_data,.01,iter)
    plot_percep(p_data,weight)
    return weight
    
    
#Problem 2: SVM

#I replaced double spaces in files with commas for simplicity. Also removed the 2 whitespace in front of every line (why is that even there)
def read_pima(filename):
    data=pd.read_csv(filename,sep=",",header=None)
    data_value=[]
    data_target=[]
    for i in data.values:
        data_value.append(i[0:-1])
        if i[-1]==1:
            data_target.append(i[-1])
        elif i[-1]==0:
            data_target.append(-1)
    return data_value, data_target

def run_svm(train_value, train_target,test_value,test_target):
    clf=svm.LinearSVC()
    clf.fit(train_value,train_target)
    train_predict=clf.predict(train_value)
    test_predict=clf.predict(test_value)
    return train_predict,test_predict

def calc_svm():
    train_value,train_target=read_pima('pima_train.txt')
    test_value,test_target=read_pima('pima_test.txt')
    train_predict,test_predict=run_svm(train_value, train_target,test_value,test_target)
    #print train_predict
    print "Train missclassification:"
    print zero_one_loss(train_target,train_predict)
    print "Test missclassification:"
    print zero_one_loss(test_target, test_predict)
    print "Train CM:"
    print confusion_matrix(train_target,train_predict)
    print "Test CM:"
    print confusion_matrix(test_target,test_predict)
    






