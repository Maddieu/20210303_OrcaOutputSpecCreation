



"""
read here the "transitions_dictionary.
this is one state ("STATE 1400:")
with all its transitions:
    18a -> 136a  :     0.020718 (c=  0.14393672)
    18a -> 142a  :     0.014727 (c= -0.12135343)
    20a -> 135a  :     0.016189 (c=  0.12723443)

split for 1st [0] and 3rd [2] column to get all participating orbitals
extract:
    donor_spin_up_min
    donor_spin_up_max
    donor_spin_down_min
    donor_spin_down_max

    acceptor_spin_up_min
    acceptor_spin_up_max
    acceptor_spin_down_min
    acceptor_spin_down_max
"""
def return_all_participating_orbitals(transitions_dictionary):
    participating_orbitals = {}
    list_of_all_participating_donor_orbitals_in_excitations = []
    list_of_all_participating_acceptor_orbitals_in_excitations = []
    for state in transitions_dictionary:
        for line in transitions_dictionary[state]:
            #print('here comes the state and line:', state, line)
            if not line.startswith('STATE'):
                donor_orbital, acceptor_orbital = line.split()[0], line.split()[2]
                if donor_orbital not in list_of_all_participating_donor_orbitals_in_excitations:
                    list_of_all_participating_donor_orbitals_in_excitations.append(donor_orbital)
                if acceptor_orbital not in list_of_all_participating_acceptor_orbitals_in_excitations:
                    list_of_all_participating_acceptor_orbitals_in_excitations.append(acceptor_orbital)

    #print(list_of_all_participating_donor_orbitals_in_excitations)

    participating_orbitals['donor_spin_up_min'] = sorted([i for i in list_of_all_participating_donor_orbitals_in_excitations if i.endswith('a')])[0]
    participating_orbitals['donor_spin_up_max'] = sorted([i for i in list_of_all_participating_donor_orbitals_in_excitations if i.endswith('a')])[-1]
    participating_orbitals['donor_spin_down_min'] = sorted([i for i in list_of_all_participating_donor_orbitals_in_excitations if i.endswith('b')])[0]
    participating_orbitals['donor_spin_down_max'] = sorted([i for i in list_of_all_participating_donor_orbitals_in_excitations if i.endswith('b')])[-1]

    participating_orbitals['acceptor_spin_up_min'] = str(sorted([int(i.replace('a','')) for i in list_of_all_participating_acceptor_orbitals_in_excitations if i.endswith('a')])[0]) + 'a'
    participating_orbitals['acceptor_spin_up_max'] = str(sorted([int(i.replace('a','')) for i in list_of_all_participating_acceptor_orbitals_in_excitations if i.endswith('a')])[-1]) + 'a'
    participating_orbitals['acceptor_spin_down_min'] = str(sorted([int(i.replace('b','')) for i in list_of_all_participating_acceptor_orbitals_in_excitations if i.endswith('b')])[0]) + 'b'
    participating_orbitals['acceptor_spin_down_max'] = str(sorted([int(i.replace('b','')) for i in list_of_all_participating_acceptor_orbitals_in_excitations if i.endswith('b')])[-1]) + 'b'

    participating_orbitals['all_acceptor_orbitals'] = list_of_all_participating_acceptor_orbitals_in_excitations

    return participating_orbitals