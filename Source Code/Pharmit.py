#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Author: Haoqi Wang
"""

outputfile=['{\n', '    "points": [\n', '        {']

fragment1=['        {\n', '            "name": "\n', '            "hasvec": false,\n', '            "x":\n', '            "y":\n', '            "z":\n', '            "radius": 1,\n', '            "enabled": true,\n', '            "vector_on": 0,\n', '            "svector": {\n', '                "x": 1\n', '                "y": 0\n', '                "z": 0\n', '            },\n', '            "minsize": "",\n', '            "maxsize": "",\n', '            "selected": true\n', '        }']
fragment2=['    ],\n', '    "subset": "molport",\n', '    "ShapeModeSelect": "filter",\n', '    "inselect": "none",\n', '    "intolerance": 1,\n', '    "inshapestyle": "inshapestyle-solid",\n', '    "exselect": "none",\n', '    "extolerance": 1,\n', '    "exshapestyle": "exshapestyle-solid",\n', '    "max-orient": "",\n', '    "reduceConfs": "",\n', '    "max-hits": "",\n', '    "minMolWeight": "",\n', '    "maxMolWeight": "",\n', '    "minrotbonds": "",\n', '    "maxrotbonds": "",\n', '    "minlogp": "",\n', '    "maxlogp": "",\n', '    "minpsa": "",\n', '    "maxpsa": "",\n', '    "minaromatics": "",\n', '    "maxaromatics": "",\n', '    "minhba": "",\n', '    "maxhba": "",\n', '    "minhbd": "",\n', '    "maxhbd": "",\n', '    "LigandMolStyleSelect": "stick",\n', '    "LigandMolStyleSelectcolor": "#c8c8c8",\n', '    "ResultsMolStyleSelect": "stick",\n', '    "ResultsMolStyleSelectcolor": "#808080",\n', '    "ReceptorMolStyleSelect": "cartoonwire",\n', '    "ReceptorMolStyleSelectcolor": "#c8c8c8",\n', '    "receptorbackbone": "plainBackbone",\n', '    "surfaceopacity": 0.8,\n', '    "backgroundcolor": "whiteBackground",\n', '    "ligand": null,\n', '    "ligandFormat": null,\n', '    "receptor": null,\n', '    "recname": null,\n', '    "receptorid": null,\n', '    "view": [\n', '        0,\n', '        0,\n', '        0,\n', '        18.873262406249992,\n', '        0.6300778787272721,\n', '        0.08411783594121802,\n', '        0,\n', '        -0.7719624708592429\n', '    ]\n', '}']

f=fragment1
f[1]+=pA0[Sori[i],1] + "\""
f[3]+=str(round(tmpA,3)) + ","
f[4]+=str(round(tmpA,4)) + ","
f[5]+=str(round(tmpA,5)) + ","

# with open("fragment1.txt") as file:
#     f=file.readlines()
#     f[1]+=pA0[Sori[i],1] + "\""
#     f[3]+=str(round(tmpA,3)) + ","
#     f[4]+=str(round(tmpA,4)) + ","
#     f[5]+=str(round(tmpA,5)) + ","
#
#     for j in range(len(f)):
#         outputfile.append(f[j])

#
#
# if outputfile[-1]=="},\n":
#     outputfile[-1] == "}\n"
# with open("fragment2.txt") as file:
#     f=file.readlines()
#     for i in f:
#         outputfile.append(i)
