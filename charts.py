import glob
import plotly.express as px
import plotly.graph_objects as go
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
                lineNo = 0
                for line in filePointer:
                    try:
                        lineNo += 1
                        dateTime = re.search('#(.*)#', line)
                        lineJsonS = line[(dateTime.span()[1]+1):(len(line))]
                        lineJson = json.loads(lineJsonS)
                        csv_line = '"{}",{},{},{}\n'.format(dateTime.group(1), round(lineJson['download']/1000000, 2), round(lineJson['upload']/1000000, 2), round(lineJson['ping'], 2))
                        filePointerCSV.write(csv_line)
                    except Exception as Ex:
                        print('Excetion during line-parsing to CSV! LineNo. {} Ex: {}'.format(lineNo, str(Ex)))
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

        filenames = glob.glob('./logs/*.csv')
        for filename in filenames:
            df = pd.read_csv(filename)

            df_long = pd.melt(df, id_vars=['datetime'],
                              value_vars=['download', 'upload', 'ping'])

            fig = px.line(df_long, x='datetime', y='value', color='variable',
                          title='SPEEDTEST - {}'.format(VENDOR))

            for figData in fig.data:
                if figData.name == 'ping':
                    figData.name += ' [ms]'
                else:
                    figData.name += ' [MBit/s]'

            fig.update_traces(mode="markers+lines", hovertemplate=None)
            fig.update_layout(hovermode="x unified", hoverlabel=dict(namelength=-1))

            fig.write_html('.{}.html'.format(filename.split('.')[1]))
        # fig.show()

    except Exception as Ex:
        print('Exception: %s' % str(Ex))


if __name__ == '__main__':
    main()