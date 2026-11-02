"""
List all affixes available in the SemEval dataset.
"""
from collections import defaultdict
import csv
import os

def process_inflections(input_path, output_dir):
    '''List every affix on inflection file, order by its frequency.'''
    affixes = defaultdict(int)

    with open(input_path, 'r', encoding='utf-8') as input_file:
        input_reader = csv.reader(input_file, delimiter='\t')
        for line in input_reader:
            morphemes = line[1].split('|')
            for morph in morphemes[1:]:
                affixes[morph] += 1

    affixes = sorted(affixes.items(), key=lambda i: i[1], reverse=True)

    output_path = os.path.join(output_dir, 'semeval_affixes.txt')
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(f"Total: {len(affixes)}\n\n")
        for affix, count in affixes:
            output_file.write(f'{count:4d} {affix}\n')

    print(f"Found {len(affixes)} affixes")


def process_derivations(input_path, output_dir):
    '''List every affix on derivation file, order by its frequency.'''
    prefixes = defaultdict(int)
    suffixes = defaultdict(int)

    with open(input_path, 'r', encoding='utf-8') as input_file:
        input_reader = csv.reader(input_file, delimiter='\t')
        for line in input_reader:
            morphemes = line[1].split('|')
            is_prefix = line[2] == 'prefix'
            if is_prefix:
                prefixes[morphemes[0]] += 1
            else:
                suffixes[morphemes[-1]] += 1

    prefixes = sorted(prefixes.items(), key=lambda i: i[1], reverse=True)
    suffixes = sorted(suffixes.items(), key=lambda i: i[1], reverse=True)

    output_path = os.path.join(output_dir, 'semeval_affixes.txt')
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(f"Prefixes: {len(prefixes)}\n")
        for affix, count in prefixes:
            output_file.write(f'{count:4d} {affix}\n')

        output_file.write(f"\n\nSuffixes: {len(suffixes)}\n")
        for affix, count in suffixes:
            output_file.write(f'{count:4d} {affix}\n')

    print(f"Found:\n{len(prefixes)} prefixes\n{len(suffixes)} suffixes")
