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


from argparse import ArgumentParser
from pypdf import PdfMerger


def merge_pdfs(input_files, output_file):
    merger = PdfMerger()
    for file in input_files:
        merger.append(file)
    merger.write(output_file)
    merger.close()


def main():
    parser = ArgumentParser()
    parser.add_argument('input_files', nargs='+', help='List of input PDF files, the order of the files is important')
    parser.add_argument('output_file', help='Output PDF file')
    args = parser.parse_args()

    merge_pdfs(args.input_files, args.output_file)


if __name__ == '__main__':
    main()
