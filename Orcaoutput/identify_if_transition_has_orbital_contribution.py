def check_transition(transitioncheck_dictionary, spectrum_dictionary, transitions_dictionary):

    #print(transitioncheck_dictionary)
    #print(spectrum_dictionary)
    #print(transitions_dictionary)

    # transitioncheck_dictionary['restrict_donor_orbitals_spinup'] = [4]
    # transitioncheck_dictionary['restrict_acceptor_orbitals_spinup'] = []
    #
    # transitioncheck_dictionary['restrict_donor_orbitals_spindown'] = [5, 6]
    # transitioncheck_dictionary['restrict_acceptor_orbitals_spindown'] = [60, 61]
    #
    # transitioncheck_dictionary['number_of_analysis'] = number_of_most_intense_analyzed_sticks



    donor_space = []
    acceptor_space = []

    for donor_orbital in transitioncheck_dictionary['restrict_donor_orbitals_spinup']:
        donor_space.append(str(donor_orbital) + 'a')
    for donor_orbital in transitioncheck_dictionary['restrict_donor_orbitals_spindown']:
        donor_space.append(str(donor_orbital) + 'b')
    for acceptor_orbital in transitioncheck_dictionary['restrict_acceptor_orbitals_spinup']:
        acceptor_space.append(str(acceptor_orbital) + 'a')
    for acceptor_orbital in transitioncheck_dictionary['restrict_acceptor_orbitals_spindown']:
        acceptor_space.append(str(acceptor_orbital) + 'b')

    #   go through the donor and acceptor space
    #   check if a transition what we are looking for is there
    #   if yes, get the intensities
    #

    partial_spectrum = []

    for donor_orbital in donor_space:
        for acceptor_orbital in acceptor_space:
            #print(donor_orbital, '->', acceptor_orbital)
            pass

            for transition_package in transitions_dictionary:
                for line in transitions_dictionary[transition_package]:
                    #print(line.split()[0], line.split()[2])
                    try:
                        if (line.split()[0] == donor_orbital) and (line.split()[2] == acceptor_orbital):
                            relative_weight = line.split()[4]
                            weighted_intensity = round(float(relative_weight) * spectrum_dictionary['Intensity'][transition_package - 1], 9)
                            #print('#', spectrum_dictionary['Energy'][transition_package],
                            #      weighted_intensity,
                            #      line.split()[0], line.split()[2], transition_package)
                            partial_spectrum.append(
                                {
                                    'Energy': spectrum_dictionary['Energy'][transition_package - 1],
                                    'Intensity': weighted_intensity,
                                    'donor': line.split()[0],
                                    'acceptor': line.split()[2],
                                    'transition_number': transition_package
                                }
                            )
                    except Exception as err:
                        #print(err)
                        pass
    for element in partial_spectrum:
        #print(element)

        pass

    return partial_spectrum