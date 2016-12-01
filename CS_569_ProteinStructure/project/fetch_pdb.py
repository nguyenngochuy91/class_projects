#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : Using the combination.fa file (this faile contains the sequence
              of amino acids of each operon that was a combination of fragmental
              part of best match protein from the pdb), we query search the pdb 
              automatically, then retrieve the classification of what the operon do
    Start   : 12/01/2016
    End     : 12/2016 
'''

from bs4 import BeautifulSoup
from urllib.request import urlopen

###############################################################################
## helper function

'''
    function: given operon_classification, write the operon ,and its classification into a text file
    input   : operon_classification
    output  : file
'''
def to_file(operon_classification):
    outfile = open('result.txt','w')
    for operon in operon_classification:
        outfile.write(operon)
        for classification in operon_classification[operon]:
            outfile.write('\t'+classification)
        outfile.write('\n')
    outfile.close()

###############################################################################
# global variables to fethch file
blast_url         = "http://www.rcsb.org/pdb/rest/getBlastPDB1"
blast_parameter1  = "?sequence="
blast_parameter2  = "&eCutOff=1E-20&matrix=BLOSUM62&outputFormat=HTML"

pdb_report_url    = "http://www.rcsb.org/pdb/rest/customReport.csv"
report_parameter2 = "&customReportColumns=classification&service=wsfile&format=csv"

'''
    function: parse the combination.fa, store as a dic with key as the operon name, 
                value stores the sequence
    input   : fasta (combination.fa)
    output  : dic (key: operon name,value: list(amino acid sequence))
'''
def parser(myfile):
    dic ={}
    infile = open(myfile,'r')
    operons = infile.read().split('>')
    for item in operons[1:]:
        info = item.split('\n')
        dic[info[0]]=info[1] # info[0] is the operon name, info[1] is the sequence
    return dic

dic = parser('combination.fa')

'''
    function: using the dictionary of operon and sequence, blast against pdb
              and retrieve the pdbids into a dic, and a list of all pdbid to retrieve classification
    input   : dic (key: operon name,value: list(amino acid sequence))
    output  : dic (key: operon name,value: list(pdbids)), set(pdbids)
'''
def retrieve_pdb_ids(dic):
    pdbids_dic ={}
    pdbids_list =set()
    for operon in dic:
        print ("Working on operon:",operon)
        URL = blast_url+blast_parameter1+dic[operon]+blast_parameter2
        soup = BeautifulSoup(urlopen(URL)) # fetch the file 
        text = soup.text
        # parsing the text in the best way to retrieve ID
        # print (text)
        info = text.split('>')[0]
        info = info.split('Value\n')
        # print ("info",info)
        # print (len(info))
        if len(info) == 1:
            continue
        info = info[1].split('\n')
        pdb_list =[] # initiate empty list to add pdbId name
        for item in info:
            if len(item) != 0:
                id = item[:4]
                pdb_list.append(id)
                pdbids_list.add(id)
        pdbids_dic[operon] = pdb_list
    return pdbids_dic,pdbids_list
    
# pdbids_dic,pdbids_list = retrieve_pdb_ids(dic)

'''
    function: using the pdbids_list to retrieve the classification into a dic
    input   : set(pdbids)
    output  : dic (key: pdbid,value: classification)
'''

def retrieve_pdb_classification(pdbids_list):
    report_parameter1 = "?pdbids="
    classification_dic ={}
    for pdb_id in pdbids_list:
        report_parameter1 += pdb_id+','
    URL  = pdb_report_url+report_parameter1[:-1]+report_parameter2
    soup = BeautifulSoup(urlopen(URL)) # fetch the file 
    text = soup.text
    text = text.replace('"','')
    core_info = text.split('\n')[1:-1]
    for info in core_info:
        info = info.split(',')
        classification_dic[info[0]]=info[1]
    return classification_dic
    
# classification_dic = retrieve_pdb_classification(pdbids_list)

'''
    function: using the info from pdbids_dic, and classification_dic to predict
              classification for the operon
    input   : dic (key: pdbid,value: classification), dic (key: operon name,value: list(pdbids))
    output  : dic (key: operon, value: set of classification)
'''
def predict_classification(pdbids_dic,classification_dic):
    operon_classification = {}
    for operon in pdbids_dic:
        classification = set()
        for pdb_id in pdbids_dic[operon]:
            classification.add(classification_dic[pdb_id])
        operon_classification[operon] = classification
    return operon_classification
    
#operon_classification =  predict_classification(pdbids_dic,classification_dic)
to_file(operon_classification)
