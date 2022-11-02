#!/usr/bin/env python

import csv, os, sys

def process_csv(filetype):

     # Test if CSV file exists
    if filetype == "artists":
        csv_file = "artist-studies/artists.csv"
    elif filetype == "modifiers":
        csv_file = "modifier-studies/modifiers.csv"

    if not os.path.exists(csv_file):
        sys.exit("Error: File {} does not appear to exist." .format(csv_file))

    with open(csv_file) as f:
        reader = csv.DictReader(f)

        artists = {}
        modifiers = {}

        # Iterate through each row in the CSV
        for row in reader:
            if filetype == "artists":
                # store artist_name depending on presence of first name in spreadsheet
                if not row['Artist (first)'] or row['Artist (first)'] == 'N/A':
                    artist_name = "{}" .format(row['Artist (last/only) (or other effect)'])
                else:
                    artist_name = "{}, {}" .format(row['Artist (last/only) (or other effect)'], row['Artist (first)'])

                is_recognized = True if row['Recognized? (Stable)'] == 'Yes' else False

                tags = [tag.strip() for tag in row['Tags (work-in-progress)'].split(',')]

                # remove any empty strings from tags list
                while '' in tags:
                    tags.remove('')

                # replace non-alphanumeric characters with hyphens for artist_name and each tag value
                artist_name = ''.join(e for e in artist_name if e.isalnum() or e == " ").replace(" ", "-")
                
                # add artist entry to dictionary
                artists[artist_name] = {
                    "is_recognized": is_recognized,
                    "tags": tags
                }
                
            elif filetype == "modifiers":
                modifier_name = row['Name']
                strength = row['Strength']
                tags = [tag.strip() for tag in row['Tags'].split(',')]

                # remove any empty strings from tags list
                while '' in tags:
                    tags.remove('')

                 # replace non-alphanumeric characters with hyphens for each modifier_name and tag value
                modifier_name = ''.join(e for e in modifier_name if e.isalnum() or e == " ").replace(" ", "-")

                # add modifier entry to dictionary
                modifiers[modifier_name] = {
                    "strength": strength,
                    "tags": tags,
                } if len(strength) > 0 else None # don't include modifiers which don't have recognizable effects in SD

        # sort artists and modifiers dictionaries alphabetically by key before returning them
        if filetype == "artists":
            return {k: v for k, v in sorted(artists.items(), key=lambda item: item[0])}

        elif filetype == "modifiers":
            return {k: v for k, v in sorted(modifiers.items(), key=lambda item: item[0])}

    f.close()


# def generate_wildcards(artists, modifiers):