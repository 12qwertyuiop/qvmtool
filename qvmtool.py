from base64 import urlsafe_b64encode, urlsafe_b64decode
from hashlib import sha1
import hmac
import requests
import json
from tabulate import tabulate
import wcwidth
import argparse
import textwrap


class Auth(object):

    def __init__(self, access_key, secret_key, disable_qiniu_timestamp_signature=None):
        """初始化Auth类"""
        self.__checkKey(access_key, secret_key)
        self.__access_key = access_key
        self.__secret_key = b(secret_key)
        self.disable_qiniu_timestamp_signature = disable_qiniu_timestamp_signature

    @staticmethod
    def __checkKey(access_key,secret_key):
        if not (access_key and secret_key):
            raise ValueError('invalid key')

    def get_access_key(self):
        return self.__access_key

    def get_secret_key(self):
        return self.__secret_key

    def __token(self, data):
        data = b(data)
        hashed = hmac.new(self.__secret_key, data, sha1)
        return urlsafe_base64_encode(hashed.digest())

    def token(self, data):
        return '{0}:{1}'.format(self.__access_key, self.__token(data))

def urlsafe_base64_encode(data):
    """urlsafe的base64编码:

    对提供的数据进行urlsafe的base64编码。规格参考：
    https://developer.qiniu.com/kodo/manual/1231/appendix#1

    Args:
        data: 待编码的数据，一般为字符串

    Returns:
        编码后的字符串
    """
    ret = urlsafe_b64encode(b(data))
    return s(ret)


def urlsafe_base64_decode(data):
    """urlsafe的base64解码:

    对提供的urlsafe的base64编码的数据进行解码

    Args:
        data: 待解码的数据，一般为字符串

    Returns:
        解码后的字符串。
    """
    ret = urlsafe_b64decode(s(data))
    return ret


def s(data):
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    return data


def b(data):
    if isinstance(data, str):
        return data.encode('utf-8')
    return data

def list_qvm(Qauth):
    signingStr="GET" + " "+"/v1/vm/instance"
    signingStr=signingStr+"\nHost: api-qvm.qiniu.com\n\n"
    z=Qauth.token(signingStr)
    headers = {
        "Host":"api-qvm.qiniu.com",
        "Authorization":"Qiniu {0}".format(z)
    }
    req = requests.get(url="https://api-qvm.qiniu.com/v1/vm/instance",headers=headers)
    result = json.loads(req.text)
    qvm_num = result["total"]
    print("qvm主机数量：{0}".format(qvm_num))
    qvmdata_sum = []
    for index in range(qvm_num):
        qvmdata = []
        qvminfo = result["data"][index]
        instance_id = qvminfo['instance_id']
        os_type = qvminfo['image_info']['os_type']
        status = qvminfo['image_info']['status']
        region_id = qvminfo['region_id']
        vnc_passwd = qvminfo['vnc_passwd']
        eip_address = qvminfo['eip_address']['ip_address']
        public_ip_address = qvminfo['public_ip_address']['ip_address']
        qvmdata.extend([instance_id,os_type,status,region_id,vnc_passwd,eip_address,public_ip_address])
        qvmdata_sum.append(qvmdata)
    return print(tabulate(qvmdata_sum, headers=["instance_id", "os_type", "status","region_id","vnc_passwd","eip_address","public_ip_address"],tablefmt='psql'))

def changepass_qvm(Qauth,instance_id,region_id,password):
    urlpath = "/v1/vm/instance/{0}/attribute".format(instance_id)
    signingStr="PUT" + " "+urlpath
    signingStr=signingStr+"\nHost: api-qvm.qiniu.com"
    signingStr=signingStr+"\nContent-Type: application/json"
    signingStr=signingStr+"\n\n"
    reqbody="{\"region_id\":\""+region_id+"\",\"password\":\""+password+"\"}"
    signingStr=signingStr+reqbody
    z = Qauth.token(signingStr)
    headers = {
        "Host": "api-qvm.qiniu.com",
        "Authorization": "Qiniu {0}".format(z),
        "Content-Type": "application/json"
    }
    req = requests.put(url="https://api-qvm.qiniu.com{0}".format(urlpath), headers=headers, data=reqbody)
    #print(req.text)
    if req.status_code ==200:
        return print("qvm reset password please reboot ...")


def reboot_qvm(Qauth,instance_id,region_id):
    """
    #POST /v1/vm/instance/:instance_id/reboot（重启）
    #请求参数 instance_id（path） region_id(body)
    """
    urlpath = "/v1/vm/instance/{0}/reboot".format(instance_id)
    signingStr="POST" + " "+urlpath
    signingStr=signingStr+"\nHost: api-qvm.qiniu.com"
    signingStr=signingStr+"\nContent-Type: application/json"
    signingStr=signingStr+"\n\n"
    reqbody = "{\"region_id\":\""+region_id+"\"}"
    signingStr=signingStr+reqbody
    z = Qauth.token(signingStr)
    headers = {
        "Host": "api-qvm.qiniu.com",
        "Authorization": "Qiniu {0}".format(z),
        "Content-Type": "application/json"
    }
    req = requests.post(url="https://api-qvm.qiniu.com{0}".format(urlpath), headers=headers,data=reqbody)
    if req.status_code ==200:
        return print("qvm reboot...")

