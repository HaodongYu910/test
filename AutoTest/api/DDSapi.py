from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from AutoTest.common.api_response import JsonResponse
from AutoDicom.common.deletepatients import *
from AutoDicom.common.duration_verify import *

class ddsData(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取持续列表详细数据
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        type = request.GET.get("type")
        ddsHostID = int(request.GET.get("id"))
        datalist = {}

        # 判断是否有查询时间
        if request.GET.get("startdate"):
            startdate = request.GET.get("startdate")
        else:
            startdate = '2000-01-01 00:00:00'

        if request.GET.get("enddate"):
            enddate = request.GET.get("enddate")
        else:
            enddate = datetime.datetime.now()

        # 判断查询数据类型
        if type == 'patientid':
            patientid = request.GET.get("patientid")
            obi = duration_record.objects.filter(duration_id=durationid, patientid__contains=patientid).order_by("-id")
        elif type == 'Not_sent':
            obi = duration_record.objects.filter(duration_id=durationid, aistatus__isnull=True,
                                                 create_time__lte=enddate, create_time__gte=startdate).order_by("-id")
        elif type == 'sent':
            obi = duration_record.objects.filter(duration_id=durationid, aistatus__isnull=False,
                                                 create_time__lte=enddate, create_time__gte=startdate).order_by("-id")
        elif type == 'AiTrue':
            obi = duration_record.objects.filter(duration_id=durationid, aistatus__in=[1, 2], create_time__lte=enddate,
                                                 create_time__gte=startdate).order_by("-id")
        elif type == 'AiFalse':
            obi = duration_record.objects.filter(duration_id=durationid, aistatus__in=[-1, -2, 3],
                                                 create_time__lte=enddate, create_time__gte=startdate).order_by("-id")
        else:
            obi = duration_record.objects.filter(duration_id=durationid, create_time__lte=enddate,
                                                 create_time__gte=startdate).order_by("-id")
        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        count = paginator.count  # 总页数
        try:
            obm = paginator.page(page)
        except PageNotAnInteger:
            obm = paginator.page(1)
        except EmptyPage:
            obm = paginator.page(paginator.num_pages)
        serialize = duration_record_Deserializer(obm, many=True)
        rdata = serialize.data
        du = duration.objects.get(id=durationid)
        if du.dds is not None:
            server = du.dds
        else:
            server = du.server
        try:
            datalist['sent'] = durationtotal(obi, server, '1,2')
            datalist['ai_false'] = durationtotal(obi, server, '-2,-1,1,2,3')
            datalist['ai_true'] = durationtotal(obi, server, '1,2')
            datalist['ai_false'] = durationtotal(obi, server, '-2,3')
            datalist['notai'] = durationtotal(obi, server, '-1')
            datalist['all'] = obi.count()
            datalist['notsent'] = int(datalist['all']) - int(datalist['sent'])
        except ValueError:
            return JsonResponse(data={"data": datalist
                                      }, code="0", msg="测试环境数据库连接失败")
        for i in rdata:
            try:
                dbresult = connect_postgres(database="orthanc",Username='postgres',password='4a53e4f5c42fd5a31890860b204472c5',Port='5432',host=server,
                                               sql="SELECT aistatus,diagnosis,imagecount,insertiontime FROM study_view WHERE studyinstanceuid =\'{0}\'".format(
                                                   i["studyinstanceuid"]))
                _dict = dbresult.to_dict(orient='records')
            except Exception as e:
                logger.error(e)
            if _dict == []:
                i['aistatus'] = None
                i['diagnosis'] = None
                i['imagecount_server'] = None
            else:
                for j in _dict:
                    i['aistatus'] = j['aistatus']
                    i['diagnosis'] = j['diagnosis']
                    i['imagecount_server'] = j['imagecount']

        return JsonResponse(data={"data": rdata,
                                  "durationresult": [datalist],
                                  "page": page,
                                  "total": total,
                                  "count": count
                                  }, code="0", msg="成功")

class sync_dds_data(APIView):

    # time_dic = {}
    # time_dic[1] = {"time":"00:00:00-03:59:59", "success":0, "fail":0, "image":0}
    # time_dic[2] = {"time":"04:00:00-07:59:59", "success":0, "fail":0, "image":0}
    # time_dic[3] = {"time":"08:00:00-11:59:59", "success":0, "fail":0, "image":0}
    # time_dic[4] = {"time":"12:00:00-15:59:59", "success":0, "fail":0, "image":0}
    # time_dic[5] = {"time":"16:00:00-19:59:59", "success":0, "fail":0, "image":0}
    # time_dic[6] = {"time":"20:00:00-23:59:59", "success":0, "fail":0, "image":0}
    # current_time_period = time.localtime()
    # i = 0
    # for i in 12:
    #     time_dic[i] = 1
    pass

