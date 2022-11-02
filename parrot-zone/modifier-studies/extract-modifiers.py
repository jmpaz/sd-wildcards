#!/usr/bin/env python

import csv
import os
import re

modifiers = {}

# Create the directory structure if it doesn't already exist
if not os.path.exists('modifiers'):
    os.makedirs('modifiers')
    print('Created modifiers/')

if not os.path.exists('modifiers/strength'):
    os.makedirs('modifiers/strength')
    print('Created modifiers/strength/')

if not os.path.exists('modifiers/tags'):
    os.makedirs('modifiers/tags')
    print('Created modifiers/tags/')


# Get column indexes for Name, Strength, and Tags from the first row of the csv file
with open('modifiers.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    headers = next(reader)
    name_index = headers.index('Name')
    strength_index = headers.index('Strength')
    tags_index = headers.index('Tags')

    print('Starting to parse modifiers.csv...')
    
    # Iterate through each row of the csv file starting after column headers
    for row in reader:

        # Get the Name, Strength, and Tags values from each row
        name = row[name_index]
        strength = row[strength_index]
        tags = row[tags_index]

        # Add the Name, Strength, and Tags values to the modifiers dictionary if they don't already exist
        if name not in modifiers:
            modifiers[name] = {
                'strength': strength,
                'tags': []
            }

        # Add the Tags values to the modifiers dictionary if they don't already exist
        for tag in tags.split(','):
            tag = tag.strip()

            if tag not in modifiers[name]['tags']:
                modifiers[name]['tags'].append(tag)

        # Create a new text file for each tag if it doesn't already exist
        for tag in modifiers[name]['tags']:

            # Remove any non-alphanumeric characters from the filename, replacing them with a hyphen
            tag_filename = re.sub(r'[^a-zA-Z0-9]', '-', tag)

            if not os.path.exists('modifiers/tags/{}.txt'.format(tag_filename)):
                with open('modifiers/tags/{}.txt'.format(tag_filename), 'w') as tagfile:
                    pass

        # Append the Name value to the corresponding text file for each tag
        for tag in modifiers[name]['tags']:

            # Remove any non-alphanumeric characters from the filename, replacing them with a hyphen
            tag_filename = re.sub(r'[^a-zA-Z0-9]', '-', tag)

            with open('modifiers/tags/{}.txt'.format(tag_filename), 'a') as tagfile:
                print(name, file=tagfile)

        # Append the Name value to the corresponding text file for each strength level if it doesn't already exist
        if strength == '★★★':
            strength_filename = 'high'

        elif strength == '★★☆':
            strength_filename = 'med'

        elif strength == '★☆☆':
            strength_filename = 'low'

        with open('modifiers/strength/{}.txt'.format(strength_filename), 'a') as strengthfile:
            print(name, file=strengthfile)


# Create a text file containing all Name values from the csv
with open('modifiers/all-modifiers.txt', 'w') as allfile:
    for name in modifiers:
        print(name, file=allfile)
    
print('Done!')