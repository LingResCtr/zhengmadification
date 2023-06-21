#! /usr/bin/env python
# 
# Zheng Ma conversion helper functions

# == Packages =======================

import sys
import getopt

import pickle

import pandas as pd
import re


# == Data Input/Output ==============

def read_zm(file, file_encoding='utf-16', head=5, re_pattern=r"^\"(\w+)\"=\"(\w+)\"", verbose=False, find_character=None):
    # Read the Zheng Ma data files
    # Create a dictionary database, where 
    #   keys are the ZM codes, and
    #   values are the corresponding CJK characters
    # Input:
    #   file: filename
    #   file_encoding: what flavor of UTF encoding, or other?
    #   head: show how many (key, value) pairs?
    #   re_pattern: give a raw-string with the regex for reading codes & characters from the file
    # Output:
    #   zm_codes: dictionary of (code, character) pairs
    #   print:
    #     how many lines read
    #     how many lines with characters
    #     head-number of (key, value) pairs in zm_codes
    
    data_pattern = re.compile(re_pattern)
    
    zm_codes = {}
    line_count = 0
    cjk_count = 0
    head_count = 0
    
    with open(file, encoding=file_encoding) as fi:
        for line in fi:
            row = line.strip()

            if not row:
                # Optionally let me know if we've skipped a line
                if verbose:
                    print('Skipping line: {}'.format(row))
                continue
            
            line_count += 1
            
            m = data_pattern.match(line)
            if m:
                zm_code, cjk_char = m.group(1), m.group(2)

                # It turns out that some ZM codes are used
                # for more than one CJK character string.
                # So we need to make sure not to overwrite earlier characters
                # by making the new ZM code string unique.
                # (Example: the code yi in the RIME database)
                # So append '-' and then add a number suffix
                # ... but make sure that new code isn't already there...
                while zm_code in zm_codes.keys():
                    if '-' not in zm_code:
                        zm_code += '-'
                    
                    base_code, n_suffix = zm_code.split('-')
                    
                    # Take the numerical suffix and add 1
                    # But if n_suffix is None, int(n_suffix) is undefined
                    zm_code = base_code + '-' + str(int(0 if n_suffix in (None, '') else n_suffix) + 1)

                    # Next loop... see if this incremented code is itself already in the keys
                    # If not, done.  If it is, increment again.
                
                # We should now have a zm_code not in the keys
                zm_codes[zm_code] = cjk_char

                cjk_count += 1

                # In case we want to make sure that we read in
                # a certain CJK character from the database
                if find_character:
                    if str(find_character) in cjk_char:
                        print('Found one instance of {}: \nLine: {:>}\t{:>}\t{:>}'.format(str(find_character), cjk_count, zm_code, cjk_char))
            else:
                # Optionally let me know if there was no regex match
                if verbose:
                    print('No pattern match in line {:>}: {}'.format(line_count, row))
                continue

   
    print('\nTotal lines read:  {:>10}'.format(line_count))
    print('Total codes found: {:>10}\n'.format(cjk_count))

    if head > 0:
        # If you want to see some of the ZM codes and CJK characters read in
        print('Some of the initial codes:\n')
        for code_idx, cjk_string in zm_codes.items():
            if head_count < head:
                print('{}:\t{}'.format(code_idx, cjk_string))
                head_count += 1
            else:
                break

    return zm_codes


# == Character & Code Conversion ====

def characters_to_codes(cjk_string, zm_dataframe, cjk_columns=['MS Characters'], zm_column='ZM Codes'):
    # Input: 
    #   string of CJK characters
    #   database of Zheng Ma codes as a pandas DataFrame
    #   list of columns to check for characters
    #   name of column containing Zheng Ma codes
    # Output: 
    #   list (dictionary?) of Zheng Ma codes

    characters = cjk_string.strip().replace(' ', '')

    codes = {}

    for character in characters:
        codes[character] = {}

        for column in cjk_columns:
            # This part won't work based on the test above
            # For the 'MS Characters' column, for example, CJK character '三' returns **3 rows**: dg, dgg, dggg
            codes[character][column] = zm_dataframe[zm_dataframe[column] == character][zm_column]
    
    return codes


