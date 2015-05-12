
class DrbdConnector(object):
    def getDrbdLines(self):
        return open('/proc/drbd','r').readlines()

class DrbdParser(object):
    def __init__(self,num,connector=DrbdConnector()):
        self.num=num
        self.connector=connector
    def parse(self):
        num2=str(self.num)
        lines=[x.strip() for x in self.connector.getDrbdLines()]
        found=[x for x in enumerate(lines) if x[1][:len(num2)+1]==num2+':']
        line=lines[found[0][0]]
        nextl=lines[found[0][0]+1]
        csi=line.index('cs:')
        roi=line.index('ro:')
        dsi=line.index('ds:')
        self.cs=line[csi+3:roi-1].strip()
        self.dr=line[roi+3:dsi-1].strip()
        self.dr1=self.dr.split('/')[0]
        self.dr2=self.dr.split('/')[1]
        self.ds=line[dsi+3:].split(' ')[0]
        self.ds1=self.ds.split('/')[0]
        self.ds2=self.ds.split('/')[1]


if __name__=='__main__':
    print DrbdConnector().getDrbdLines()
    DrbdParser(1).parse()
