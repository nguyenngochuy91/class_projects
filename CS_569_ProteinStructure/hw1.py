#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : HW1
    Start   : 08//2016
    End     : 08//2016
'''
import numpy
backbone =['N','CA','C']
'''@function: parse in pdb file
   @input   : text file
   @output  : dictionary (key: protein, value ( dictionary (key: backbone or residue, value : coordinate)))
'''   
###############################################################################
## 1 retrieve the coordinates of the backbone atoms
###############################################################################
def parse(myfile):
    dic ={}
    infile = open(myfile,'r')
    for line in infile.readlines():
        if line[:4] == 'ATOM':
            polypeptide = int(line[22:26] )
            atom = line[12:16]
            atom = atom.replace(' ','')
            # print (atom)
            if polypeptide not in dic:
                dic[polypeptide]={}
            x = line[30:38]
            y = line[38:46]
            z = line[46:54]
            dic[polypeptide][atom] = [float(x),float(y),float(z)]
    return dic
'''@function: write string to print
   @input   : name, coordinate
   @output  : string
'''       
def to_string_cordinate(name,coordinates):
    for coordinate in coordinates:
        name += '\t' + str(coordinate)
    name += '\t'
    return name
'''@function: write out result
   @input   : fileout,dic
   @output  : text
'''   
def ques1_write(fileout,dic):
    for polypeptide in dic:
        # writing N
        fileout.write(str(polypeptide)+':\t')
        fileout.write(to_string_cordinate('N',dic[polypeptide]['N']))
        fileout.write(to_string_cordinate('CA',dic[polypeptide]['CA']))
        fileout.write(to_string_cordinate('C',dic[polypeptide]['C']))
        fileout.write('\n')
        # writing CA
        # writing C
###############################################################################
## 2a bond lengths
###############################################################################
'''@function: provide bond length for an edge
   @input   : 2 atoms coordinates
   @output  : float 
'''      
def get_length(coordinate1, coordinate2):
    value = 0
    for item in range(3):
        value += (coordinate2[item]-coordinate1[item])**2
    return (value)**.5
'''@function: provide bond lengths
   @input   : dic
   @output  : mean, standard deviation 
'''       
def bond_length(dic):
    edges = []
    for polypeptide in dic:
        edges.append(get_length(dic[polypeptide]['N'],dic[polypeptide]['CA']))
        edges.append(get_length(dic[polypeptide]['CA'],dic[polypeptide]['C']))
        try:
            edges.append(get_length(dic[polypeptide]['C'],dic[polypeptide+1]['N']))
        except:
            continue
    return numpy.mean(edges),numpy.std(edges)
###############################################################################
## 2b bond angles
###############################################################################
'''@function: provide bond angle for a triple cordinates 
            Using the low of consines: 
            c**2 = a**2 + b**2 -2ab. cos c
   @input   : 3 atoms coordinates
   @output  : degree 
'''      
def get_angle(coordinate1, coordinate2,coordinate3):
    a = get_length(coordinate1, coordinate2)
    b = get_length(coordinate2, coordinate3)
    c = get_length(coordinate3, coordinate1)
    value = (a**2 + b**2 - c**2)/(2*a*b)
    degree = numpy.arccos(value)
    return (degree*180/numpy.pi)

'''@function: provide bond lengths
   @input   : dic
   @output  : mean, standard deviation 
'''       
def bond_angle(dic):
    angles = []
    for polypeptide in dic:
        angles.append(get_angle(dic[polypeptide]['N'],dic[polypeptide]['CA'],dic[polypeptide]['C']))
        try:
            angles.append(get_angle(dic[polypeptide]['CA'],dic[polypeptide]['C'],dic[polypeptide+1]['N']))
        except:
            continue
        try:
            angles.append(get_angle(dic[polypeptide][''],dic[polypeptide+1]['N'],dic[polypeptide+1]['CA']))
        except:
            continue
    return numpy.mean(angles),numpy.std(angles)
###############################################################################
## 2c distance between adjacent CAs
###############################################################################    
'''@function: provide bond lengths
   @input   : dic
   @output  : mean, standard deviation 
