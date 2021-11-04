import numpy as np
import os
import readspectrum
from Classfile import Spectrumclass
from matplotlib import pyplot as plt



sigma = 0.3 # broadening for spectrum export

folder_with_output_file = r'D:\OrcaData\20211027_MT_DyCp_specC_slowSCF_Roots1400_ompiotest'
folder_with_output_file = r'D:\OrcaData\20211011_Olesya_Mn4O4_PBE0_tightenedSCF'

transitioncheck_dictionary = {}



number_of_most_intense_analyzed_sticks = 20

first_acc_orbital = 70
last_acc_orbital = 116
last_acc_orbital = 72
# spin up from 70
# spin down from 65
# until 116 + 1


spectrum = Spectrumclass(folder_with_output_file)
participating_orbitals_dict = spectrum.return_participating_orbitals()

"""
    donor_spin_up_min
    donor_spin_up_max
    donor_spin_down_min
    donor_spin_down_max

    acceptor_spin_up_min
    acceptor_spin_up_max
    acceptor_spin_down_min
    acceptor_spin_down_max"""

transitioncheck_dictionary['restrict_donor_orbitals_spinup'] = range(int(participating_orbitals_dict['donor_spin_up_min'][:-1]), int(participating_orbitals_dict['donor_spin_up_max'][:-1])+1)
transitioncheck_dictionary['restrict_donor_orbitals_spindown'] = range(int(participating_orbitals_dict['donor_spin_down_min'][:-1]), int(participating_orbitals_dict['donor_spin_down_max'][:-1])+1)

#print('participating_orbitals_dict:', participating_orbitals_dict)
first_acc_orbital = int(participating_orbitals_dict['acceptor_spin_up_min'][:-1])
last_acc_orbital = int(participating_orbitals_dict['acceptor_spin_up_max'][:-1])

print('first_acc_orbital:', first_acc_orbital)
print('last_acc_orbital:', last_acc_orbital)

try:
    for n, acceptor_orbital in enumerate(participating_orbitals_dict['all_acceptor_orbitals']):
        spin_state = 'unknownspinstate'
        if acceptor_orbital[-1] == 'a':
            spin_state = 'spinup'
        if acceptor_orbital[-1] == 'b':
            spin_state = 'spindown'
        label = f'{spin_state}_orbital{acceptor_orbital[:-1]}'
        transitioncheck_dictionary[f'restrict_acceptor_orbitals_spindown'] = []
        transitioncheck_dictionary[f'restrict_acceptor_orbitals_spinup'] = []
        transitioncheck_dictionary[f'restrict_acceptor_orbitals_{spin_state}'] = [int(acceptor_orbital[:-1])]
        transitioncheck_dictionary['number_of_analysis'] = number_of_most_intense_analyzed_sticks



        print(f"looking into orbital transition {n} (i.e. acceptor orbital {acceptor_orbital}) from {len(participating_orbitals_dict['all_acceptor_orbitals'])}-1 total transitions.")




        partial_spectrum = spectrum.checktransitions(transitioncheck_dictionary)


        x = [i['Energy'] for i in partial_spectrum]
        y = [i['Intensity'] for i in partial_spectrum]



        with open(f'outputfolder{os.sep}output_{label}_stk.txt', 'w') as file:
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

        broadened_axis = np.linspace(min(spectrum.energy()) - 2, max(spectrum.energy()) + 2, num=1000, endpoint=True)
        gE = broaden_spectrum(x, y, sigma, broadened_axis)


        with open(f'outputfolder{os.sep}output_{label}_spec.txt', 'w') as file:
            # file.write('# ' + folder_with_output_file + '_' + label + '\n')
            file.write(f'{label}_Energie\t{label}_Normiert\n')
            for element in zip(broadened_axis, gE):
                file.write(str(round(element[0], 4)) + '\t' + str(round(element[1], 9)) + '\n')



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