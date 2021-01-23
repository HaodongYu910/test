import os
from TestPlatform.common.regexUtil import savecsv
from TestPlatform.models import auto_case,autotest,dicom


# 执行UI 自动化测试
def autoRun(id):
    path = os.path.join(os.getcwd())
    obj = autotest.objects.get(id=str(id))
    print(obj.cases)
    caseobj = auto_case.objects.filter(id__in=obj.cases)
    for i in caseobj:
        dicomobj = dicom.objects.filter(fileid=i.testdata)
        for j in dicomobj:
            savecsv(str('{0}/testdata/tdd.csv'.format(path)), [j.diseases, j.studyinstanceuid, j.vote])