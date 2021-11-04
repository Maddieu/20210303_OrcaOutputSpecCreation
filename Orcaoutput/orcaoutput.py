"""

this file is old and not used anymore

look into orcaoutput2.py


"""



import numpy as np
import os
import readspectrum
from Classfile import Spectrumclass
from matplotlib import pyplot as plt



folder_with_output_file = r'D:\OrcaData\20210301_Martin_DyCp2_FreqSpecPbe0'
folder_with_output_file = r'D:\OrcaData\20210223_Martin_DyCp2_spec'
folder_with_output_file = r'D:\OrcaData\20210225_Olesya_Mn2O4_groundstate - PBE0'
#folder_with_output_file = r'D:\OrcaData\20210226_Olesya_Mn2O3_PBE0'

folder_with_output_file = r'D:\OrcaData\20211022_MT_DyCp_specC_slowSCF_Roots800'

number_of_most_intense_analyzed_sticks = 20


label = '_' + '20211026_px-py_over6'

transitioncheck_dictionary = {}

#transitioncheck_dictionary['restrict_donor_orbitals_spinup'] = [10, 13]
#transitioncheck_dictionary['restrict_donor_orbitals_spindown'] = [10, 13]
transitioncheck_dictionary['restrict_donor_orbitals_spinup'] = range(18, 27+1)
transitioncheck_dictionary['restrict_donor_orbitals_spindown'] = range(18, 27+1)

#transitioncheck_dictionary['restrict_acceptor_orbitals_spinup'] = range(40,46+1)
#transitioncheck_dictionary['restrict_acceptor_orbitals_spindown'] = range(40,46+1)
#transitioncheck_dictionary['restrict_acceptor_orbitals_spinup'] = [73, 74]
#transitioncheck_dictionary['restrict_acceptor_orbitals_spindown'] = [75, 78]

#transitioncheck_dictionary['restrict_acceptor_orbitals_spinup'] = [71, 72, 73, 74, 79, 82, 84, 85, 87, 88, 89, 94]     # 2021 10 26 - pz / thresh 10
#transitioncheck_dictionary['restrict_acceptor_orbitals_spindown'] = [69, 70, 73, 76, 79, 84, 85, 86, 87, 88, 89, 95]

templist1 = list(set([75, 90, 92, 96, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 110, 111, 112, 113, 114, 115
]) | set([73, 75, 91, 92, 93, 98, 99, 101, 102, 103, 104, 105, 106, 107, 108, 110, 111, 112, 113, 114, 115, 116
])) # spin down, px and py orbitals > 6 % Loewdin nature
templist2 = list(set([90, 92, 96, 98, 99, 101, 102, 103, 104, 105, 106, 107, 108, 110, 111, 112, 113, 114, 115, 116
]) | set([73, 74, 79, 91, 92, 93, 98, 99, 101, 102, 103, 104, 105, 106, 107, 108, 110, 111, 112, 113, 114, 116])) #spin up px, py

transitioncheck_dictionary['restrict_acceptor_orbitals_spinup'] = templist2    # 2021 10 26 - px/py / thresh 6
transitioncheck_dictionary['restrict_acceptor_orbitals_spindown'] = templist1


transitioncheck_dictionary['restrict_acceptor_orbitals_spinup'] = range(60,110)    # 2021 10 26 - px/py / thresh 6
transitioncheck_dictionary['restrict_acceptor_orbitals_spindown'] = range(60,110)


transitioncheck_dictionary['number_of_analysis'] = number_of_most_intense_analyzed_sticks




#
#read the output file and initialize the spectrum here
#

spectrum = Spectrumclass(folder_with_output_file)





#print(spectrum.maxintensity())
#print(spectrum.number_of_sticks())


for element in spectrum.return_transition(1):
    print(element, end="")
    pass

print('')


for element in spectrum.return_most_intense_transitions(number_of_most_intense_analyzed_sticks):
    print(element)
    pass

print('')


#print(spectrum.return_list_of_tuple())





partial_spectrum = spectrum.checktransitions(transitioncheck_dictionary)

for element in partial_spectrum:
    if (element['donor'] == '12b') and (element['acceptor'] == '36b'):
        print(element)




x = [i['Energy'] for i in partial_spectrum]
y = [i['Intensity'] for i in partial_spectrum]






with open(f'outputfolder\output{label}.txt', 'w') as file:
    file.write('# ' + folder_with_output_file + '\n')
    file.write(f'reduced_orbitals{label}_Energie\treduced_orbitals{label}_Normiert\n')
    for element in zip(x, y):
        file.write(str(element[0]) + '\t' + str(element[1]) + '\n')










def broaden_spectrum(E,osc,sigma,x):
    gE=[]
    for Ei in x:
        tot=0
        for Ej,os in zip(E,osc):
            tot+=os*np.exp(-((((Ej-Ei)/sigma)**2)))
        gE.append(tot)
    return gE

broadened_axis = np.linspace(min(spectrum.energy())-2,max(spectrum.energy())+2, num=1000, endpoint=True)
sigma = 0.4
gE = broaden_spectrum(x,y,sigma,broadened_axis)





plt.close()
plt.plot(broadened_axis, gE, "--k")
plt.stem(x, y, markerfmt=' ', basefmt=None)
plt.title(folder_with_output_file)

plt.annotate(str(transitioncheck_dictionary), xy=(0.6, 0.85), xycoords='axes fraction', wrap=True, fontsize=6)
# plt.text(0.5, 0.5, str(transitioncheck_dictionary), # transform=ax.transAxes)
plt.show()
