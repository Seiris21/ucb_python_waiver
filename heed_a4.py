#!/usr/bin/env python
"""
Derrick Hee
Assignment 4 Python
10/21/2016
Functions:

SeqTypeError(string): Error to return if sequence given has characters not in [ATCG]

DNAseq class: Class for DNA sequence. Can pass sequence when making or later using set_sequence function. If sequence is not entirely ATCG, will return SeqType Error. Also has function for finding enzyme restriction sites (restriction_site) which prints out the enzyme followed by the sequence that matches that enzyme's restriction site.

Wikiscrape(): Read the URL for Nucleic Acid notation and scrapes the information off hte table. Specifically scrapes ('W','S','M','K','R','Y','N') as specified in HW4. 
"""
from bs4 import BeautifulSoup as bs
from urllib import urlopen
import re

#Open URL _ read
url = urlopen('https://en.wikipedia.org/wiki/Nucleic_acid_notation').read()
lxml = bs(url,'lxml')
table = lxml.find('table')
#Find rows
allRow=table.findAll('tr')
d_table={}
#Ignore header, cycle through rest
for row in allRow[1:]:
    cell = row.findAll('td')
    newCell=[]
    for c in cell:
        newCell.append(c.getText())
    #Look for specific Nucleotide for dictionary
    if newCell[0] in ('W','S','M','K','R','Y','N'):
        l_nuc=''
        for i in newCell[2:6]:
            if i != '':
                l_nuc=l_nuc+i
        d_table.update({newCell[0]:l_nuc})
print d_table

#EcoRI: GAATTC
#Eali: YGGCCR
#Erhl: CCWWGG
#Ecal GGTNACC
#Fbli GTMKAC
#enzyme dict{'EcoRI':'GAATTC','Eali':'[CT]G{2}C{2}[AG]','Erhl':'C{2}[AT]{2}G{2}','Ecal':'G{2}T[ATCG]ACC','Fbli':'GT[AC][GT]AC'}
#Given Enzyme dictionary
d_enzyme={'EcoRI':'GAATTC','Eali':'YGGCCR','Erhl':'CCWWGG','Ecal':'GGTNACC','Fbli':'GTMKAC'}
print d_enzyme
#Substitute each char in dictionary for nucleotide equivalent in regex format
for i in d_enzyme.keys():
    s=''
    for j in d_enzyme[i]:
        if j in d_table.keys():
            s=s+'['+d_table[j]+']'
        #Assumption is we know N, should be caught in table making loop regardless
        elif j == "N":
            s=s+'[ATCG]'
        #If nucleotide (ATCG) then just glue it on the end
        elif j in ('A','T','C','G'):
            s=s+j
        else:
            print 'Character not recognized: '+j
    d_enzyme.update({i:s})
print d_enzyme

class SeqTypeError(Exception):
    def __inti__(self,string):
        self.seq=string
    def __str__(self):
        return 'Sequence given was not DNA sequence'

class DNAseq:
    sequence='NA'

    ResEnzymeDict=d_enzyme
    def __init__(self,sequence):
        if re.search('[^ATCG]',sequence) != None:
            raise SeqTypeError(sequence)
        else:
            self.sequence=sequence
    def set_sequence(self,sequence):
        if re.search('[^ATCG]',sequence) != None:
            raise SeqTypeError(sequence)
        else:
            self.sequence=sequence
    def restriction_sites(self):
        seq=self.sequence
        for i in self.ResEnzymeDict.keys():
            find = re.finditer(self.ResEnzymeDict[i],self.sequence)
            for j in find:
                print i
                print j.group()
        
        
        

def wikiScrape():
    url = urlopen('https://en.wikipedia.org/wiki/Nucleic_acid_notation').read()
    lxml = bs(url,'lxml')
    table = lxml.find('table')
    allRow=table.findAll('tr')
    d_table1={}
    for row in allRow[1:]:
        cell = row.findAll('td')
        newCell=[]
        for c in cell:
            newCell.append(c.getText())
        if newCell[0] in ('W','S','M','K','R','Y','N'):
            l_nuc=[]
            for i in newCell[2:6]:
                if i != '':
                    l_nuc.append(i)
            d_table1.update({newCell[0]:l_nuc})
    return d_table1
