import requests
import time
import os
import shutil
import json

def pre(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
        print("已删除之前生成的%s文件夹"%dir)
    os.makedirs(dir)

def get_time(x):
    hour,minute,second=0,0,0
    if x>3600:
        hour=x//3600
        x%=3600
    if x>60:
        minute=x//60
        x%=60
    second=x
    return "{}小时{}分{}秒".format(hour,minute,second)

pre("./temp")
startTime = time.time()

# 改这里！！！
l = 11
r = 399
name_list_file = "/work100/chenrenmiao/CN-Celeb/id_name_list"

Error_id = []



with open(name_list_file,"r") as f:
    task = []
    for line in f:
        task.append(line)

    while len(task) != 0:
        try:
            line = task[0]
            id = line.split(" ")[0]
            word = line.split(" ")[1]
            peo_num = int(id[2:7])
            del(task[0])
            if peo_num < l or peo_num > r:
                continue
            print(id,peo_num,word)
            
            # 注意：这里pn=  后面的数字是30的倍数，也是页面打开的数量限制！！！  # 最后1&e是一个时间戳！！！
            head = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 '
                            'Safari/537.36 SLBrowser/7.0.0.6241 SLBChan/25 '
            }
            number = 20
            root = './temp/%s/'%id
            pre(root)
            num = 1
            while num * 30 <= int(number):
                num = num + 1
            imglist = []

            for i in range(0, int(num)):
                finalurl = 'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=10746385342931146838&ipn=rj&ct' \
                        '=201326592&is=&fp=result&queryWord=%E6%9D%8E%E5%85%8B%E5%8B%A4%E5%9B%BE%E7%89%87' \
                        '&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&word={}' \
                        '&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&expermode=&nojc=&cg' \
                        '=star&pn={}&rn=30&gsm=b4&{}='.format(
                    word, (i + 1) * 30, time.time())

                response = requests.get(url=finalurl, headers=head).json()

                for j in range(0, len(response['data']) - 1):
                    imglist.append(response['data'][j]['thumbURL'])

            for ke in range(0, int(number)):
                content = requests.get(url=imglist[ke], headers=head).content
                path = root+str(ke)+'.png'
                with open(path, 'wb') as e:
                    e.write(content)
            
            print("已完成%d/%d人，占%f%%,用时%s"%(peo_num-l+1 , r - l + 1, (peo_num-l+1)*100/(r - l + 1),get_time(time.time()-startTime)))
            time.sleep(0.5)
        except Exception as e:
            print(e)
            Error_id.append((id,word))

for i in Error_id:
    print(i)