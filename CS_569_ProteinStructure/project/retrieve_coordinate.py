Skip to content
Personal Open source Business Explore
Sign upSign inPricingBlogSupport
This repository
Search
 Watch 2  Star 0  Fork 0 nguyenngochuy91/class_projects
 Code  Issues 0  Pull requests 0  Projects 0  Pulse  Graphs
Branch: master Find file Copy pathclass_projects/CS_569_ProteinStructure/retrieve_coordinate.py
15d9512  40 seconds ago
@nguyenngochuy91 nguyenngochuy91 Add files via upload
1 contributor
RawBlameHistory    
113 lines (106 sloc)  3.84 KB
#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : using info from the blast, retrieve the coordination of the sequence
                of nucleotide that best matches the gene
'''
from Bio.PDB.PDBParser import PDBParser
pdb_dic = 'pdb/'
'''
    function: take in a blast file, file the best matching between a gene and 
                an available pdb file
    input: blast file
    output: dic (key: gene name, value: tuple (pdb file name, start ,stop,length))
'''
def get_best_match_gene_pdb(blast):
    infile = open(blast,'r')
    dic ={}
    for line in infile.readlines():
        line = line.strip()
        line = line.split('\t')
        pdb_info = line[0].split('|')[0]
        gene_info = line[1].split('|')[3]
        start = int(line[7])
        stop = int(line[9])
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
            structure = parser.get_structure(filename,pdb_dic+filename+'.pdb')
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
    

'''
    function: pfrom the operon, figure out which operon has all of its gene matching
                with a pdb file
    input:  dic (key: operon name, value: genes),dic (key: gene name, value: list of residues (which contain info about coordinate
             inside))
    output: list (operon name that has all of its gene mapped)
'''
def get_all_map(operon,coordinates):
    operon_list =[]
    for operon_name,genes in operon.items():
        flag = True
        for gene in genes:
            if gene not in coordinates:
                flag= False
                break
        if flag:
            operon_list.append(operon_name)
    return operon_list

blast = get_best_match_gene_pdb('output_reverse')  
coordinates = get_coordinate(blast)   
operon = get_operon_genes('gene_block_names_and_genes.txt')

