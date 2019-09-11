#!/usr/bin/python
# -*- coding: utf-8 -*-

import ssl
import re
import urllib.request
import peewee



import ssl
import re



from shici import Database

ssl._create_default_https_context = ssl._create_unverified_context
agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.1.2.3000 Chrome/55.0.2883.75 Safari/537.36'
headersAtHome = {
'User-Agent':agent,
# 'X-Requested-With': 'XMLHttpRequest',
# "Cookie":"fpid_sa=null; PHPSESSID=jfdgva5m9g4mi75bcqv2nm7227; lang=zh; feid=03c1a79df4c0f65ca1c825dce3f24702; feid_sa=null; fpid=53b72efc6b9c8fd2df3d055be149c48e; xfeid=87aea5cdb4af154c93739691f69716fb; _ym_uid=1554907281660967363; _ym_d=1554907281; locale=en"
         }
hosturl = "https://www.xzslx.net/"

db = Database({'db':'new_schema',
                'engine':'peewee.MySQLDatabase',
                'user':'yida1',
                'host':'localhost',
                'charset': 'utf8',
                'use_unicode': True,
                'port':3306,
                'passwd':'yida'})

# 爬取页面历史
class History(db.Model):
    class Meta:
        db_table = 'history'
    id = peewee.PrimaryKeyField()
    history_url=peewee.TextField(default='url')

History.create_table()


class Poetry(db.Model):
    class Meta:
        db_table = 'poetry'
    id = peewee.PrimaryKeyField()
    # 诗词内容
    content =  peewee.TextField()
    # 诗词翻译
    translate = peewee.TextField()
    # 诗词注释
    notes = peewee.TextField()
    #诗词赏析
    notes =  peewee.TextField()
    # 诗词赏析
    appreciation = peewee.TextField()
    # 诗词拼音
    pinyin = peewee.TextField()
    # 诗名
    name =  peewee.TextField()
    # 朝代
    dynasty = peewee.TextField()
    # 诗人
    poet =  peewee.TextField()
Poetry.create_table()

class Tag(db.Model):
    class Meta:
        db_table = 'tag'
        id = peewee.PrimaryKeyField()
        name=peewee.TextField()
    petoryid = peewee.IntegerField()
    tag =  peewee.TextField()
Tag.create_table()

def getEveryPoet(s):
    result=s.split("tandzz")
    for a in result:
        if("onview conview_main show" in a):
            # 诗词内容
            global  content
            global translate
            global notes
            global appreciation
            global pinyin
            global name
            global dynasty
            global poet
            global poetId

            content = ''
            translate = ''
            notes = ''
            appreciation = ''
            pinyin = ''
            name = ''
            dynasty = ''
            poet = ''

            patern=re.compile(r'conview conview_main show"><div>(.*?)</div>',re.S)
            r=patern.findall(a)
            if(len(r)>0):
                result = r[0].replace("<br> <br>", "")
                result = result.replace("<br> '", "")
                content = result

            # 诗词翻译
            patern1 = re.compile(r'conview conview_yi"><div>(.*?)</div>', re.S)
            r1 = patern1.findall(a)
            if(len(r1)>0):
                result1 = r1[0].replace("<br> <br>", "")
                result1 = result1.replace("<br> '", "")
                translate=result1
                #print(result1)

            # 诗词注释
            patern2 = re.compile(r'conview conview_zhu"><div>(.*?)</div>', re.S)
            r2 = patern2.findall(a)
            if(len(r2)>0):
                result2 = r2[0].replace("<br> <br>", "")
                result2 = result2.replace("<br> '", "")
                notes=result2
                #print(result2)

            # 诗词赏析
            patern3 = re.compile(r'conview conview_shang"><div>(.*?)<br></div></div>', re.S)
            r3 = patern3.findall(a)
            if (len(r3) > 0):
                result3 = r3[0].replace("<br> <br>", "")
                result3 = result3.replace("<br> '", "")
                appreciation=result3
                # print(result3)

            # 诗词拼音
            patern4 = re.compile(r'conview conview_pin"(.*?)</b></div></div>', re.S)
            r4= patern4.findall(a)
            if (len(r4) > 0):
                result4 = r4[0].replace("<br> <br>", "")
                result4 = result4.replace("<br> '", "")
                pinyin=result4
                # print(result4)
                # print('/n')

            # 诗名


       # '">\n<div class="t"><a href="/shi/45385.html" target=_blank>赠妻诗</a></div>\n<div class="zz">\n<span>唐代</span>\n<span>唐晅</span>\n<span></span>\n</div>\n</div>\n']

            patern5 = re.compile(r'^(.*?)<div class="btnbox">', re.S)
            r5 = patern5.findall(a)
            if (len(r5) > 0):
                result5 = r5[0].replace("<br> <br>", "")
                result5 = result5.replace("<br> '", "")
                patern6=re.compile(r'target=_blank>(.*?)</a>', re.S)
                title=patern6.findall(result5)
                # 诗名
                if(len(title)>0):
                    titlename=title[0]
                    name = titlename.replace("-古诗文网", "")
                    print(name)
                if (len(Poetry.select().where(Poetry.name == name))>0):
                    print("跳过-------->"+name)
                    continue
                # 朝代
                patern6 = re.compile(r'<span>(.*?)</span>', re.S)
                dentisy = patern6.findall(result5)
                if (len(dentisy) > 0):
                    dentisyname=dentisy[0]
                    dynasty = dentisyname
                    # print(dentisy[0])

                #诗人
                if(result5.find("shiren")>-1):
                    patern7 = re.compile(r'<span><A href="/shiren/.*?.html" target=_blank>(.*?)$', re.S)
                    author = patern7.findall(result5)
                    if (len(author) > 0):
                        authorname = author[0]
                        poet = authorname
                        # print(authorname)
                else:
                    patern7 = re.compile(r'<span>.*?</span>.*?<span>(.*?)</span>', re.S)
                    author = patern7.findall(result5)
                    if (len(author) > 0):
                        authorname = author[0]
                        poet = authorname

                if (poet.find("</") > -1):
                    patern10 = re.compile(r'^(.*?)</', re.S)
                    author1 = patern10.findall(poet)
                    if (len(author1) > 0):
                        poet = author1[0]
            # p=Poetry(translate=1,content=1,dynasty=1,poet=poet,name=name,pinyin=1,appreciation=1,notes=1)
            poetId = -1
            if (len(Poetry.select().where(Poetry.name == name)) == 0):
                p = Poetry(translate=translate, content=content, dynasty=dynasty, poet=poet, name=name, pinyin=pinyin,appreciation=appreciation, notes=notes)
                p.save()
                poetId = p.id

            content = ''
            translate = ''
            notes = ''
            appreciation = ''
            pinyin = ''

            dynasty = ''
            poet = ''

            # tag
            patern8 = re.compile(r'ziliao">(.*?)</div', re.S)
            tag = patern8.findall(a)


            if (len(tag) > 0):
                tagSplit=tag[0].split("\n")
                if (len(Tag.select().where(Tag.petoryid == poetId)) == 0):
                    for tags in tagSplit:
                        tags=tags.replace("，", "")
                        name=Tag(petoryid=poetId,tag=tags,name=name)
                        name.save()


