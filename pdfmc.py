#!/usr/bin/env python
#
# MIT License
#
# Copyright (c) 2024 Manuel Werder
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os

from argparse import ArgumentParser
from pypdf import PdfWriter


def get_pdf_files_in_folders(folders):
    pdf_files_with_paths = []
    for folder_path in folders:
        try:
            # List all files in the given folder
            files = os.listdir(folder_path)
            # Filter out the files with a .pdf extension and get their full paths
            pdf_files = [os.path.join(folder_path, file) for file in files if file.lower().endswith('.pdf')]
            pdf_files_with_paths.extend(pdf_files)
        except Exception as e:
            print(f"An error occurred with folder {folder_path}: {e}")
    return pdf_files_with_paths



def merge_pdfs(input_files, output_file):
    """
    Merge PDFs.

    :param input_files: List of input PDF files to be merged.
    :param output_file: Output file to save the merged PDF.
    :return: None

    This method takes a list of input PDF files and merges them into a single PDF file specified by the output file path.
    The input files are appended one by one using the `PdfWriter.append` method from the `pypdf` library, and then the
    merged PDF is written to the output file using the `PdfWriter.write` method.

    .. Example usage:
    >>> input_files = ["file1.pdf", "file2.pdf", "file3.pdf"]
    >>> output_file = "merged.pdf"
    >>> merge_pdfs(input_files, output_file)

    .. note::
        This method requires the `pypdf` library to be installed.

    .. warning::
        The output file will be overwritten if it already exists.

    .. seealso::
        `pypdf <https://pypi.org/project/pypdf/>`_
    """
    writer = PdfWriter()
    for file in input_files:
        writer.append( file)
    writer.write(output_file)
    writer.close()


def main():
    """
    Entry point of the program. It parses the command line arguments and calls the `merge_pdfs` function.

    :return: None
    """
    parser = ArgumentParser()
    parser.add_argument(
        '-i',
        '--files',
        nargs='+',
        help='List of input PDF files, the order of the files is important')
    parser.add_argument(
        '-f',
        '--folders',
        nargs='+',
        help='List of input Folders with PDF files, the order of the folders and the files in them is important')
    parser.add_argument('-o', '--output_file', help='Output PDF file', default='merged.pdf')
    args = parser.parse_args()

    files = []

    if args.files:
        files = files + args.files

    if args.folders:
        pdf_files = get_pdf_files_in_folders(args.folders)
        files = files + pdf_files

    print("PDF files to merge:")
    for pdf in files:
        print(pdf)

    merge_pdfs(files, args.output_file)


if __name__ == '__main__':
    main()