'''       
def adjacent_CA_length(dic):
    edges = []
    for polypeptide in dic:
        try:
            edges.append(get_length(dic[polypeptide]['CA'],dic[polypeptide+1]['CA']))
        except:
            continue
    return numpy.mean(edges),numpy.std(edges)  
###############################################################################
## 3 torsional angles: phi, psi, and omega
############################################################################### 
'''@function: given 3 pairs of cordinates, find the plane they are in using
                vector and cross product:
                vector AB x vector AC = (a,b,c)
   @input   : 3 atoms coordinates
   @output  : plane (ax+by+cz+d=0), given by a,b,c,d as float numbers
''' 
def get_plane(coordinate1, coordinate2,coordinate3):
    # set up the matrices
    A = [coordinate1[0],coordinate1[1],coordinate1[2]]
    B = [coordinate2[0],coordinate2[1],coordinate2[2]]
    C = [coordinate3[0],coordinate3[1],coordinate3[2]]
    # calculation
    a = (B[1]-A[1])*(C[2]-A[2]) - (C[1]-A[1])*(B[2]-A[2])
    b = (B[0]-A[0])*(C[2]-A[2]) - (C[0]-A[0])*(B[2]-A[2])
    c = (B[1]-A[1])*(C[0]-A[0]) - (C[1]-A[1])*(B[0]-A[0])
    d = - (a*A[0] + b*B[0] +c*C[0])
    return (a,b,c,d)
    
'''@function: given 2 plane coefficient, compute the angle between the plane using
            dihedral angle cosine formula 
   @input   : 2 plan coefficient in 2 array
   @output  : angle
''' 
def get_planes_angle(plane1,plane2):
    numerator = (plane1[0]*plane2[0]+plane1[1]*plane2[1]+plane1[2]*plane2[2])
    denominator = ((plane1[0]**2+plane1[1]**2+plane1[2]**2)*(plane2[0]**2+plane2[1]**2+plane2[2]**2))**.5
    cos_angle = numerator/denominator
    degree = numpy.arccos(cos_angle)
    return (degree*180/numpy.pi)
    
'''@function: provide torsion angles given the residue/ polipeptide number n
            phi = (C_n-1,N_n,CA_n,C_n)
            psi = (N_n,CA_n,C_n,N_n+1)
            omega = (CA_n-1,C_n-1,N_n,CA_n)
   @input   : dic
   @output  : 3 angles in degree phi, psi, omga
''' 
def get_torsion_angles(dic,n):
    phi_info   = [dic[n-1]['C'],dic[n]['N'],dic[n]['CA'],dic[n]['C']]
    psi_info   = [dic[n]['N'],dic[n]['CA'],dic[n]['C'],dic[n+1]['N']]
    omega_info = [dic[n-1]['CA'],dic[n-1]['C'],dic[n]['N'],dic[n]['CA']]
    # print ('omega_info',omega_info)
    # print ('plane1',get_plane(omega_info[0],omega_info[1],omega_info[2]))
    phi = get_planes_angle(get_plane(phi_info[0],phi_info[1],phi_info[2]),
                           get_plane(phi_info[1],phi_info[2],phi_info[3]))
    psi = get_planes_angle(get_plane(psi_info[0],psi_info[1],psi_info[2]),
                           get_plane(psi_info[1],psi_info[2],psi_info[3]))
    omega = get_planes_angle(get_plane(omega_info[0],omega_info[1],omega_info[2]),
                           get_plane(omega_info[1],omega_info[2],omega_info[3])) 
    return phi,psi,omega

'''@function: given 3 coordinates A B C, find a candidate vector 
                CA' that is parallel to vector BA
   @input   : plane coefficient, 3 coordinates
   @output  : coordinate of point A'
