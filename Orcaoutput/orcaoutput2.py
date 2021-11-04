import numpy as np
import os
import readspectrum
from Classfile import Spectrumclass
from matplotlib import pyplot as plt

import shutil

sigma = 0.3 # broadening for spectrum export

folder_with_output_file = r'D:\OrcaData\20211027_MT_DyCp_specC_slowSCF_Roots1400_ompiotest'
folder_with_output_file = r'D:\OrcaData\20211011_Olesya_Mn4O4_PBE0_tightenedSCF'

folder_with_output_file = os.getcwd()
os.chdir(folder_with_output_file)

try:
    shutil.rmtree('outputfolder')
    print('deleted outputfolder')
except Exception as err:
    print(err)
    print('no "outputfolder" to delete.')
try:
    os.mkdir('outputfolder')
    print('outputfolder successfully created')
except Exception as err:
    print(err)
    print('could not create output folder.')


transitioncheck_dictionary = {}



number_of_most_intense_analyzed_sticks = 20 # I think this is not used anywhere?



"""
create the spectrum object of the class "Spectrumclass"
- in the cwd, look for an .out file
- read this .out file into "content"
- extract from this content:
-- the "spectrum": intensity vs energy for a stick
-- the nature of this transition: this one stick is composed by x transitions from donor -> acceptor orbitals  

participating_orbitals_dict gives us the min & max orbital for donor & acceptor for spin up (a) & spin down (b)
"""


spectrum = Spectrumclass(folder_with_output_file)
participating_orbitals_dict = spectrum.return_participating_orbitals()


# now we will start to define from which to which orbital we are going

transitioncheck_dictionary['restrict_donor_orbitals_spinup'] = range(int(participating_orbitals_dict['donor_spin_up_min'][:-1]), int(participating_orbitals_dict['donor_spin_up_max'][:-1])+1)
transitioncheck_dictionary['restrict_donor_orbitals_spindown'] = range(int(participating_orbitals_dict['donor_spin_down_min'][:-1]), int(participating_orbitals_dict['donor_spin_down_max'][:-1])+1)

#print('participating_orbitals_dict:', participating_orbitals_dict)
first_acc_orbital = int(participating_orbitals_dict['acceptor_spin_up_min'][:-1])
last_acc_orbital = int(participating_orbitals_dict['acceptor_spin_up_max'][:-1])

print('first_acceptor_orbital:', first_acc_orbital)
print('last_acceptor_orbital:', last_acc_orbital)


"""
now we will start walking through all the orbitals
"""

try:
    for n, acceptor_orbital in enumerate(participating_orbitals_dict['all_acceptor_orbitals']):
        spin_state = 'unknownspinstate'
        if acceptor_orbital[-1] == 'a':
            spin_state = 'spinup'
        if acceptor_orbital[-1] == 'b':
            spin_state = 'spindown'
        label = f'orbital{acceptor_orbital[:-1]}_{spin_state}'
        transitioncheck_dictionary[f'restrict_acceptor_orbitals_spindown'] = []
        transitioncheck_dictionary[f'restrict_acceptor_orbitals_spinup'] = []
        transitioncheck_dictionary[f'restrict_acceptor_orbitals_{spin_state}'] = [int(acceptor_orbital[:-1])]
        transitioncheck_dictionary['number_of_analysis'] = number_of_most_intense_analyzed_sticks



        print(f"looking into orbital transition {n} (i.e. acceptor orbital {acceptor_orbital}) from {len(participating_orbitals_dict['all_acceptor_orbitals'])}-1 total transitions.")


        """
        here we will look for one acceptor orbital how the partial_spectrum for this one orbital looks like 
        """

        partial_spectrum = spectrum.checktransitions(transitioncheck_dictionary)


        # take this partial spectrum and extract the energy (x) and intensity (y) out of it to be able to export

        x = [i['Energy'] for i in partial_spectrum]
        y = [i['Intensity'] for i in partial_spectrum]


        # write all the sticks into a file

        with open(f'outputfolder{os.sep}output_{label}_stk.txt', 'w') as file:
            file.write('# ' + folder_with_output_file + '\n')
            file.write(f'{label}_Energie\t{label}_Normiert\n')
            for element in zip(x, y):
                file.write(str(element[0]) + '\t' + str(element[1]) + '\n')

        # broaden the spectrum using numpy, thanks google

        def broaden_spectrum(E,osc,sigma,x):
            gE=[]
            for Ei in x:
                tot=0
                for Ej,os in zip(E,osc):
                    tot+=os*np.exp(-((((Ej-Ei)/sigma)**2)))
                gE.append(tot)
            return gE

        broadened_axis = np.linspace(min(spectrum.energy()) - 2, max(spectrum.energy()) + 2, num=1000, endpoint=True)
        gE = broaden_spectrum(x, y, sigma, broadened_axis)

        # export the broadened spectrum into a txt file

        with open(f'outputfolder{os.sep}output_{label}_spec.txt', 'w') as file:
            # file.write('# ' + folder_with_output_file + '_' + label + '\n')
            file.write(f'{label}_Energie\t{label}_Normiert\n')
            for element in zip(broadened_axis, gE):
                file.write(str(round(element[0], 4)) + '\t' + str(round(element[1], 9)) + '\n')

        # export the broadened spectrum into a png file


        plt.close()
        plt.plot(broadened_axis, gE, "--k")
        plt.stem(x, y, markerfmt=' ', basefmt=None)
        plt.title(folder_with_output_file)

        plt.annotate(str(transitioncheck_dictionary), xy=(0.6, 0.85), xycoords='axes fraction', wrap=True, fontsize=6)
        # plt.text(0.5, 0.5, str(transitioncheck_dictionary), # transform=ax.transAxes)
        plt.savefig('outputfolder' + os.sep + f'output_{label}.png')

        plt.close()

except Exception as Err:
    print(Err)

print(participating_orbitals_dict['all_acceptor_orbitals'])