def characters_to_codes_simplistic(cjk_string, zm_dataframe, db_column='RIME Characters', zm_column='ZM Codes'):
    # Input: 
    #   string of CJK characters
    #   database of Zheng Ma codes as a pandas DataFrame
    #   name of column to check for characters
    #   name of column containing Zheng Ma codes
    # Output: 
    #   list (dictionary?) of Zheng Ma codes
    #     - In case of multiple code correspondences, choose the longest

    characters = cjk_string.strip().replace(' ', '')

    codes = []

    for character in characters:
        # Find any rows in the desired column that have the desired character
        # Take the ZM codes in those rows as a list
        possible_codes = zm_dataframe[zm_dataframe[db_column] == character][zm_column].tolist()

        # Choose the **longest code** in that list of ZM codes
        max_code = max(possible_codes, key=len) if possible_codes else None
        # There could be several, so order alphabetically and pick the first
        desired_codes = [c for c in possible_codes if len(c) == len(max_code)] if max_code else None
        desired_code = sorted(desired_codes)[0] if desired_codes else 'N/A: no match'
        codes.append([character, desired_code])
    
    return codes

def codes_to_characters_simplistic(code_list, zm_dataframe, db_column='RIME Characters', zm_column='ZM Codes'):
    # Input: 
    #   list of ZM codes
    #   database of Zheng Ma codes as a pandas DataFrame
    #   name of column to check for characters
    #   name of column containing Zheng Ma codes
    # Output: 
    #   string of CJK characters
    #     - In case of multiple character correspondences for a code, choose...

    cjk_string = ''

    for code in code_list:
        # Make sure the code is a valid ZM code:
        #   - fewer than 5 letters
        #   - no spaces
        if ' ' not in code:
            if len(code) < 5:
                # Get the characters for that code
                possible_characters = zm_dataframe[zm_dataframe[zm_column] == code][db_column].tolist()
                # Remove any empty strings
                viable_characters = [x for x in possible_characters if (len(x) > 0)]
                # Add the smallest string (hopefully 1 character)
                # ... watch out: there might be more than one minimum...
                # ... what does min() do?  return the first it finds in the list?
                cjk_string += min(viable_characters, key=len)
            else:
                print('Code too long: {}'.format(code))
        else:
            print('Code should not contain spaces: {}'.format(code))
    
    return cjk_string

# == Unicode Conversion =============

def characters_to_unicodes(cjk_string):
    # Read a list of CJK characters (as strings)
	# Convert to a number, write the number in hexadecimal
    return [hex(ord(x)) for x in cjk_string]

def unicodes_to_characters(code_list):
	# Read a list of hexadecimal codes as strings (with '0x' prefix)
	# Convert to hexadecimal numbers, then get the corresponding Unicode character
	return [chr(int(code, 16)) for code in code_list]

# == Default Usage ==================

def usage():
    # How to use this...
    message = """
    Usage:
        zm_helpers [-h] [-c=<cjk_string>] [-z=<zm_code_string>]
    
    Options:
        -h, --help: print the usage message
        -c, --cjk: follow by input string comprising CJK characters, 
        -z, --zmcode: follow by input string comprising a quote-delimited string 
                        of ZM codes separated by spaces
    
    """

    print(message)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:z:", ["help", 
                                                            "cjk=",
                                                            "zmcode="
                                                            ])

    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    
    process = None
    input = None
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-c", "--cjk"):
            process = 'cjk'
            input = arg.replace('=','')
        elif opt in ("-z", "--zmcode"):
            process = 'zmcode'
            input = arg.replace('=','').split()
            print(input)
        else:
            assert False, "unhandled option"
    

    data_prefix = '../data/'
    
    # Load pickle    
    with open(data_prefix + 'df_zm_merged.pkl', 'rb') as pickle_file:
        df_zm_merged = pickle.load(pickle_file)
    
    # Process input
    # test_string1 = '三人行必有我師'
    # test_code1 = 'cd od oi wzm gdq mdhm ?'
    # test_string2 = '性相近也习相远也'
    # test_code2 = 'umc flvv pdw yi yt flvv bdrw yi'

    if process == 'cjk':
        zm_codes = characters_to_codes_simplistic(input, df_zm_merged)
        print(zm_codes)
    elif process == 'zmcode':
        zm_characters = codes_to_characters_simplistic(input, df_zm_merged)
        print(zm_characters)
    else:
        print("Please specify an input type and string of codes or CJK characters")

if __name__ == "__main__":
    main()