def getMoudle(url,name,num):
    # url=gushi / 0 / 0 / 0 / 68 / 0 / 0 /
    # https: // www.xzslx.net / gushi / 0 / 0 / 0 / 0 / 0 / 1 /
    myurl=url.strip(" ")[:-2]
    page=num
    # 没爬取过该页面
    if(len(History.select().where(History.history_url==hosturl +myurl + str(page)+ "/"))==0):
        urlresult = myurl + str(page);
        print(hosturl + urlresult + "/")
        r = urllib.request.urlopen(hosturl + urlresult + "/").read().decode('utf-8', errors='ignore')

        history = History(history_url=hosturl + urlresult + "/")
        history.save()

        print("start" + name + "page:" + str(num)+"progress:"+str(num/5793))
        getEveryPoet(r)
        if ("下一页" in r):
            try:
                getMoudle(url, name, num + 1)
            except:
                getMoudle(url, name, num + 1)
    # 爬取过该页面,下一页
    else:
        print("跳过该页--"+url+str(page)+ "/")
        getMoudle(url, name, num + 1)


def addpage():
        addurl = hosturl
        # urllib.request.urlopen(addurl).read()
        r =urllib.request.urlopen(addurl).read().decode('utf-8', errors='ignore')
        # class ="mask" > < p class ="f_12 clr_f" > 高中文言文主要整理了包括过秦论、兰亭集序、归去来兮辞、劝学 《荀子》、邹忌讽齐王纳谏 《战国策》、师说 韩愈、阿房宫赋等古...< / p > < div class ="al_ct" > < a href="/gushi/0/0/0/66/0/0/" class ="f_12" target="_blank" rel="nofollow" > 点击阅读 < / a > < / div > < / div > < p > < img src="/css/xgaozhongwenyanwen.gif.pagespeed.ic.ZfMHIBOryP.png" class ="dis_b" alt="高中文言文" / > < / p > < div class ="zhuanj_text f_16" > < a href="/gushi/0/0/0/66/0/0/" class =" fl" target="_blank" > 高中文言文 < / a > < span class ="f_12 ver_mid clr_qianh fr" > 26首 < / span > < div class ="cls" > < / div > < / div > < / li >
        # pattern2 = re.compile(r'f_12 clr_f(.*?)首', re.S)
        pattern2 = re.compile(r'png" class="dis_b" alt=(.*?)" class=" fl" target="_blank">', re.S)
        result = pattern2.findall(r)
        for a in result:
            name=re.match(r'"(.*?)"/><.*?a href="/(.*?)$',a, re.M|re.I);
            # print(name.group(1))
            # print(name.group(2))
            getMoudle(name.group(2),name.group(1),0)
# addpage()
getMoudle("gushi/0/0/0/0/0/0/","古诗",5401)

