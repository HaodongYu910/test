from django.db.models import Count, When, Case
from ..models import install, dictionary
from AutoInterface.models import  gold_record

from AutoUI.models import autoui, auto_uirecord

import logging


logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


class InstallReportThread:
    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.obj = install.objects.get(id=self.id)

    def report(self):
        result = []
        goldData = []
        uiData = []
        try:
            uidiseases = auto_uirecord.objects.filter(auto__autoid=self.obj.uid).values('case_id').annotate(

                success=Count(Case(When(result='匹配成功', then=0))), fail=Count(Case(When(result='匹配失败', then=0))),
                count=Count('case_id'))

            for i in uidiseases:
                error = int(i["count"]) - int(i["success"]) - int(i["fail"])
                disease = {
                    "diseases": i["diseases"],
                    "aisuccess": int(i["success"]) + int(i["fail"]),
                    "success": i["success"],
                    "fail": i["fail"],
                    "error": error
                }
                uiData.append(disease)

            smokediseases = gold_record.objects.filter(gold_id=self.obj.gold_id).values('diseases').annotate(
                success=Count(Case(When(result='匹配成功', then=0))), fail=Count(Case(When(result='匹配失败', then=0))),
                count=Count('diseases'))

            for j in smokediseases:
                error = int(j["count"]) - int(j["success"]) - int(j["fail"])
                disease = {
                    "diseases": j["diseases"],
                    "aisuccess": int(j["success"]) + int(j["fail"]),
                    "success": j["success"],
                    "fail": j["fail"],
                    "error": error
                }
                goldData.append(disease)

            for k in ['成功', '失败']:
                smobj = gold_record.objects.filter(gold_id=self.obj.gold_id, result__contains=k)
                uiobj = auto_uirecord.objects.filter(auto__autoid=self.obj.uid, result__contains=k)
                result.append(smobj.count())
                result.append(uiobj.count())
            smerror = int(gold_record.objects.filter(gold_id=self.obj.gold_id).count()) - int(result[0]) - int(
                result[2])
            uierror = int(auto_uirecord.objects.filter(auto__autoid=self.obj.uid).count()) - int(result[1]) - int(
                result[3])
            data = {
                "basedata": [{
                    "version": self.obj.version,
                    "product": '金标准测试',
                    "aisuccess": int(result[0]) + int(result[2]),
                    "success": result[0],
                    "fail": result[2],
                    "error": smerror
                }, {
                    "version": self.obj.version,
                    "product": 'UI自动化',
                    "aisuccess": int(result[1]) + int(result[3]),
                    "success": result[1],
                    "fail": result[3],
                    "error": uierror
                }],
                "gold": {
                    "version": self.obj.version,
                    "product": '金标准测试',
                    "aisuccess": int(result[0]) + int(result[2]),
                    "success": result[0],
                    "fail": result[2],
                    "error": smerror
                },
                "ui": {
                    "version": self.obj.version,
                    "product": 'UI自动化',
                    "aisuccess": int(result[1]) + int(result[3]),
                    "success": result[1],
                    "fail": result[3],
                    "error": uierror
                },
                "goldrows": [
                    {'状态': '匹配成功', '数量': result[0]},
                    {'状态': '匹配失败', '数量': result[2]},
                    {'状态': '报错', '数量': smerror}
                ],
                "uirows": [
                    {'状态': '匹配成功', '数量': result[1]},
                    {'状态': '匹配失败', '数量': result[3]},
                    {'状态': '报错', '数量': uierror}
                ],
                "uiData": uiData,
                "goldData": goldData
            }
        except Exception as e:
            logger.error("数据报错{}".format(e))
            return {}
        return data
