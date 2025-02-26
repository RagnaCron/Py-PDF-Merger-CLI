#!/usr/bin/env python
#
# MIT License
#
# Copyright (c) 2024-2025 Manuel Werder
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
import logging
import os
from tqdm import tqdm

from argparse import ArgumentParser
from pypdf import PdfWriter, PdfReader


def get_pdf_files_in_folders(folders, recursive=False):
    pdf_files_with_paths = []
    for folder_path in folders:
        try:
            # Choose appropriate directory walker based on recursive flag
            file_walker = os.walk(folder_path) if recursive else [(folder_path, None, os.listdir(folder_path))]
            for root, _, files in file_walker:
                pdf_files = [os.path.join(root, file) for file in files if file.lower().endswith('.pdf')]
                pdf_files_with_paths.extend(pdf_files)
        except Exception as e:
            logging.error(f"Error processing folder {folder_path}: {e}")
    return pdf_files_with_paths


def validate_pdf_files(file_paths):
    valid_files = []
    for file_path in file_paths:
        if not os.path.exists(file_path):
            logging.warning(f"File not found: {file_path}")
            continue
        if not file_path.lower().endswith(".pdf"):
            logging.warning(f"Not a PDF file: {file_path}")
            continue
        valid_files.append(file_path)
    return valid_files


def merge_pdfs(input_files, output_file):
    writer = PdfWriter()
    for file in tqdm(input_files, desc="Merging PDFs"):
        try:
            w = PdfWriter(file)
            for page in w.pages:
                page.compress_content_streams(level=9)
                writer.add_page(page)
        except Exception as e:
            logging.error(f"Error processing file {file}: {e}")
    writer.metadata = {}
    writer.compress_identical_objects()
    writer.write(output_file)
    writer.close()


def main():
    """
    Entry point of the program. It parses the command line arguments and calls the `merge_pdfs` function.

    :return: None
    """
    parser = ArgumentParser(
        description='This is a PDF merging Tool.',
        epilog='Copyright (c) 2024-2025 Manuel Werder. All rights reserved.'
    )
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

    parser.add_argument('--dry-run', action='store_true', help='Show files to be merged without merging them')

    parser.add_argument('--recursive', action='store_true', help='Recursively scan folders for PDFs')

    parser.add_argument('--version', action='version', version='%(prog)s No version info available')

    args = parser.parse_args()

    files = []

    if args.files:
        files = files + validate_pdf_files(args.files)

    if args.folders:
        pdf_files = get_pdf_files_in_folders(args.folders, recursive=args.recursive)
        files = files + pdf_files

    if args.dry_run:
        logging.info("Dry run mode. Files to be merged:")
        for file in files:
            print(file)
        return

    merge_pdfs(files, args.output_file)


if __name__ == '__main__':
    main()
