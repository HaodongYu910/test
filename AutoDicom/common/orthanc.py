import json, os

from AutoTest.common.transport import SSHConnection


def orthancInfo(**kwargs):
    BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "../.."))
    path = os.path.join(BASE_DIR, 'logs')
    ssh = SSHConnection(host=kwargs["host"], pwd=kwargs["pwd"])
    ssh.download('{0}/orthanc{1}.json'.format(path, kwargs["host"]),
                 '/home/biomind/.biomind/var/biomind/orthanc/orthanc.json')
    with open("{}/orthanc{}.json".format(path, kwargs["host"]), "r") as f:
        load_dict = json.load(f)
        print(load_dict["DicomModalities"])
        if load_dict["DicomModalities"].__contains__("orthanc120") is False:
            load_dict["DicomModalities"]["orthanc120"] = {
                "AET": "QA120",
                "Host": "192.168.1.120",
                "Port": "4242",
                "AllowEcho": True,
                "AllowFind": True,
                "AllowMove": True,
                "AllowStore": True
            }
            with open("{}/orthanc{}.json".format(path, kwargs["host"]), "w") as f:
                json.dump(load_dict, f)
            ssh.upload('{0}/orthanc{1}.json'.format(path, kwargs["host"]),
                 '/home/biomind/.biomind/var/biomind/orthanc/orthanc.json')
            ssh.close()
