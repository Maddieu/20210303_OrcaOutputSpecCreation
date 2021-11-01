import numpy as np
import os
import readspectrum
from Classfile import Spectrumclass
from matplotlib import pyplot as plt





folder_with_output_file = r'D:\OrcaData\20211022_MT_DyCp_specC_slowSCF_Roots800'



transitioncheck_dictionary = {}

transitioncheck_dictionary['restrict_donor_orbitals_spinup'] = range(18, 27+1)
transitioncheck_dictionary['restrict_donor_orbitals_spindown'] = range(18, 27+1)



number_of_most_intense_analyzed_sticks = 20

first_acc_orbital = 70
last_acc_orbital = 116
# spin up from 70
# spin down from 65
# until 116 + 1
try:
    for acceptor_orbital in range(first_acc_orbital,last_acc_orbital+1):
        label = f'spinup_orbital{acceptor_orbital}'
        transitioncheck_dictionary['restrict_acceptor_orbitals_spinup'] = []
        transitioncheck_dictionary['restrict_acceptor_orbitals_spindown'] = []
        transitioncheck_dictionary['restrict_acceptor_orbitals_spinup'] = [acceptor_orbital]
        transitioncheck_dictionary['restrict_acceptor_orbitals_spindown'] = []
        transitioncheck_dictionary['number_of_analysis'] = number_of_most_intense_analyzed_sticks

        print(f'looking into orbital {acceptor_orbital} from {last_acc_orbital}')


        spectrum = Spectrumclass(folder_with_output_file)

        for element in spectrum.return_transition(1):
            #print(element, end="")
            pass

        for element in spectrum.return_most_intense_transitions(number_of_most_intense_analyzed_sticks):
            #print(element)
            pass


        partial_spectrum = spectrum.checktransitions(transitioncheck_dictionary)

        #for element in partial_spectrum:
        #    if (element['donor'] == '12b') and (element['acceptor'] == '36b'):
        #        #print(element)
        #        pass

        x = [i['Energy'] for i in partial_spectrum]
        y = [i['Intensity'] for i in partial_spectrum]



        with open(f'outputfolder\output_{label}_stk.txt', 'w') as file:
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
        sigma = 0.3
        gE = broaden_spectrum(x,y,sigma,broadened_axis)


        with open(f'outputfolder\output_{label}_spec.txt', 'w') as file:
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