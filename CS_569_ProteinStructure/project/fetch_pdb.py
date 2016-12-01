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

# global variables to fethch file
blast_url         = "http://www.rcsb.org/pdb/rest/getBlastPDB1"
blast_parameter1  = "?sequence="
blast_parameter2  = "&eCutOff=1E-20&matrix=BLOSUM62&outputFormat=HTML"

pdb_report_url    = "http://www.rcsb.org/pdb/rest/customReport.csv"
report_parameter1 = "?pdbids="
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
    
pdbids_dic,pdbids_list = retrieve_pdb_ids(dic)