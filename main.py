"""
MorphEval-PT - Evaluation Script
"""

import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

import argparse

import morpheval_pt


# default path to MorphEval-PT files
_MORPHEVAL_DER_FPATH="./data/morpheval/derivational.tsv"
_MORPHEVAL_INF_FPATH="./data/morpheval/inflectional.tsv"


def read_arguments(format_required=True):
    '''Read and return valid command line arguments.'''
    parser = argparse.ArgumentParser(description="MorphEval-PT")

    # FORMAT OPTIONS
    format_options = parser.add_mutually_exclusive_group(required=format_required)
    format_options.add_argument(
        '-I', '--inflectional',
        action="store_true",
        help="Input file follows the inflectional dataset format."
    )
    format_options.add_argument(
        '-D', '--derivational',
        action="store_true",
        help="Input file follows the derivational dataset format."
    )

    # INPUT and OUTPUT options
    parser.add_argument(
        "--file-path",
        required=False,
        help="Path to TSV file. When not specified, the default " +
            "MorphEval-PT file will be selected based on format option."
    )
    parser.add_argument(
        "--model-name",
        required=False,
        help="Local path or name of the model hosted on HuggingFace's Hub."
    )

    args = parser.parse_args()
    return args


def derivational():
    print("MorphEval-PT: DERIVATIONAL Evaluation.")
    args = read_arguments(format_required=False)
    args.derivational = True

    # default input file
    if args.file_path is None:
        args.file_path = _MORPHEVAL_DER_FPATH

    morpheval_pt.evaluate(args.file_path, args.model_name)


def inflectional():
    print("MorphEval-PT: INFLECTIONAL Evaluation.")
    args = read_arguments(format_required=False)
    args.inflectional = True

    # default input file
    if args.file_path is None:
        args.file_path = _MORPHEVAL_INF_FPATH

    morpheval_pt.evaluate(args.file_path, args.model_name)


def main():
    print("MorphEval-PT")
    args = read_arguments()

    # default input file
    if args.file_path is None:
        if args.derivation:
            args.file_path = _MORPHEVAL_DER_FPATH
        else:
            args.file_path = _MORPHEVAL_INF_FPATH

    morpheval_pt.evaluate(args.file_path, args.model_name)


if __name__ == "__main__":
    main()