def GetVNC_Url(Qauth,instance_id,region_id):
    """
    # instance_id	string	path	是	云主机实例ID
    # region_id	string	body	是	地域 ID。
    :param Qauth:
    :param instance_id:
    :param region_id:
    :return: vnc_url
    """
    urlpath = "/v1/vm/instance/{0}/vnc_url?region_id={1}".format(instance_id,region_id)
    signingStr = "GET" + " " + urlpath
    signingStr = signingStr + "\nHost: api-qvm.qiniu.com"
    signingStr = signingStr + "\n\n"
    z = Qauth.token(signingStr)
    headers = {
        "Host": "api-qvm.qiniu.com",
        "Authorization": "Qiniu {0}".format(z),
    }
    req = requests.get(url="https://api-qvm.qiniu.com{0}".format(urlpath), headers=headers)
    vnc_url = json.loads(req.text)
    vnc_url = vnc_url['data']['vnc_url']
    return  print(vnc_url)
def ResetVNC_Pass(Qauth,instance_id,region_id,password):
    urlpath = "/v1/vm/instance/{0}/vnc_passwd".format(instance_id)
    signingStr = "PUT" + " " + urlpath
    signingStr = signingStr + "\nHost: api-qvm.qiniu.com"
    signingStr = signingStr + "\nContent-Type: application/json"
    signingStr = signingStr + "\n\n"
    reqbody = "{\"region_id\":\"" + region_id + "\",\"vnc_password\":\""+ password+"\"}"
    signingStr = signingStr + reqbody
    z = Qauth.token(signingStr)
    headers = {
        "Host": "api-qvm.qiniu.com",
        "Authorization": "Qiniu {0}".format(z),
        "Content-Type": "application/json"
    }
    req = requests.put(url="https://api-qvm.qiniu.com{0}".format(urlpath), headers=headers, data=reqbody)
    print(req.text)
    if req.status_code == 200:
        return print("qvm vncpassword reset...")
def setqvmkey():

    print("Enter qvm ak:")
    access_key = input()
    print("Enter qvm sk:")
    secret_key = input()
    with open("config.json","w") as f:
        f.write("{\"ak\":\""+access_key+"\",\"sk\":\""+secret_key+"\"}")
    return print("setkey finish")

def get_Qauth():
    with open("config.json","r") as r:
        keyjson = r.readline()
        keyjson = json.loads(keyjson)
        #print(keyjson,type(keyjson))
    access_key = keyjson['ak']
    secret_key = keyjson['sk']
    #print(access_key,secret_key)
    return Auth(access_key, secret_key)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='qvmtool', formatter_class=argparse.RawDescriptionHelpFormatter,epilog=textwrap.dedent(
            """
                python qvmtool.py -s #set qiniu qvm ak and sk
                python qvmtool.py -l #list qvm
                python qvmtool.py -r -i instance_id -rid region_id #reboot qvm
                python qvmtool.py --vncurl -i instance_id -rid region_id #vnc url
                python qvmtool.py --resetvncpassword -i instance_id -rid region_id -p Qvm123
            """
        ))
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('-s','--setkey',action='store_true',help='#set ak and sk')
    parser.add_argument('-l', '--listqvm', action='store_true', help='#list qvminfo')
    parser.add_argument('-r', '--reboot', action='store_true', help='#reboot qvm')
    parser.add_argument('-i', '--instance_id', type=str, help='#set instance_id')
    parser.add_argument('-rid', '--region_id', type=str, help='#set region_id')
    parser.add_argument('-rhp', '--resethostpassword', action='store_true', help='#reset qvm password#注意：重置实例密码后，需要在重启实例后才能生效')
    parser.add_argument('--vncurl', action='store_true', help='#get vncurl')
    parser.add_argument('-p','--password', type=str, help='#set password')
    parser.add_argument('-rvp','--resetvncpassword', action='store_true', help='#reset vnc password,仅限 6 个字符，必须包含大小写字母和数字，不支持特殊字符\n注意：修改密码后，如果是I/O优化的实例，立刻生效，无需重启实例；非I/O优化的实例，需要在控制台或者 API 重启实例才能生效。')
    args = parser.parse_args()

    if args.setkey:
        setqvmkey()
    if args.listqvm:
        list_qvm(get_Qauth())
    if args.reboot and args.instance_id and args.region_id:
        reboot_qvm(get_Qauth(),args.instance_id,args.region_id)
    if args.resethostpassword and args.instance_id and args.region_id and args.password:
        changepass_qvm(get_Qauth(), args.instance_id, args.region_id, args.password)
    if args.vncurl:
        GetVNC_Url(get_Qauth(),args.instance_id,args.region_id)
    if args.resetvncpassword and args.instance_id and args.region_id and args.password:
        ResetVNC_Pass(get_Qauth(), args.instance_id, args.region_id, args.password)


