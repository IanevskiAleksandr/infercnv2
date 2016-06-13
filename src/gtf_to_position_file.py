#!/usr/bin/env python


"""
Converts GTF files to proprietary formats.
"""


# Import statements
import argparse
import os

__author__ = 'Timothy Tickle, Itay Tirosh, Brian Haas'
__copyright__ = 'Copyright 2016'
__credits__ = ["Timothy Tickle"]
__license__ = 'BSD-3'
__maintainer__ = 'Timothy Tickle'
__email__ = 'ttickle@bbroadinstitute.org'
__status__ = 'Development'


def convert_to_positional_file(input_gtf, output_positional):
    """ Convert input GTF file to positional file.

    :param input_gtf: Path to input gtf file
    :type input_gtf: String
    :param output_positional: Path to output positional file
    :type output_positional: String

    :returns: Indicator of success (True) or Failure (False)
    :rtype: boolean
    """

    if not input_gtf or not os.path.exists(input_gtf):
        print("gtf_to_position_file.py:: Could not find input file : " + input_gtf)

    # Holds lines to output after parsing.
    output_line = []
    previous_gene = None
    previous_chr = None
    gene_positions = []

    with open(input_gtf, "r") as gtf_file:
        for gtf_line in gtf_file:
            if gtf_line[0] == "#":
                pass
            line_tokens = gtf_line.split("\t")
            gene_name = line_tokens[8].split(";")[0].split(" ")[1].strip('"').split("|")[0]
            if not gene_name == previous_gene:
                if len(gene_positions) > 1:
                    gene_positions.sort()
                    output_line.append("\t".join([previous_gene,
                                                  previous_chr,
                                                  str(gene_positions[0]),
                                                  str(gene_positions[-1])]))
                gene_positions = []
            gene_positions += [int(line_tokens[3]), int(line_tokens[4])]
            previous_gene = gene_name
            previous_chr = line_tokens[0]
        if previous_gene and previous_chr and len(gene_positions) > 1:
            gene_positions.sort()
            output_line.append("\t".join([previous_gene,
                                          previous_chr,
                                          str(gene_positions[0]),
                                          str(gene_positions[-1])]))

    with open(output_positional, "w") as positional_file:
        positional_file.write("\n".join(output_line))


if __name__ == "__main__":

    # Parse arguments
    prsr_arguments = argparse.ArgumentParser(prog='gtf_to_position_file.py',
                                             description='Convert a GTF file to a positional file.',
                                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # Add positional argument
    prsr_arguments.add_argument("input_gtf",
                                metavar="input_gtf",
                                help="Path to the input GTF file.")
    prsr_arguments.add_argument("output_positional",
                                metavar="output_positional",
                                help="Path for the output positional file.")
    args = prsr_arguments.parse_args()

    # Run Script
    convert_to_positional_file(args.input_gtf, args.output_positional)
