#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : providing 2 method to study operon functionality
            1) Method 1: predict structure for each genes in each operon
                         do a docking for the genes structure in an operon
                         utilize structure alignment to predict functionality
            2) Method 2: Blast each gene against pdb file, then combine the 
                        sequence to blase gainst pdb database
'''


from Bio.PDB.PDBParser import PDBParser
from Bio.PDB import PDBIO
from Bio.PDB.PDBIO import Select
from Bio import SeqIO
import os
pdb_dir = 'pdb/'
operon_dir = 'operon/'
###############################################################################
## helper functions
###############################################################################
'''
    function: parsing the gene_block_names_and_genes.txt, create a dic
                with key as the operon and value is its gene
    input: gene_block_names_and_genes.txt
    output: dic (key: operon name, value: genes)
'''
def get_operon_genes(myfile):
    infile = open(myfile,'r')
    dic ={}
    for line in infile.readlines():
        line = line.strip()
        line = line.split('\t')
        dic[line[0]]=line[1:]
    return dic

operon = get_operon_genes('gene_block_names_and_genes.txt')

'''
    function: parsing the gene_block_query and retrieve the translation of each gene into a dic
    input: gene_block_query.fa
    output: dic (key: gene, value: translation)
'''
def get_translation(myfile):
    dic = {}
    for seq_record in SeqIO.parse(myfile, "fasta"):
        dic[(seq_record.id).split('|')[3]] = seq_record.seq
    return dic

###############################################################################
## Method 1
###############################################################################
'''
    function: take in a blast file, file the best matching between a gene and 
                an available pdb file
    input: blast file
    output: dic (key: gene name, value: tuple (pdb file name, start of the pdb file ,stop of the pdb file,length))
'''
def get_best_match_gene_pdb(blast):
    infile = open(blast,'r')
    dic ={}
    for line in infile.readlines():
        line = line.strip()
        line = line.split('\t')
        pdb_info = line[0].split('|')[0]
        gene_info = line[1].split('|')[3]
        start = int(line[6])
        stop = int(line[7])
        length = abs(stop-start)
        if gene_info not in dic:
            if length >=10:
                if start < stop:
                    dic[gene_info] = (pdb_info,start,stop,length)
                else:
                    dic[gene_info] = (pdb_info,stop,start,length)
        else:
            if dic[gene_info][3] < length:
                if start < stop:
                    dic[gene_info] = (pdb_info,start,stop,length)
                else:
                    dic[gene_info] = (pdb_info,stop,start,length)
    return dic

# dic = get_best_match_gene_pdb('output_reverse')
'''
    function: take in the dictionary from the previous function, find the right 
                pdb file, extract the coordinate of the nucleotide from the start position
    input: dic (key: gene name, value: tuple (pdb file name, start ,stop,length))
    output: dic (key: gene name, value: list of residues (which contain info about coordinate
             inside))
'''
def get_coordinate(dic):
    new_dic ={}
    for gene,pdb in dic.items():
        # get the info from the dic 
        pdb_info = pdb[0].split(':') # '1A9X:A' -> [1A9X,A]
        start = pdb[1]
        stop = pdb[2]
        filename = pdb_info[0].lower()
        chain = pdb_info[1]
        # parsing pdb file
        parser = PDBParser()
        try:
            structure = parser.get_structure(filename,pdb_dir+filename+'.pdb')
            # get the residues from pdb file given the start, stop position and chain 
            residues =[]
            for i in range(start,stop+1):
                try:
                    residues.append(structure[0][chain][i])
                except:
                    continue
            # assign key, value to the new_dic
            new_dic[gene] = residues
        except:
            continue
    return new_dic
        

# new_dic = get_coordinate(dic)   

    

'''
    function: pfrom the operon, figure out which operon has all of its gene matching
                with a pdb file
    input:  dic (key: operon name, value: genes),dic (key: gene name, value: list of residues (which contain info about coordinate
             inside))
    output: list (operon name that has all of its gene mapped)
'''
def get_all_map(operon,blast):
    operon_list =[]
    for operon_name,genes in operon.items():
        flag = True
        for gene in genes:
            if gene not in blast:
                flag= False
                break
        if flag:
            operon_list.append(operon_name)
    return operon_list

'''
    function: take in the dictionary from the previous function, find the right 
                pdb file, write out the right residue into new pdb file
    input: dic (key: gene name, value: tuple (pdb file name, start ,stop,length)), operon_list,operon
    output: a directory that name as the operon, inside is the protein matching file to the genes
