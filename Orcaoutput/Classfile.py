
import os
import readspectrum
import identify_if_transition_has_orbital_contribution
import get_participating_orbitals_from_content


class Spectrumclass():

    def __init__(self, folder):

        # initialize
        # look into the given folder, find .out file, and read the whole file into "content" list
        self.read_output_file(folder)


        self.spectrum_dictionary = readspectrum.readspectrum(self.content)
        self.transitions_dictionary = readspectrum.readcontributions(self.content)
        #print('## self.transitions_dictionary:', self.transitions_dictionary)
        self.all_participating_orbitals = get_participating_orbitals_from_content.return_all_participating_orbitals(self.transitions_dictionary)



    def read_output_file(self, folder):
        for file in os.listdir(folder):
            #if file.endswith(".inp") and (file.count('.') == 1):
            #    outputfilename = file.replace('.inp', '.out')
            #    outputfilepath = folder + os.sep + outputfilename
            if file.endswith('.out'):
                outputfilename = file
                outputfilepath = folder + os.sep + outputfilename

        if outputfilepath:
            print('\nworking with the file:')
            print(outputfilepath, end="\n\n")
        else:
            #print('there was no .out file which had the same name as an .inp file.')
            print('did not find a file that ends with ".out"')
        ####
        #   read .out file as list into content variable
        ####

        with open(outputfilepath, 'r') as file:
            self.content = file.readlines()

    def return_dictionary(self):
        return self.spectrum_dictionary

    def energy(self):
        return self.spectrum_dictionary['Energy']

    def intensity(self):
        return self.spectrum_dictionary['Intensity']

    def index(self):
        return self.spectrum_dictionary['Index']

    def maxintensity(self):
        return max(self.spectrum_dictionary['Intensity'])

    def number_of_sticks(self):
        return len(self.spectrum_dictionary['Energy'])

    def return_transition(self, n):
        return self.transitions_dictionary[n]


    def return_list_of_tuple(self):
        return list(zip(self.energy(), self.intensity(), self.index()))


    def return_most_intense_transitions(self, number_of_transitions):
        # number_of_transitions = round(self.number_of_sticks() * fraction)
        return sorted(self.return_list_of_tuple(), key=lambda x: x[1], reverse=True)[:number_of_transitions]



    def return_participating_orbitals(self):
        return self.all_participating_orbitals


    def checktransitions(self, transitioncheck_dictionary):
        return identify_if_transition_has_orbital_contribution.check_transition(transitioncheck_dictionary, self.spectrum_dictionary, self.transitions_dictionary)