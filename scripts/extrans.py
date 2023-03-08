import sys
import os

from pathlib import Path

if __name__ == '__main__':
    python_loc = sys.exec_prefix
    print(f'+Python located at: {python_loc}')
    if len(sys.argv) < 3:
        print('-Missing arguments')
        print(f'Usage: {__file__} %1 %2 [%3]')
        print('%1 - input file (.py)')
        print('%2 - output file')
        print('%3 - domain')
        exit(0)

    infile = Path(sys.argv[1])
    print(f'+Infile path: {infile}')
    outfile = Path(sys.argv[2])
    print(f'+Outfile path: {outfile}')

    try:
        domain = sys.argv[3]
    except IndexError:
        domain = 'base'

    print(f'+Domain: {domain}')

    print('+Extracting...')

    command = f'python {python_loc}/Tools/i18n/pygettext.py -v -d {domain} -o {outfile} {infile} '
    os.system(command)
    print(f'+Done. File saved to {outfile.absolute().parent}')
