import glob
import plotly.express as px
import pandas as pd
import re
import json

global CSVHEADER
global VENDOR
CSVHEADER = 'datetime,download,upload,ping\n'
VENDOR = 'MAGENTA Kabelinternet + TV'

def toCSV(filename):
    try:
        with open(filename, 'r') as filePointer:
            with open(filename + '.csv', 'w+') as filePointerCSV:
                filePointerCSV.write(CSVHEADER)
                for line in filePointer:
                    dateTime = re.search('#(.*)#', line)
                    lineJsonS = line[(dateTime.span()[1]+1):(len(line))]
                    lineJson = json.loads(lineJsonS)
                    csv_line = '"{}",{},{},{}\n'.format(dateTime.group(1), round(lineJson['download']/1000000, 2), round(lineJson['upload']/1000000, 2), round(lineJson['ping'], 2))
                    filePointerCSV.write(csv_line)
    except Exception as Ex:
        print('Excetion during convertion to CSV! Ex: %s' % str(Ex))

def parseLogFiles(FileDirectory):
    try:
        # parse logfile
        filenames = glob.glob(FileDirectory+'*.log')
        for filename in filenames:
                toCSV(filename)
    except Exception as Ex:
        print('Error parsing files! Ex: %s' % str(Ex))


def main():
    try:
        parseLogFiles('./logs/')

        df = pd.read_csv('./logs/2020-06-11.log.csv')

        fig = px.line(df, x='datetime', y='download', title='SPEEDTEST - {}'.format(VENDOR))

        fig.show()

    except Exception as Ex:
        print('Exception: %s' % str(Ex))


if __name__ == '__main__':
    main()