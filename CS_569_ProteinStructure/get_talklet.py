#!/usr/bin/env python
''' Author  : Huy Nguyen
    Program : Quick program to download web talklet for lecture
    Start   : 08/26/2016
    End     : 08/27/2016
'''

import argparse
from bs4 import BeautifulSoup
from urllib.request import urlopen # for python2  use from urllib2 import urlopen 
import os
import time # to sleep to wait for the opening of browser and load the swf file



#global variable
# hardcode dictionary that map error name to right name (a pain)
dic ={
    '1':
        {'The_Cycle_of_Life':'Cycle_of_Life',
         # 'Structural_Overview_of_Biology':'Structural_Overview_Of_Biology',
         # 'Informatics_Overview_of_Biology':'Informatics_Overview_Of_Biology',
         'Informatics_Overview_of_Biology':'Informatics_Overview',
         'Cellular_Cities':'Cellular_Citties', #the alternate root need this
         'The_Core_Machinery_of_Life':'Core_Machinery_of_Life',
         #'Drug_Binding_to_Receptor':'Drug_Binding_to_Receptor',
         #'Fibrous_Proteins_in_Disease':'Fibrous_Proteins_In_Disease',
         #'Protein_in_Water':'Protein_In_Water',
#         'See_the_Protein_alone':'See_The_Protein_Alone',
#         'See_the_Bonded_Atoms':'See_The_Bonded_Atoms',
         'Fundamental_interactions':'Fundamental_Interactions',
         'Try_to_See_the_Main_Chain_1':'Try_to_See_Mainchain_1',
         'Try_to_See_the_Main_Chain_2':'Try_to_See_Mainchain_2',
         'Try_to_See_the_Main_Chain_3':'Try_to_See_Mainchain_3',
         'Try_to_See_the_Chain_Path':'Try_to_See_Chain_Path',
         'What_is_An_Atom':'What_Is_An_Atom',
         'What_is_a_Molecule':'What_Is_A_Molecule',
         'Van_Der_Waals_interaction':'Van_Der_Waals_Interaction',
         'Electrostatics_interaction':'Electrostatics_Interaction',
         'Forces_Between_atoms':'Forces_Between_Atoms',
         'Bond_angle_Bending':'Bond_Angle_Bending',
         'Water_Energy_and_Dipole':'Water_Energy_And_Dipole',
         'Units_in_Force_Fields':'Units_In_Force_Fields',
         'Explaining_the_Dielectric_Effect':'Explaining_The_Dielectric_Effect',
         'Energy_and_Springs_1':'Energy_And_Springs_1',
         'Energy_and_Springs_2':'Energy_And_Springs_2',
         'Strength_of_Interactions':'Strength_Of_Interactions',
         'Complex_interactions':'Complex_Interactions',
         'Liquids_argon_and_Water':'Liquids_Argon_and_Water',
         'Useful_tools':'Useful_Tools',
         'See_the_Protein_Alone':'See_Protein_Alone',
         'See_the_Bonded_Atoms':'See_Bonded_Atoms'},
    '2':
        {'Amino_Acids_Gly_and_Pro':'Amino_Acids_Gly_And_Pro',
         'Amino_Acids_Leu_and_Phe':'Amino_Acids_Leu_And_Phe',
         'Amino_Acids_Glu_and_Arg':'Amino_Acids_Glu_And_Arg',
         'Amino_Acids_Val_and_Ile':'Amino_Acids_Val_And_Ile',
         'Degrees_of_Freedom._Concept_2.3':'Degrees_Of_Freedom._Concept_2.3',
         'Degrees_of_Freedom':'Degrees_Of_Freedom',
         'Backbone_Degrees_of_Freedom':'Backbone_Degrees_Of_Freedom',
         'The_Alpha_Heli':'The_Alpha_Helix_',
         'Beta_Sheet':'Beta_Sheets_'},
     '3':
         {'Cath_the_Numbers':'Cath_The_Numbers',
          'Alpha-Helix_and_Beta-Sheet':'Alpha-Helix_And_Beta-Sheet',
          'Cath_Drill_Down_to_a_Level':'Cath_Drill_Down_to_A_Level'},
     '4':
         {'Entropy_and_Free_Energy1':'Entropy_and_Free_Energy',
          'Simulated_annealing':'Simulated_Annealing',
          'Molecular_Dynamics_theory':'Molecular_Dynamics_Theory',
          'Liquids_argon_and_Water':'Liquids_Argon_and_Water',
          'Voronoi_analysis_of_Contacts':'Voronoi_Analysis_of_Contacts',
          'Simulating_alpha-Helix.__Concept_4.5':'Simulating_Alpha-Helix.__Concept_4.5',
          'Dynamics_of_the_alpha-Helix':'Dynamics_of_the_Alpha-Helix',
          'Water_allows_Hydrogen_Bonds_to_Break':'Water_Allows_Hydrogen_Bonds_to_Break',
          'Los_alamos_1943-45':'Los_alamos_1943-45',
          'Units_in_Force_Fields':'Units_In_Force_Fields',
          'Los_alamos_1943-45':'Los_Alamos_1943-45'},
     '5':
         {'Normal_Mode_theory._Concept_5.1':'Normal_Mode_Theory.__Concept_5.1',
          'Basic_theory':'Basic_Theory',
          'Potential_Energy_in_torsion_Space':'Potential_Energy_in_Torsion_Space',
          'Trypsin_inhibitor_Modes':'Trypsin_Inhibitor_Modes',
          'Unfolding_alpha_Helix.__Concept_5.3':'Unfolding_Alpha_Helix.__Concept_5.3',
          'Unfold_alpha-Helix':'Unfold_Alpha-Helix',
          'Helix_Less_Stable_in_Water':'Helix_Less_Stable_In_Water',
          'Water_allows_Hydrogen_Bonds_to_Break':'Water_Allows_Hydrogen_Bonds_to_Break',
          'What_Happens_to_aromatic_Sidechains':'What_Happens_to_Aromatic_Sidechains',
          'Why_is_Folding_So_Difficult':'Why_Is_Folding_So_Difficult',
          'Folding_at_Home_Rates':'Folding_at_Home_Rates'      
         },
     '6':{},
     '7':{},
     '8':{},
     '9':{}
          }
      
         
     