'''
def write_specific_residue(blast,operon,operon_list):
    # iterate through the operon_list
    for operon_name in operon_list:
        # create dir for the operon_name
        os.mkdir(operon_dir+operon_name)
        for gene in operon[operon_name]:
            # get the info from the dic 
            pdb = blast[gene]
            pdb_info = pdb[0].split(':')
            start = pdb[1]
            stop = pdb[2]
            filename = pdb_info[0].lower()
            chain_info = pdb_info[1]
            # parsing pdb file
            parser = PDBParser()
            io = PDBIO()
            try:
                structure = parser.get_structure(filename,pdb_dir+filename+'.pdb')
                chain = structure[0][chain_info]
                io.set_structure(chain)
                class ResiSelect(Select):
                    def accept_residue(self, residue):
                         if residue.get_id()[1] in range(start,stop+1):
                             return True
                         else:
                             return False
                io.save(operon_dir+operon_name+'/'+gene+'.pdb', ResiSelect()) 
            except:
                continue


#blast = get_best_match_gene_pdb('output_reverse')  
#coordinates = get_coordinate(blast)   
#
#operon_list = get_all_map(operon,coordinates)
#write_specific_residue(blast,operon,operon_list)

###############################################################################
## Method 2
###############################################################################
'''
    function: take in a blast file, file the bag of protein structure that
                each gene has good hit
    input: blast file
    output: dic (key: gene name, value: tuple ((pdb file name, start  ,stop,length)), dic (key:gene name, value: set {pdb file names})
'''
def get_matches_gene_pdb(blast):
    dic = {}
    gene_pdb_bags ={}
    infile = open(blast,'r')
    for line in infile.readlines():
        line = line.split('\t')
        pdb_info = line[0].split('|')[0]
        gene_info = line[1].split('|')[3]
        start = int(line[8])
        stop = int(line[9])
        length = abs(stop-start)
        if gene_info not in dic:
            dic[gene_info] = set()
        if length >=10:
            if start < stop:
                dic[gene_info].add((pdb_info,start,stop,length))
            else:
                dic[gene_info].add((pdb_info,stop,start,length))
        if gene_info not in gene_pdb_bags:
            gene_pdb_bags[gene_info]=set()
        gene_pdb_bags[gene_info].add(pdb_info)

    return dic,gene_pdb_bags

blast,gene_pdb_bags = get_matches_gene_pdb('output_reverse')

###############################################################################
## sub method to check if there is a structure that combine all the genes

'''
    function: given the gene_pdb_bags, using the info from operon and operon list
              check if there is an intersection of protein file for all the genes 
              within an operon
    input: dic (key:gene name, value: set {pdb file names}), list (operon names), dic (key:operon, value: genes)
    output: dic (key: operon, value: list of intersected pdb file)
'''
def get_intersection_bags(gene_pdb_bags,operon, operon_list):
    dic ={}
    for operon_name in operon_list:
        intersection = gene_pdb_bags[operon[operon_name][0]] # get the bags of structure of the first gene in the operon
        for gene in operon[operon_name][1:]:
            intersection = intersection & gene_pdb_bags[gene]
        if len(intersection)!=0 :
            dic[operon_name] = intersection
    return dic    
###############################################################################
    
'''
    function: given operon_list, create a dictionary for those operon using info from operon dic.
                Then write this out into a fasta file
    input: dic (key: gene name, value: tuple ((pdb file name, start  ,stop,length)), dic (operon_list), dic (operon),
                file (fasta file)
    output: fasta file
'''

def retrieve_sequence_to_blast(blast,operon_list,operon, fasta):
    translation = get_translation('gene_block_query.fa')
    outfile = open(fasta,'w')
    for operon_name in operon_list:
        outfile.write('>'+operon_name+'\n')
        string = ''
        for gene in operon[operon_name]:
            length = 0
            start = 0
            stop = 0
            for possible_structure in blast[gene]:
                if length < possible_structure[3]: # change if find a new max length
                    start = possible_structure[1]
                    stop  = possible_structure[2]
            string += str(translation[gene][start-1:stop]) # add the gene translation into string
        size = len(string)
        string += '\n'
        # write the whole string to outfile
        outfile.write(string)
        outfile.write(str(size)+'\n')
    outfile.close()
    
retrieve_sequence_to_blast(blast,operon_list,operon, 'combination.fa')
