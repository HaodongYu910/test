import re, os, sys
final = []
pwd = os.getcwd()
def listfilename():
    cwd =os.path.abspath(os.path.join(os.getcwd(), "../..")) + '/logs'
    list = os.listdir(cwd)
    print(cwd)
    for i in list:
        list2 = os.path.join(cwd, i)
        if os.path.isdir(list2):
            os.chdir(list2)
            listfilename()
        else:
            final.append(list2)

if len(sys.argv) != 1:
    filenames = sys.argv[1:]
else:
    listfilename()
    filenames = final

for file in final:
    print(file)
    filename = file
    log_dir = os.path.join(pwd, filename)
    with open(log_dir, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        error_line = []
        for line in lines:
            if 'Error' in line or 'ERROR' in line or 'Exception' in line or 'EXCEPTION' in line:
                line1 = re.findall(r'(ERROR|Error|Exception|EXCEPTION) (.*)', line)
                if len(line1) >= 1:
                    line1 = line1[0]
                    error_line.append(line1[1])
                else:
                    break
    print('日志错误总数为------> ' + str(len(error_line)) + '个')
    print('日志错误类型数量为------> ' + str(len(list(set(error_line)))) + '个')
    for i in list(set(error_line)):
        with open('result.txt', 'a') as result:
            #result.write('日志错误总数为------> ' + str(len(error_line)) + '个'+ '\n' )
            #result.write('日志错误类型数量为------> ' + str(len(list(set(error_line)))) + '个' + '\n')
            result.write(file + '\n')
            result.write(i + '\n')
            print(i)