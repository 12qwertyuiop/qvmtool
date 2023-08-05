<h1 align="center">qvmtool</h1>

qvmtool是一个简单的七牛云主机管理脚本,用于安全测试，其他行为概不负责🤗



### 安装

```bash
git clone https://github.com/12qwertyuiop/qvmtool
pip -r requirements.txt
```



### 使用方法

```
usage: qvmtool [-h] [--version] [-s] [-l] [-r] [-i INSTANCE_ID] [-rid REGION_ID] [-rhp] [--vncurl] [-p PASSWORD] [-rvp]
                                                                                                                       
options:                                                                                                               
  -h, --help            show this help message and exit                                                                
  --version             show program's version number and exit                                                         
  -s, --setkey          #set ak and sk                                                                                 
  -l, --listqvm         #list qvminfo                                                                                  
  -r, --reboot          #reboot qvm                                                                                    
  -i INSTANCE_ID, --instance_id INSTANCE_ID                                                                            
                        #set instance_id
  -rid REGION_ID, --region_id REGION_ID
                        #set region_id
  -rhp, --resethostpassword
                        #reset qvm password#注意：重置实例密码后，需要在重启实例后才能生效
  --vncurl              #get vncurl
  -p PASSWORD, --password PASSWORD
                        #set password
  -rvp, --resetvncpassword
                        #reset vnc password,仅限 6 个字符，必须包含大小写字母和数字，不支持特殊字符 注意：修改密码后，如果是I/O优化的实例，立刻生效，无需重启实例；非I/O优化的实例，需要在控制台或者 API 重启实例才能生效。

python qvmtool.py -s #set qiniu qvm ak and sk
python qvmtool.py -l #list qvm
python qvmtool.py -r -i instance_id -rid region_id #reboot qvm
python qvmtool.py --vncurl -i instance_id -rid region_id #vnc url
python qvmtool.py --resetvncpassword -i instance_id -rid region_id -p Qvm123
```

### 例子

![setkey](https://github.com/12qwertyuiop/qvmtool/blob/main/img/setkey.PNG)

![qvmlist](https://github.com/12qwertyuiop/qvmtool/blob/main/img/listqvm.PNG)

### 学习与交流

👇

![qrcode](https://github.com/12qwertyuiop/qvmtool/blob/main/img/qrcode.png)