'''
def get_parallel(coordinate1, coordinate2,coordinate3):
    vector_BA= []
    for index in range(3):
        vector_BA.append(coordinate2[index]-coordinate1[index])
    vector_CA =[]
    for index in range(3):
        vector_CA.append(vector_BA[index]+coordinate3[index])
    return vector_CA
    
    
'''@function: given 4 continous pairs of coordinates (A,B,C,D), get the torsion angle between
                (A,B,C) and (B,C,D)
              The idea is as follow:
              find coefficient of plane (A,B,C). Find point A' in (A,B,C) so that 
              vector CA' // vector BA. 
              From CA',CD, get the angle by using dot product.
   @input   : 4 coordinates
   @output  : torsion angle
''' 
def get_torsion_angle(coordinate1, coordinate2,coordinate3,coordinate4):
    vector12 = get_parallel(coordinate1, coordinate2,coordinate3)
    print ('vector12',vector12)
    vector34 = []
    dot_product = 0
    for index in range(3):
        vector34.append(coordinate4[index]-coordinate3[index])
        dot_product += (vector12[index]*vector34[index])
    print ('vector34',vector34)
    length12 = get_length(coordinate1,coordinate2)
    length34 = get_length(coordinate3,coordinate4)
    
    cos_angle = dot_product/length12/length34
    print (cos_angle)
    degree = numpy.arccos(cos_angle)
    return (degree*180/numpy.pi)
###############################################################################
## 4a Set both phi and psi angles of residue 30 (Phenylalanine) to 0 degree.
##    Recompute the coordinates of all the residues.
##    Use the new coordinates to replace the old and construct a new pdb file
############################################################################### 
'''@function: set phi and psi angles of residue 30 to 0 degree. This means that
            plane (C_n-1,N_n,CA_n) is same as plane (N_n,CA_n,C_n) and 
            plane (N_n,CA_n,C_n) is same as plane (CA_n,C_n,N_n+1)
            therefore, C_n-1,N_n,CA_n,C_n,N_n+1 are in the same plane.
            Consider keep the coordinate upto C_29, N_30. Then CA_30 coordinates 
            still stay the same. However, C_30,N_31 coordinate will change,
   @input   : dic
   @output  : dic (key: atom that changes coordinate in the back bone, value: new possible coordinates)
'''
def set_phi_0(dic):
    C_29 = dic[29]['C']
    N_30 = dic[30]['N']
    edge_C_29_N_30 = get_length(dic[29]['C'],dic[30]['N'])
    CA_30 = dic[30]['CA']
    C_30_old = dic[30]['C']
    edge_CA_30_C_30 = get_length(dic[30]['CA'],dic[30]['C'])
    N_31_old = dic[31]['N']
    # we check dot product of 
    C_29_N_30 = [N_30[0]-C_29[0],N_30[1]-C_29[1],N_30[2]-C_29[2]]

###############################################################################
## 4b Is there any steric clashing now
##    What is the minimum distance between atoms in the current structure
##    Identify the pair of atoms that have the minimum distance
##    
############################################################################### 

###############################################################################
## 5 Extend your program so that it can compute the side chain torsional angles 
##   Apply your program to 2GB1.pdb and output the side chain χ angles of each residue
############################################################################### 
dic = parse('2gb1.pdb')
fileout = open('output.txt','w')
##
fileout.write('Question 1: \n')
ques1_write(fileout,dic)
##
fileout.write('Question 2: \n')
mean_edge,std_edge = bond_length(dic)
fileout.write('a:\t mean: '+str(mean_edge)+'\t std: '+str(std_edge)+'\n')
mean_angle,std_angle = bond_angle(dic)
fileout.write('b:\t mean: '+str(mean_angle)+'\t std: '+str(std_angle)+'\n')
mean_CA,std_CA = adjacent_CA_length(dic)
fileout.write('c:\t mean: '+str(mean_CA)+'\t std: '+str(std_CA)+'\n')
##
fileout.write('Question 3: \n')
phi,psi,omega = get_torsion_angles(dic,30)
fileout.write('phi: '+str(phi)+'\t psi: '+str(psi)+'\t omega: '+str(omega)+'\n')
fileout.close()
##


                
