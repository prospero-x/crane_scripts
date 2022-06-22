import os
import glob
import re

"""
This script is meant to be run after Bolsig+ has created outputs. It parses
the output in every directory matching *K (every temperature directory)
and places each electron-impact reaction rate into a single text file
for CRANE to reference
"""

# Bolsig+ understands the addition of an electron as an ionization, which
# means multiple reactions are listed under IONIZATION in the output. To
# distinguish Ionization reactions, I set the threshold energy to be slightly
# different for each one, and this dictionary is used to identify and name each
# reaction in the Bolsig+ output.
_REACTION_NAMES = {
    '.*Ionization.*13.30 eV': 'CO2_ionization',
    '.*Excitation.*0.083 eV': 'CO2v1_excitation',
    '.*Excitation.*0.17 eV':  'CO2v2_excitation',
    '.*Excitation.*0.25 eV':  'CO2v3_excitation',
    '.*Excitation.*0.34 eV':  'CO2v4_excitation',
    '.*Excitation.*10.50 eV': 'CO2*_excitation',
    '.*Attachment':             'CO2_attachment',
    '.*Ionization.*10.50 eV': 'O+_production',
    '.*Ionization.*10.60 eV': 'CO+_production',
    '.*Ionization.*10.70 eV': 'C+_production',
    '.*Excitation.*10.80 eV': 'CO+O_neutral_production',
}

def get_reaction_name(data_line):
    """
    Using regex patterns corresponding to known reaction names, find
    the reaction name corresponding to this data line in the Bolsig+
    output file.
    """

    for pattern, reaction_name in _REACTION_NAMES.items():
        if re.match(pattern, data_line):
            return reaction_name
    return None


def parse_output_file(directory):
    """
    Parse the Bolsig+ output file into separate text files, one for each
    reaction.
    """
    data_dir = directory + '/electron_impact_rates'
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    bolsig_output_filename = directory + f'/CO2_plasma_rates_{directory}.dat'
    with open(bolsig_output_filename, 'r') as f:
        line = f.readline()
        reaction_file = None


        # Sometimes Bolsig+ can have duplicate values for the mean electron
        # energy. Since crane objects to this, we compare to the previously
        # written x-value and only write in the case where the new line
        # does not match the previous one.
        prev_x = None
        while line:
            line = line.strip()
            columns = line.split(' ')
            if len(columns) == 1:
                columns = line.split('\t')

            if re.match('C\d+', columns[0]):
                if 'Effective (momentum)' in line:
                    # Ignore electron effective momentum data
                    line = f.readline()
                    continue

                reaction_name = get_reaction_name(line)
                if reaction_name is None:
                    print('Warning: failed to find reaction name matching line "%s"' % line)
                    line = f.readline()
                    continue

                reaction_file_name = data_dir + '/' + reaction_name + '.txt'

                # This is now the file handle to which we are writing data
                reaction_file = open(reaction_file_name, 'w')

            elif line == 'Energy (eV) 	Electric field / N (Td)':
                # special case, the relationship between mean electron energy and E/N
                reaction_file_name = directory + '/reduced_field.txt'
                reaction_file = open(reaction_file_name, 'w')

            elif reaction_file is not None:
                if line == '':
                    # Reached the end of this data set
                    print(f'wrote reaction rate file {reaction_file_name}')
                    reaction_file.close()
                    reaction_file = None
                elif line != 'Energy (eV)	Rate coefficient (m3/s)' and columns[0] != prev_x:
                    reaction_file.write(line + '\n')
                    prev_x = columns[0]

            line = f.readline()


def main():
    dirs = glob.glob('*K')
    for directory in dirs:
        parse_output_file(directory)


if __name__ == '__main__':
    main()

