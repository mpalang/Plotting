# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 15:55:36 2022

@author: work
"""


def GIF(folderpath,extension='png',savename='movie'):
    import imageio
    from pathlib import Path
    from glob import glob
    from difflib import SequenceMatcher
    from re import findall
    
    folderpath='Z:/Nutzer/Lang/privat/02_Projekte/ESKIMO-Pro_IRON/Fe-PD312_PD310/Figures/Difference'
    extension='png'
    savename='movie'
    
    filenames=glob(str(Path(folderpath,'*.'+extension)))
    
    substring_counts={}
    
    for i in range(0, len(filenames)):
        for j in range(i+1,len(filenames)):
            string1 = filenames[i]
            string2 = filenames[j]
            match = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))
            matching_substring=string1[match.a:match.a+match.size]
            if(matching_substring not in substring_counts):
                substring_counts[matching_substring]=1
            else:
                substring_counts[matching_substring]+=1
    
    
    base_path=max(substring_counts, key=substring_counts.get)
    
    index=[]
    for n,i in enumerate(filenames):
        index.append(int(findall('[0-9]+',i.removeprefix(base_path))[0]))
    
    filenames_sorted=[None]*len(filenames)
    for n,i in enumerate(index):
        filenames_sorted[i]=filenames[n]
    
    images = []
    for filename in filenames_sorted:
        images.append(imageio.imread(filename))
    imageio.mimsave(Path(folderpath,savename+'.gif'), images)