#!/usr/bin/env python
# -*- coding: utf-8 -*-


''' A partir de la sortie du mcl programme:
repartit les differents clusters en fonction du nombre de proteome presents
clusters avec tous les proteomes representes (conserves)
clusters avec au moins 2 proteomes et au plus n-1 avec n = nombre de proteomes (111 dans notre cas) (intermediaires)
cluster specifique avec un seul proteome represente (specifiques)


Parametres:

-i  proteome names (.list) file groups.txt -o [histogramme]


usage
==============
python cluster_repartition.py
'''

import os, sys,re
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def count_clusters(good_prot, proteomes_name, groups):
    ''''Description de la fonction' : renvoit 3 listes avec les nombres de clusters contenant des proteines conservees, intermediaires et specifiques
    '''
    with open (groups, 'r') as out_mcl, open (good_prot, 'r') as f:

        all_proteins       = set()
        my_ortho_cluster   = set()

        for ortho in out_mcl :

            ortho = ortho.rstrip()
            tmp = ortho.split()
            my_cluster = (tmp[1:])
            for names in my_cluster:
                my_ortho_cluster.add(names)

        for fasta in f:
            fasta = fasta.strip()
            if fasta.startswith('>'):
                name_protein = fasta[1:].split()[0]
                all_proteins.add(name_protein)

        singleton = all_proteins - my_ortho_cluster

        # Format des singleton idem que celui d'orthomcl pour fichier de sortie (loop optionnel)
        # specifiq = set()
        # singleton=list(singleton)
        # for seq_id in range(len(singleton)):
        #     my_format = 'cyano'+str(seq_id)+': '+str(singleton[seq_id])
        #     specifiq.add(my_format)


        singleton = list(singleton)
        prot_spec=[]

        cluster_all, cluster_inter, cluster_spec, cluster_spec_single = [0]*len(proteomes_name), [0]*len(proteomes_name), [0]*len(proteomes_name), [0]*len(proteomes_name)

        for names in singleton:
            tmpr_sing = names.split('|')
            proteome_single = tmpr_sing[0]
            protein  = tmpr_sing[1]
            pos_sing = proteomes_name.index(proteome_single)
            prot_spec.append(proteome_single)
            cluster_spec[pos_sing]+=1


        with open (groups, 'r') as clusters:

            nb_cluster=0
            for line in clusters:
                line = line.rstrip()
                tmp = line.split()
                my_cluster = (tmp[1:])
                cluster_id = tmp[0]
                nb_cluster+=1

                dico_proteome_name = {}

                for names in my_cluster:
                    tmpr = names.split('|')
                    proteome = tmpr[0]
                    protein  = tmpr[1]

                    if proteome in dico_proteome_name:
                        dico_proteome_name[proteome]+=1
                    else:
                        dico_proteome_name[proteome]=1
                for proteome in dico_proteome_name:
                    for pos, item in enumerate(proteomes_name):
                        if item == proteome:
                            if len(dico_proteome_name)==1:
                                cluster_spec[pos]+= dico_proteome_name[proteome]
                            if len(dico_proteome_name) >= len(proteomes_name):
                                cluster_all[pos]+=dico_proteome_name[proteome]
                            else:
                                cluster_inter[pos]+=dico_proteome_name[proteome]


        return cluster_all, cluster_inter, cluster_spec


