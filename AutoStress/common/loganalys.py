# encoding=utf-8
import re, os, sys
from ..models import errorlog
final = []
pwd = os.getcwd()

def errorLogger(stressid,version,folder):
    os.system("unzip {}".format(folder))
    file_names = os.listdir(folder)
    file_names.sort()
    for fn in file_names:
        full_fn = os.path.join(folder, fn)
        if (os.path.splitext(fn)[1] in ['.log'] == False):
            continue
        elif (os.path.isdir(full_fn)):
            errorLogger(full_fn)
            continue
        with open(full_fn, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            error_line = []
            for line in lines:
                if 'Error' in line or 'ERROR' in line or 'Exception' in line or 'EXCEPTION' in line:
                    line1 = re.findall(r'(ERROR|Error|Exception|EXCEPTION|Traceback) (.*)', line)
                    if len(line1) >= 1:
                        line1 = line1[0]
                        error_line.append(line1[1])
                        data ={
                            "version": version,
                            "stressid": stressid,
                            "content": line1[1],
                            "route": full_fn
                        }
                        errorlog.objects.create(**data)
                    else:
                        break

