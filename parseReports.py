#print f.read(10)


# testStep = []
# testException = []
#
# testStepList = []
# testExceptionList = []
lSuccess = 'test_run_this_test Success'
lFailure = 'test_run_this_test Failure'
lError = 'test_run_this_test Error'
lTestStep = 'Test Step'
lFailStep = 'C:/Python27'
lFailStep2 = 'F]]>'
lExceptOpen = '<exception>'
lExceptClose = '</exception>'

class ParseReport(object):

    def __init__(self):
        self.testStep = []
        self.testException = []
        self.testStepList = []
        self.testExceptionList = []

        self.addTo = 'pass'


    def printLines(self, lis):
        for item in lis:
            print item

    def concatLines(self, lis):
        final = ''
        for item in lis:
            final += item.rstrip('\n')
        return final

    def findException(self, s):
        n = '/n'
        e = ']>'
        count = 0
        last = ''
        nExcept = False
        lastExcept = ''
        lExcept = False
        while count < len(s) - 1:
            count += 1
            if count < 1:
                continue
            elif s[count-1:count+1] == e:
                return lastExcept
            elif nExcept == False:
                if s[count-1:count+1] == n:
                    nExcept = True
                    last = s[count-1:count+1]
                else:
                    last += s[count]
            elif nExcept == True:
                if s[count-1:count+1] == n:
                    last += s[count]
                    lastExcept = last
                    nExcept = False
                else:
                    last += s[count]
        return lastExcept

    def run(self):
        f = open('testReport.txt', 'r+')

        lines = f.readlines()

        for line in lines:
            if self.addTo == 'pass':
                if line[0:len(lFailure)] == lFailure:
                    self.addTo = 'fail'
            if self.addTo == 'fail':
                if line[0:len(lTestStep)] == lTestStep:
                    self.testStep.append(line)
                    self.addTo = 'failStep'
            if self.addTo == 'failStep':
                if line[0:len(lTestStep)] == lTestStep:
                    self.testStep = []
                    self.testStep.append(line)
                elif line[0:len(lFailStep)] == lFailStep or line[0:len(lFailStep2)] == lFailStep2:
                    self.addTo = 'except'
                    self.testException.append(line)
                    self.testStepList.append(self.concatLines(self.testStep))
                    self.testStep = []
                else:
                    self.testStep.append(line)
            elif self.addTo == 'except':
                if line[0:len(lExceptOpen)] == lExceptOpen:
                    self.addTo = 'exceptOpen'
                    testException = []
                    testException.append(line)
            elif self.addTo == 'exceptOpen':
                if line[0:len(lExceptClose)] == lExceptClose:
                    self.addTo = 'pass'
                    self.testException.append(line)
                    self.testExceptionList.append(self.findException(self.concatLines(
                        testException)))
                else:
                    testException.append(line)

        count = 0
        for i in self.testStepList:
            count += 1
            print str(count) + '. ' + i
            #print '\n'

        count = 0
        for i in self.testExceptionList:
            count += 1
            print str(count) + '. ' + i
            #print '\n'

        #findException(testExceptionList[0])
        f.close()

if __name__ == "__main__":
    pr = ParseReport()
    pr.run()
