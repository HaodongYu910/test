# coding=utf-8
#python study_statistic --filefolder "xxx/xxxxxx/xxxxx"
import csv
import datetime
import os
import codecs
import sys
import getopt
from TestPlatform.tools.image_num_verify import runVerify

def get_yesterday():
    now_time = datetime.datetime.now()
    yesterday_time = now_time + datetime.timedelta(days=-1)
    return(yesterday_time.strftime('%Y%m%d'))

def get_date():
    now_time = datetime.datetime.now()
    return (now_time.strftime("%Y%m%d"))

def isbetween(times):
    date = times[:8]
    time = times[8:]
    if (date == get_yesterday()) or (date == get_date() and time[:2] <= "09"):
        return True
    else:
        return False

def isanalysis(filename):
    if filename.split("_")[-1] == "analysis.csv":
        return True
    else:
        return False

def prepare_config(argv):
    try:
        opts, args = getopt.getopt(argv, "", ["filefolder="])
        for opt, arg in opts:
            if opt in ("--filefolder"):
                csv_filefolder = arg
    except Exception as e:
        print("error: failed to get args")
    if not os.path.isdir(csv_filefolder):
        return False
    else:
        return csv_filefolder


def main(server_ip):
    runVerify(server_ip)
    csv_filefolder = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "../..")),
                            'logs/{0}'.format(server_ip))
    if not csv_filefolder:
        print("failed to find filefolder")
        sys.exit(0)
    else:
        rightfile = set()
        for filename in os.listdir(csv_filefolder):
            if(isanalysis(filename)):
                if(isbetween(filename.split("_")[1])):
                    rightfile.add(os.path.join(csv_filefolder,filename))
        datas = []
        miss_image = 0
        sendcount = 0
        acceptcount = 0
        success = 0
        fail = 0
        unpredict = 0
        start_time = get_yesterday() + "-" + "090000"
        end_time = get_date() + "-" + "090000"
        # start_time = "20200426" + "-" + "090000"
        # end_time = "20200427" + "-" + "090000"
        for eachcsv in rightfile:
            with open(eachcsv, 'r+', encoding='utf-8') as dailyfile:
                rows = csv.reader(dailyfile)
                for row in rows:
                    datas.append(row)
            dailyfile.close()

        for each in datas[1:]:
            date = each[0].split("-")[0]
            times = each[0].split("-")[1]
            # if (date == get_yesterday() and times[:2] >= "09") or (date == get_date()):
            if (date == get_yesterday() and times[:2] >= "09") or (date == get_date() and times[:2] <= "09"):
                sendcount += 1
                if eval(each[5]) != 0:
                    acceptcount += 1
                    aistatus = eval(each[6])
                    if aistatus == 1 or aistatus == 2:
                        success += 1
                    elif aistatus == -1:
                        fail += 1
                    else:
                        unpredict += 1
                if int(each[4])+2 > int(each[5]):
                    miss_image += 1
            else:
                continue

        csv_fn = os.path.join(csv_filefolder, "summarize.csv")
        csv_exist = os.path.isfile(csv_fn)
        summarizefile = codecs.open(csv_fn, 'a', 'gbk')
        writer = csv.writer(summarizefile)
        if not csv_exist:
            items = ("start_time", "end_time", "send", "accept", "success_predict", "fail_predict", "unpredict", "miss_image")
            writer.writerow(items)
        newrow = []
        newrow.extend([start_time, end_time, sendcount, acceptcount, success, fail, unpredict, miss_image])
        writer.writerow(newrow)
        summarizefile.close()



if __name__ == "__main__":
    main('192.168.1.122')
