#This concatenates shortbred output files. To work, files have to be in the same folder and be of one marker type and ending with 'out.txt'
#It creates separte outputs by specified sample group, and defaults to 'other' if it can't classify
#Nov 2019

#!/usr/bin/env python3
import os

control=['1084','1143','7260','1603','6347']
treated=['6890','7830','1195','385','4130']
untreated=['3908','3482','4804','536']

def sampleid(var1):
	var1 = var1.split('_')
	if var1[0][0].isdigit() == True: return (var1[0])
	elif var1[0][0] == 'K': return (var1[0])
	else:
		try: 
			var2 = var1[0].split('.')
			return (var2[1])
		except: return (None)

def sum(dict,l,f):
    l = l.strip('\n')
    l = l.split()
    if l[0] in dict.keys():
        dict[l[0]] += [float(l[1]), int(l[2])]
        if dict[l[0]][0] != l[3] : print ('Flag: Missmacth size match (likely mixed up input files): ', l[0], '\t', f)
    else:
        dict[l[0]] = [l[3],float(l[1]),int(l[2])]

def save(savename, data):
    if len(data['sample_name']) < 2 :return()
    wr = open(savename + '_combined.txt','w')
    for key, value in sorted (data.items()):
        line = key
        for i in range(len(value)):
            line += '\t' + str(value[i])
        line += '\n'
        wr.write(line)
    f.close()
    print ('Output : \'' + savename + '_combined.txt\'')

control_markers = {'sample_name' : [''], 'first_line': ['']}
treated_markers = {'sample_name': [''], 'first_line': ['']}
untreated_markers = {'sample_name' : [''], 'first_line': ['']}
kitneg_markers = {'sample_name' : [''], 'first_line': ['']}
other_markers = {'sample_name': [''], 'first_line': ['']}

files = [file.name for file in os.scandir() if file.is_file and file.path.endswith('out.txt')]
for file in files:
	sample = sampleid(file)
	f = open(file, 'r')
	fl = f.readline()
	fl = fl.split()
	if sample != None and sample.find('Neg') != -1:
		kitneg_markers['sample_name'] += [file, file]
		kitneg_markers['first_line'] += [fl[1], fl[2]]
		for line in f: sum(kitneg_markers, line, file)
	elif sample in control:
		control_markers['sample_name'] += [file, file]
		control_markers['first_line'] += [fl[1], fl[2]]
		for line in f: sum(control_markers, line, file)
	elif sample in treated:
		treated_markers['sample_name'] += [file, file]
		treated_markers['first_line'] += [fl[1], fl[2]]
		for line in f: sum(treated_markers, line, file)
	elif sample in untreated:
		untreated_markers['sample_name'] += [file, file]
		untreated_markers['first_line'] += [fl[1], fl[2]]
		for line in f: sum(untreated_markers, line, file)
	else:
		other_markers['sample_name'] += [file, file]
		other_markers['first_line'] += [fl[1], fl[2]]
		for line in f: sum(other_markers, line, file)

dicts={'control_markers': control_markers, 'treated_markers' : treated_markers, 'untreated_markers': untreated_markers, 'kitneg_markers': kitneg_markers, 'other_markers': other_markers}
for keys,values in dicts.items(): save(keys,values)
print (os.getcwd())
