import numpy as np
from random import randrange
from math import sqrt
from sklearn import metrics
from sklearn import ensemble
from ggplot import *
import pandas as pd

filepath = "data/wdbc.csv"
#wdbc.data Wisconsin Diagnostic Data
header = ['ID','Diagnosis','radius1','texture1','perimeter1','area1','smoothness1','compactness1','concavity1','concavepoints1','symmetry1','fractaldim1','radius2','texture2','perimeter2','area2','smoothness2','compactness2','concavity2','concavepoints2','symmetry2','fractaldim2','radius3','texture3','perimeter3','area3','smoothness3','compactness3','concavity3','concavepoints3','symmetry3','fractaldim3']
#Malignant = 1, Benign = 0
dat = np.genfromtxt(filepath,dtype=None,delimiter=',',names=None)


#Print Gini to test
def calc_gini(leaves, l_classification):
    gini = 0
    for diag in l_classification:
        for leaf in leaves:
            if len(leaf) == 0:
                continue
            #Compare proportion of diagnosis
            prop = [row[1] for row in leaf].count(diag)/float(len(leaf))
            gini += (prop*(1.0-prop))
    #print gini
    return gini
    
def prelim_split(dat, index, value):
    a = list()
    b = list()
    for line in dat:
        if line[index]<value:
           a.append(line)
        else:
           b.append(line)
    return a , b
    
#Calculate Splits
def calc_split(dat,n_feature):
    #Pull classification out
    l_classification=list()
    for sample in dat:
        l_classification.append(sample[1])
    #Initialize variables
    v_index = 1000
    v_value = 1000
    v_score = 1000
    v_groups = None
    #Randomly get unique features up to n_feature to compare for split.
    l_features = list()
    while len(l_features)<n_feature:
        index = randrange(2,len(dat[1]))
        if index not in l_features:
            l_features.append(index)
    for index in l_features:
        for row in dat:
            leaves = prelim_split(dat,index,row[index])
            #print leaves
            gini_score = calc_gini(leaves,l_classification)
            if gini_score<v_score:
                v_index = index
                v_value = row[index]
                v_score = gini_score
                v_groups = leaves
    return {'index':v_index,'value':v_value,'groups':v_groups}
    
#Set a terminal node
def set_terminal(group):
    outcomes = [sample[1] for sample in group]
    return max(set(outcomes),key = outcomes.count)
    
    
#Define spliting of nodes after initial. RF goes to max depth 
#Initially wanted to go to max depth, building a tree took too much time, and random forests need a decent number of trees   
def sub_split(node, n_features,max_depth,depth):
    left, right = node['groups']
    del(node['groups'])
    #Check for no split (2 subgroups don't exist or one group is empty)
    if not left or not right:
        node['left']=node['right'] = set_terminal(left+right)
        return
    #Check if depth is reached (added due to unpacking error in python)
    if depth >= max_depth:
        node['left'] = set_terminal(left)
        node['right'] = set_terminal(right)
    #Processing L/R
    #Check if node has hit terminal (no pruning)
    if len(left) == 1:
        node['left'] = set_terminal(left)
    else:
        node['left']= calc_split(left,n_features)
        sub_split(node['left'],n_features,max_depth,depth+1)
    #Repeat for right. Check if node has hit terminal (no pruning)
    if len(right) == 1:
        node['right'] = set_terminal(right)
    else:
        node['right'] = calc_split(right,n_features)
        sub_split(node['right'],n_features,max_depth,depth+1)
    
def make_tree(train,n_features,max_depth):
    tree = calc_split(train,n_features)
    #print tree
    sub_split(tree,n_features,max_depth,1)
    return tree

def subset(dataset):
    sample = list()
    n_sample = round(len(dataset)/3)
    while len(sample)<n_sample:
        index = randrange(len(dataset))
        sample.append(dataset[index])
    return sample
def predict(node,row):
    if row[node['index']]<node['value']:
        #If dictionary, there are more subnodes
        if type(node['left']) is dict:
            return predict(node['left'],row)
        else:
            return node['left']
    else:
        #If dictionary, there are more subnodes
        if type(node['right']) is dict:
            return predict(node['right'],row)
        else:
            return node['right']
#Prediction using trees made for random forest            
def rf_pred(trees,row):
    pred = [predict(tree,row) for tree in trees]
    #return prediction with most votes
    return max(set(pred),key = pred.count)

def accuracy(actual,pred):
    counter = 0
    for i in range(len(actual)):
        if actual[i] == pred[i]:
            counter += 1
    accuracy = counter/float(len(actual))*100.0
    #Confusion matrix, 2 lists in order of Predicted 1, Predicted 0
    actual_m = [0,0]
    actual_b = [0,0]
    for i in range(len(actual)):
        if actual[i] == 1:
            if pred[i] == 1:
                actual_m[0] += 1
            elif pred[i]==0:
                actual_m[1] += 1
        elif actual[i]==0:
            if pred[i] == 1:
                actual_b[0] += 1
            elif pred[i]==0:
                actual_b[1] += 1
    confusion = pd.DataFrame.from_items([('Actual Malignant',actual_m),('Actual Benign',actual_b)],orient='index',columns=['Predicted Malignant','Predicted Benign'])
    return accuracy,confusion
    
#random forest
def random_forest(train,test,n_trees,n_features,max_depth):
    trees = list()
    print "Making Trees"
    for i in range(n_trees):
        sample = subset(train)
        tree = make_tree(sample,n_features,max_depth)
        trees.append(tree)
    print 'Trees made'
    pred = [rf_pred(trees,row) for row in test]
    return trees, pred

def run_rf(dataset,n_trees,max_depth):
    train,test=dat_split(dataset)
    n_features = sqrt(len(train[1]))
    trees, rf_pred = random_forest(train,test,n_trees,n_features,max_depth)
    actual = [row[1] for row in test]
    score,matrix= accuracy(actual,rf_pred)
    print score
    print matrix
    print metrics.confusion_matrix(actual,rf_pred)
    return trees, score,matrix,actual,rf_pred

def scikit_rf(n_tree,max_depth):
    df = pd.DataFrame(dat)
    df.columns = header
    df['train'] = np.random.uniform(0,1,len(df))<=.66
    train,test = df[df['train']==True], df[df['train']==False]
    features = df.columns[2:]
    rf = ensemble.RandomForestClassifier(n_jobs = n_tree)
    rf.fit(train[features],train["Diagnosis"])
    pred = rf.predict(test[features])
    print pred
    cm = pd.crosstab(test['Diagnosis'],pred,rownames = ['actual'],colnames = ['pred'])
    return test['Diagnosis'],pred, cm
    
def draw_ROC(test_actual, pred,name):
    fpr, tpr, _ = metrics.roc_curve(test_actual,pred)
    df = pd.DataFrame(dict(fpr=fpr, tpr=tpr))
    auc = metrics.auc(fpr,tpr)
    p = ggplot(df, aes(x='fpr', y='tpr'))+geom_line()+geom_abline(linetype='dashed')+geom_area(alpha=0.2)+ggtitle("ROC+AUC=%s"%str(auc))
    p.save(name)
    
def dat_split(dataset):
    #2/3 is training, 1/3 is test
    train_set = 2*len(dataset)/3
    l_train_index = np.random.choice(range(len(dataset)),train_set,replace = False)
    train = list()
    test = list()
    for i in range(len(dataset)):
        if i in l_train_index:
            train.append(dataset[i])
        else:
            test.append(dataset[i])
    return train,test
    
    
    
    
    
    
    
    