constant = 'Lecture'
apps = 'talklets'
root ='http://csb.stanford.edu/class/public/lectures/'
alter_root = 'http://www.stanford.edu/class/sbio228/public/lectures/' # in case the other sever is down

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lecture","-l",help="Which lecture to download (1-6)")
    args = parser.parse_args()
    return args

'''@function: given the lecture name, parse the website to retrieve the name of each talklet slide
   @input   : int (lecture number)
   @output  : list (talklets website in numeric order)
'''   
def parse_web(lecture):
    if lecture =='4':
        URL = root+constant+lecture+'/'
    else:
        URL = alter_root+constant+lecture+'/'
    print (URL)
    # open the url as url using url package, then use Beautiful soup to parse the website
    soup = BeautifulSoup(urlopen(URL))
    # print (soup)
    # get the text
    text = soup.text
    my_list = text.split('\n')
    # filter out the empty items 
    new_list = list(filter(None,my_list))
    # do some trick to remove not important partas well as storing information 
    # information to be stored: each section name of the chapter
    # for each section, store the name of the slide. Use those 2 information
    # in order to provide a full http link and append it into a list
    
    # list of link to download
    links =[]
    # chapter name
    # list of section names
    sections =[] # will use the length of the section to tell whether we go through
                 # all slides of a section already (since new slide starts with 'Fundamental interactions.  Concept 1.4')   
    count = 0
    while count <len(new_list):
        if new_list[count] != 'CONCEPTS IN THIS LECTURE':
            count +=1
            continue
        else:
            # get the chapter name and break here
            chapter = new_list[count+1]
            count +=2 # plus 2 so it get over the index at the chapter name
            break
    # print (new_list)
    #using chapter as a mark to do sections
    while chapter not in new_list[count]: 
        sections.append(new_list[count])
        count +=1
    count +=1 # increase to get over the second time it hits the chapter name
    while count < len(new_list):
        
        # print (new_list[count])
        if new_list[count][:2] == (lecture+'.') or (constant+' '+lecture) in new_list[count] or chapter in new_list[count]: #basically check if it is the section name, then ignore it
            count +=1
            continue
        else: # i basically ignore those 2 slides 'SB228 Lecture 2 Lecture2', 'Lecture 2 Contents'
            if new_list[count][-11:-2] == ('Concept '+lecture):
                section_index = int(new_list[count][-1])-1
                section = sections[section_index]
                # create a link to add to links
                # if it is lecture 1 then skip this part 
                chapter_link = URL + constant + lecture+'/'+ section.replace(' ','_')+'/'+apps+'/'
                if lecture =='1':
                    count +=1
                    continue
            modify = new_list[count].replace(' ','_')
            if modify in dic[lecture]:
                link = chapter_link + dic[lecture][modify]+'.swf'
            else:
                link = chapter_link + modify+'.swf'
            links.append(link)
            count +=1
        
    return links



'''@function: Given list of website link, download the video
   @input   : list,and lecture number
   @output  : make a dir with lecture name, download all the video into that file
'''   
def down_video(links,lecture):
    my_dir = './lecture'+lecture+'/'
    os.mkdir(my_dir)
    count = 0
    short = 4
    long = 6
    if lecture == '4':
        amount = long
    else:
        amount = short
    for link in links:
        count +=1
        # open the browser to load the swf file:
        cmd1= 'open '+link
        os.system(cmd1)
        time.sleep(amount)
        cmd2 ='curl -o '+my_dir+'part'+str(count)+'.swf'+' '+link
        os.system(cmd2)
        time.sleep(3)

###############################################################################
# execute the main program
###############################################################################
if __name__ == "__main__":

    args    = get_arguments()
    lecture = args.lecture
    print (lecture)
    links= parse_web(lecture)
    down_video(links,lecture)