def plotting (my_list_name, cluster_all, cluster_inter, cluster_spec):

    ''''Description de la fonction' : renvoit un histogramme superpose aux nombres de clusters avec des proteines conservees intermediaires et specifiqies
    '''
    label_names=[]
    for seq_id, seq_name in my_list_name:
        label_names.append(seq_name)
        # print(seq_id)
    print(len(label_names), ' = label_names')
    fig, ax = plt.subplots()
    N = len(label_names)
    ind = np.arange(N)
    width = 0.35


    dom = ax.bar(ind, cluster_all, width=0.6, alpha=0.6, color='b')#, label= 'Proteines conservees')
    # dom = ax.bar(ind, cluster_inter, bottom=cluster_all, width=0.7, alpha=0.6, color='grey')#, label= 'intermediaires')
    # bottom_spec = []
    # for x,y in zip(cluster_all,cluster_inter):
    #     z=x+y
    #     bottom_spec.append(z)
    # dom = ax.bar(ind, cluster_spec, bottom=bottom_spec, width=0.7, alpha=0.7, color='grey')#, label= 'specifiques')
    # all_values=[]
    # for x,y in zip(bottom_spec,cluster_spec):
    #     z=x+y
    #     all_values.append(z)
    ax.set_xlim(-width,len(ind)+width)
    ax.set_xticks(ind+width)
    ax.set_xticklabels (label_names, rotation='vertical', fontsize=10)
    # # for name in ax.set_xticklabels(proteomes_name, rotation= 'vertical', fontsize=10):
    #     if re.search('Synechococcus_sp_PCC_6312', str(name)) :
    #         name.set_color('green')
    #     elif re.search('Synechococcus_calcipolaris' , str(name)):
    #         name.set_color('green')
    #     elif re.search('Thermosynechococcus_elongatus_BP1' , str(name)):
    #         name.set_color('green')
    #
    #
    #     elif re.search('Gloeomargarita_lithophora' , str(name)):
    #         name.set_color('red')
    #     elif  re.search ('Cyanothece_sp_PCC_7425', str(name)):
    #         name.set_color('red')
    #     elif  re.search ('Chroococcidiopsis_thermalis_PCC_7203', str(name)):
    #         name.set_color('red')
    plt.grid(True)
    plt.ylabel('Nombre de proteines', fontsize=15, color='k', alpha=0.8)
    plt.xlabel('Proteomes', fontsize=15, color='k', alpha=0.8)
    # ax.set_ylim(0,500)
    for a,b in zip(ind,cluster_all):
        plt.text(a, b, str(b), va='bottom',fontsize=10, rotation='vertical', fontdict={'family': 'serif', 'color':  'r', 'weight': 'normal','size': 16})
    plt.title(u"Le nombre de proteines total/proteome dans les clusters conserves", fontsize=17, fontdict={'family': 'monospace'})
    # ax.legend(loc='upper left', fontsize=10)
    plt.show()

#
def give_full_name(full_names, proteomes_name):
    ''''Description de la fonction' : retransforme les noms des Proteomes (sous format lisible par orthomcl) aux noms complets initiaux
    '''

    proteomes_name= [thermalis.replace('C_thermalis7203','C_7203') for thermalis in proteomes_name]
    match_name={}
    for filename in full_names:
        if filename.endswith('.fasta'):
          filename = filename.split('.')[0]
          match_name.setdefault(filename, '')
          sub_id = filename.split('_')
          identifiant = sub_id[0][0]+'_'+sub_id[-1]
          match_name[filename]=identifiant
        #   print(filename , identifiant)
    my_list_name=[]
    for name in match_name:
        my_id= match_name[name]
        if my_id in proteomes_name:
            pos = (my_id, name)
            my_list_name.append(pos)
    return my_list_name

#
#
#
if __name__ == '__main__':

    proteome_dir = '/home/issa/Documents/stage/init_data/proteomes/'
    full_names = os.listdir(proteome_dir)
    good_prot = '/home/issa/Documents/stage/orthomcl/orthomcl_results/goodProteins.fasta'
    groups = '/home/issa/Documents/stage/orthomcl/orthomcl_results/groups.txt'

    directory = '/home/issa/Documents/stage/orthomcl/proteomes_format/'
    liste_fasta = os.listdir(directory)

    proteomes_name=[]

    for filename in liste_fasta:
        if filename.endswith('.fasta'):
            proteome_name = filename.split('.')[0]
            proteomes_name.append(proteome_name)


    core, inter, spec = count_clusters(good_prot,proteomes_name, groups)
    liste_names = give_full_name(full_names, proteomes_name)
    my_plot= plotting(liste_names, core, inter, spec)