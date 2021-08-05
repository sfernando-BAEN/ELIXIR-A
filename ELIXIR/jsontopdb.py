#!/usr/bin/env python
# coding: utf-8

# In[84]:


import json
from biopandas.pdb import PandasPdb


# In[85]:


def jsontonp(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    listdata=[]
    for point in range(len(data['points'])):
        if data['points'][point]['enabled']:
            tmp=data['points'][point]
            listdata.append([tmp['name'],
                           tmp['radius'],
                          [tmp['x'],
                          tmp['y'],
                          tmp['z']]])
    return listdata
        


# In[125]:


def shortcuts(fullname):
    fulllist=['HydrogenDonor',
             'HydrogenAcceptor',
             'Hydrophobic',
             'PositiveIon',
             'NegativeIon',
             'Aromatic']
    shortlist=['HDR','HAC','HPB','PIO','NIO','ARO']
    for i in range(len(fulllist)):
        if fullname==fulllist[i]:
            return shortlist[i]
    return 'DEF'


# In[250]:


def exportpdbdata(filename):
    jsondata=jsontonp(filename)
    linepdb=[]
    for index in range(len(jsondata)):
        tmpstr='ATOM   '+' '*(4-len(str(index+1))) +str(index+1)+        '  CA  '+shortcuts(jsondata[index][0])+        ' A'+ ' '*(4-len(str(index+1))) + str(index+1)+'    '+        ' '*(8-len(str(round(jsondata[index][2][0],3)))) + str(round(jsondata[index][2][0],3))+        ' '*(8-len(str(round(jsondata[index][2][1],3)))) + str(round(jsondata[index][2][1],3))+        ' '*(8-len(str(round(jsondata[index][2][2],3)))) + str(round(jsondata[index][2][2],3))+        ' '*(6-len(str(jsondata[index][1]))) + str(jsondata[index][1]) +        str(' 00.00') + '            C  \n' 
        linepdb.append(tmpstr)
    ppdb2 = PandasPdb()
    ppdb2.read_pdb_from_list(linepdb)
    ppdb2.to_pdb(path=filename+'.pdb', 
                records=None, 
                gz=False, 
                append_newline=True)


# In[251]:





# In[ ]:




