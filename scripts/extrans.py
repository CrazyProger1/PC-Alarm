import sys
import os

if __name__ == '__main__':
    python_loc = sys.exec_prefix
    print(f'+Python located at: {python_loc}')
    if len(sys.argv) < 3:
        print('-Missing arguments')
        print(f'Usage: {__file__} %1 %2')
        print('%1 - input file (.py)')
        print('%2 - output file')
        exit(0)

    infile = sys.argv[1]
    print(f'+Infile path: {infile}')
    outfile = sys.argv[2]
    print(f'+Outfile path: {outfile}')

    print('+Extracting...')

    command = f'python {python_loc}/Tools/i18n/pygettext.py -v -d myapp -o {outfile} {infile} '
    os.system(command)
    print(f'+File saved to {os.path.abspath(outfile)}')
