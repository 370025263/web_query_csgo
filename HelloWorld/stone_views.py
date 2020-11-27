import json
import time
from django.shortcuts import render
import a2s
from django.http import HttpResponse
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO
from matplotlib.pyplot import MultipleLocator


def status(request):
    try:
        out = {}
        ip = request.GET.get("ip")
        port = request.GET.get("port")
        if not port:
            port = 27015
        address = (str(ip), int(port))
        info = a2s.info(address)

        out['time']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        out['map'] = info.map_name
        out['server_name'] = info.server_name
        out['player_num'] = str(info.player_count)
        out_json = json.dumps(out)
        return HttpResponse(out_json, content_type='application/json')

    except Exception:
        out = {}
        out['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        out['map'] = None
        out['server_name'] = None
        out['player_num'] = None
        out_json = json.dumps(out)
        return HttpResponse(out_json, content_type='application/json')



def get_picture(request):
    x,y=[],[]
    with  open("/home/stone/pytorch_project/gym/mini_game/record.txt" , 'r') as record:
        for line in record:
            line = line.strip()
            line_s = line.split(",")
            x.append(float(line_s[0]))
            y.append(float(line_s[1]))
    #设置坐标轴范围
    # plt.xlim(0,len(x) )
    # plt.ylim(0, 15000 )
    #设置坐标轴名称
    plt.switch_backend('agg')
    plt.scatter(x,y,s=2)
    plt.xlabel('训练episode')
    plt.ylabel('终止距离')
    x_major_locator=MultipleLocator(int(len(x)/10))
    #把x轴的刻度间隔设置为1，并存在变量里
    y_major_locator=MultipleLocator(5)
    #把y轴的刻度间隔设置为10，并存在变量里
    ax=plt.gca()
    #ax为两条坐标轴的实例
    ax.xaxis.set_major_locator(x_major_locator)
    #把x轴的主刻度设置为1的倍数
    ax.yaxis.set_major_locator(y_major_locator)
    #把y轴的主刻度设置为10的倍数
    plt.xlim(-0.5,len(x))
    #把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
    plt.ylim(-5,110)
    #把y轴的刻度范围设置为-5到110，同理，-5不会标出来，但是能看到一点空白
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    context = {
        'img': imd,
    }
    return render(request,'./test.html',context)



