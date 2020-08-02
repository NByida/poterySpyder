#!/usr/bin/python
# -*- coding: utf-8 -*-
import _thread
import re
import ssl
import threading
import urllib.request
from bs4 import BeautifulSoup as BS
import peewee

from shici import Database

ssl._create_default_https_context = ssl._create_unverified_context
agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.1.2.3000 Chrome/55.0.2883.75 Safari/537.36'
headersAtHome = {
    'User-Agent': agent,
    # 'X-Requested-With': 'XMLHttpRequest',
    # "Cookie":"fpid_sa=null; PHPSESSID=jfdgva5m9g4mi75bcqv2nm7227; lang=zh; feid=03c1a79df4c0f65ca1c825dce3f24702; feid_sa=null; fpid=53b72efc6b9c8fd2df3d055be149c48e; xfeid=87aea5cdb4af154c93739691f69716fb; _ym_uid=1554907281660967363; _ym_d=1554907281; locale=en"
}
hosturl = "https://www.xzslx.net"

db = Database({'db': 'new_schema',
               'engine': 'peewee.MySQLDatabase',
               'user': 'root',
               'host': 'localhost',
               'charset': 'utf8',
               'use_unicode': True,
               'port': 3306,
               'passwd': 'root'})


# 爬取页面历史
class History(db.Model):
    class Meta:
        db_table = 'history'

    id = peewee.PrimaryKeyField()
    history_url = peewee.TextField(default='url')
    success = peewee.BooleanField()


History.create_table()


class Poetry(db.Model):
    class Meta:
        db_table = 'poetry'

    id = peewee.PrimaryKeyField()
    # 诗词内容
    content = peewee.TextField()
    # 诗词翻译
    translate = peewee.TextField()
    # 诗词注释
    notes = peewee.TextField()
    # 诗词赏析
    notes = peewee.TextField()
    # 诗词赏析
    appreciation = peewee.TextField()
    # 诗词拼音
    pinyin = peewee.TextField()
    # 诗名
    name = peewee.TextField()
    # 朝代
    dynasty = peewee.TextField()
    # 诗人
    poet = peewee.TextField()
    linkId = peewee.TextField()


Poetry.create_table()


class Tag(db.Model):
    class Meta:
        db_table = 'tag'
        id = peewee.PrimaryKeyField()
        name = peewee.TextField()

    petoryid = peewee.IntegerField()
    tag = peewee.TextField()


Tag.create_table()


# 大类
class WordsLabel(db.Model):
    class Meta:
        db_table = 'words_label'
        id = peewee.PrimaryKeyField()

    label_name = peewee.TextField()
    tag = peewee.TextField()


WordsLabel.create_table()


# 小类
class WordsType(db.Model):
    class Meta:
        db_table = 'words_type'
        id = peewee.PrimaryKeyField()

    label_id = peewee.IntegerField()
    label_name = peewee.TextField()
    type = peewee.TextField()
    url = peewee.TextField()
    lastpage = peewee.IntegerField()


WordsType.create_table()


class Words(db.Model):
    class Meta:
        db_table = 'words'
        id = peewee.PrimaryKeyField()

    label_name = peewee.TextField()
    type = peewee.TextField()
    words = peewee.TextField()
    # 诗名
    name = peewee.TextField()
    # 朝代
    dynasty = peewee.TextField()
    # 诗人
    poet = peewee.TextField()
    linkId = peewee.TextField()


Words.create_table()


def getEveryPoet(s):
    result = s.split("tandzz")
    for a in result:
        if ("onview conview_main show" in a):
            patern = re.compile(r'conview conview_main show"><div>(.*?)</div>', re.S)
            r = patern.findall(a)

            content = ''
            translate = ''
            notes = ''
            appreciation = ''
            pinyin = ''
            dynasty = ''
            poet = ''
            linkId = ''
            name = ''

            if (len(r) > 0):
                result = r[0].replace("<br> <br>", "")
                result = result.replace("<br> '", "")
                content = result

            # 诗词翻译
            patern1 = re.compile(r'conview conview_yi"><div>(.*?)</div>', re.S)
            r1 = patern1.findall(a)
            if (len(r1) > 0):
                result1 = r1[0].replace("<br> <br>", "")
                result1 = result1.replace("<br> '", "")
                translate = result1
                # print(result1)

            # 诗词注释
            patern2 = re.compile(r'conview conview_zhu"><div>(.*?)</div>', re.S)
            r2 = patern2.findall(a)
            if (len(r2) > 0):
                result2 = r2[0].replace("<br> <br>", "")
                result2 = result2.replace("<br> '", "")
                notes = result2
                # print(result2)

            # 诗词赏析
            patern3 = re.compile(r'conview conview_shang"><div>(.*?)<br></div></div>', re.S)
            r3 = patern3.findall(a)
            if (len(r3) > 0):
                result3 = r3[0].replace("<br> <br>", "")
                result3 = result3.replace("<br> '", "")
                appreciation = result3
                # print(result3)

            # 诗词拼音
            patern4 = re.compile(r'conview conview_pin"(.*?)</b></div></div>', re.S)
            r4 = patern4.findall(a)
            if (len(r4) > 0):
                result4 = r4[0].replace("<br> <br>", "")
                result4 = result4.replace("<br> '", "")
                pinyin = result4
                # print(result4)
                # print('/n')

            # 诗名

            # '">\n<div class="t"><a href="/shi/45385.html" target=_blank>赠妻诗</a></div>\n<div class="zz">\n<span>唐代</span>\n<span>唐晅</span>\n<span></span>\n</div>\n</div>\n']

            patern5 = re.compile(r'^(.*?)<div class="btnbox">', re.S)
            r5 = patern5.findall(a)
            if (len(r5) > 0):
                result5 = r5[0].replace("<br> <br>", "")
                result5 = result5.replace("<br> '", "")
                patern6 = re.compile(r'target=_blank>(.*?)</a>', re.S)
                paternid = re.compile(r'a href="/shi/(.*?).html', re.S).findall(result5)
                if (len(paternid) > 0):
                    linkId = paternid[0]
                title = patern6.findall(result5)
                # 诗名
                if (len(title) > 0):
                    titlename = title[0]
                    name = titlename.replace("-古诗文网", "")

                if (len(Poetry.select().where(Poetry.linkId == linkId)) > 0):
                    print("跳过-------->" + name)

                # 朝代
                patern6 = re.compile(r'<span>(.*?)</span>', re.S)
                dentisy = patern6.findall(result5)
                if (len(dentisy) > 0):
                    dentisyname = dentisy[0]
                    dynasty = dentisyname
                    # print(dentisy[0])

                # 诗人
                if (result5.find("shiren") > -1):
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

                # p=Poetry(translate=1,content=1,dynasty=1,poet=poet,name=name,pinyin=1,appreciation=1,notes=1)            poetId = -1            if len(Poetry.select().where(Poetry.name == name)) == 0:
                p = Poetry(translate=translate, content=content, dynasty=dynasty, poet=poet, name=name, pinyin=pinyin,
                           appreciation=appreciation, notes=notes, linkId=linkId)
                print("save-------------------" + name)
                p.save()
                poetId = p.id

            # tag
            patern8 = re.compile(r'ziliao">(.*?)</div', re.S)
            tag = patern8.findall(a)

            if (len(tag) > 0):
                tagSplit = tag[0].split("\n")
                if (len(Tag.select().where(Tag.petoryid == poetId)) == 0):
                    for tags in tagSplit:
                        tags = tags.replace("，", "")
                        name = Tag(petoryid=poetId, tag=tags, name=name)
                        name.save()
        # else:
        # print("没有故事-----------------------------------")
    if len(result) == 0:
        print("result ==0  没有故事-----------------------------------")


def getMoudle(url, name, num):
    # url=gushi / 0 / 0 / 0 / 68 / 0 / 0 /
    # https: // www.xzslx.net / gushi / 0 / 0 / 0 / 0 / 0 / 1 /
    myurl = url.strip(" ")[:-2]
    page = num
    # 没爬取过该页面

    try:
        successnum = len(History.select().where(
            (History.history_url == hosturl + myurl + str(page) + "/") & (History.success == True)))
        if (successnum > 0):
            print("跳过该页--" + url + str(page) + "/")
            return
        else:
            urlresult = myurl + str(page);
            print(hosturl + urlresult + "/")
            r = urllib.request.urlopen(hosturl + urlresult + "/").read().decode('utf-8', errors='ignore')
            history = History(history_url=hosturl + urlresult + "/", success=True)
            print("History success    " + history.history_url)
            getEveryPoet(r)
            if len(History.select().where((History.history_url == hosturl + myurl + str(page) + "/"))) == 0:
                history.save()
            else:
                History.update(success=True).where(History.history_url == hosturl + myurl + str(page) + "/").execute()

    except:
        if len(History.select().where(History.history_url == hosturl + myurl + str(num + 1) + "/")) == 0:
            history = History(history_url=hosturl + myurl + str(num + 1) + "/", success=False)
            print("History failed save" + history.history_url)
            history.save()
        else:
            print("History failed skip save" + hosturl + myurl + str(num + 1) + "/")


def addpage():
    addurl = hosturl
    # urllib.request.urlopen(addurl).read()
    r = urllib.request.urlopen(addurl).read().decode('utf-8', errors='ignore')
    # class ="mask" > < p class ="f_12 clr_f" > 高中文言文主要整理了包括过秦论、兰亭集序、归去来兮辞、劝学 《荀子》、邹忌讽齐王纳谏 《战国策》、师说 韩愈、阿房宫赋等古...< / p > < div class ="al_ct" > < a href="/gushi/0/0/0/66/0/0/" class ="f_12" target="_blank" rel="nofollow" > 点击阅读 < / a > < / div > < / div > < p > < img src="/css/xgaozhongwenyanwen.gif.pagespeed.ic.ZfMHIBOryP.png" class ="dis_b" alt="高中文言文" / > < / p > < div class ="zhuanj_text f_16" > < a href="/gushi/0/0/0/66/0/0/" class =" fl" target="_blank" > 高中文言文 < / a > < span class ="f_12 ver_mid clr_qianh fr" > 26首 < / span > < div class ="cls" > < / div > < / div > < / li >
    # pattern2 = re.compile(r'f_12 clr_f(.*?)首', re.S)
    pattern2 = re.compile(r'png" class="dis_b" alt=(.*?)" class=" fl" target="_blank">', re.S)
    result = pattern2.findall(r)
    for a in result:
        name = re.match(r'"(.*?)"/><.*?a href="/(.*?)$', a, re.M | re.I);
        # print(name.group(1))
        # print(name.group(2))
        getMoudle(name.group(2), name.group(1), 0)


def mutiThred(start, end):
    for i in range(start, end - 1):
        getMoudle("gushi/0/0/0/0/0/0/", "古诗", i)


def retryUrl(failedlist, start, end):
    for i in range(start, end - 1):
        try:
            r = urllib.request.urlopen(failedlist[i].history_url).read().decode('utf-8', errors='ignore')
            History.update(success=True).where(History.history_url == failedlist[i].history_url).execute()
            print("重试成功" + failedlist[i].history_url)
            getEveryPoet(r)
        except:
            print("重试失败" + failedlist[i].history_url)


def start():
    thread = 1000
    for i in range(1, 6000, thread):
        threading.Thread(target=mutiThred, args=(i, i + thread)).start()


# 重新请求失败的url
def retry():
    failedlist = History.select().where(History.success == False)
    for index in range(0, len(failedlist), 50):
        threading.Thread(target=retryUrl, args=(failedlist, index, index + 50)).start()


retry()
# start()
# ---------------------------------------------------------------------------------------

def getJuzi():
    addurl = hosturl + "mingju/"
    print(addurl)
    r = urllib.request.urlopen(addurl).read().decode('utf-8', errors='ignore')
    for link in BS(r, "html.parser").find_all("a"):
        if not (link.get('href') is None):
            if link.get('href').find('/mingju/') != -1:
                text = link.get_text()
                if text.isalpha() and text.find("页") == -1 and text.find("不限") == -1 and text.find("名句") == -1:
                    # print(link.get('href') + link.get_text())
                    wordsLabel = WordsLabel(label_name=link.get_text(), tag="")
                    wordsLabel.save()
                    getJuPage(link.get('href'), wordsLabel.id, wordsLabel.label_name)


def getJuPage(url, id, label_name):
    addurl = hosturl + url
    print(addurl)
    r = urllib.request.urlopen(addurl).read().decode('utf-8', errors='ignore')
    for link in BS(r, "html.parser").find_all("a"):
        if not (link.get('href') is None):
            if link.get('href').find(url[0:10]) != -1:
                text = link.get_text()
                if text.isalpha() and text.find("页") == -1 and text.find("不限") == -1 and text.find("名句") == -1:
                    print(link.get('href') + link.get_text())
                    wordstype = WordsType(label_id=id, label_name=label_name, type=link.get_text(),
                                          url=link.get('href'))
                    wordstype.save()


# getJuzi()


def saveWord(worldType, name,poet,id,words):
    if len(Words.select().where(Words.words == words)) == 0:
        word = Words(label_name=worldType.label_name,
                     type=worldType.type,
                     words=words,
                     name=name,
                     dynasty="",
                     poet=poet,
                     linkId=id
                     )
        word.save()
        print(worldType.type+"----"+name+"----"+poet+"----"+id+"-------"+words)
    else:
        print("jump "+name)

# 获取分类的页码末页
def getlastpage():
    for worldType in WordsType.select():
        addurl = hosturl + worldType.url
        r = urllib.request.urlopen(addurl).read().decode('utf-8', errors='ignore')
        patern = re.compile(r'共(.*?)首名句', re.S)
        res = patern.findall(r)
        num=1
        if (len(res) > 0) and not (res is None) and res[0].isdigit():
            page=int(res[0])
            if(page<20):
                print(worldType.type+"页码为1")
                num = 1
            else:
                if(page%15==0):
                    print(worldType.type+"页码为"+str(int(page/15)))
                    num = int(page/15)
                else:
                    print(worldType.type + "页码为" + str(int(page/15+1)))
                    num = int(page/15)+1
        else:
            print(worldType.type+"页码为1")
            num = 1
        WordsType.update(lastpage=num).where(WordsType.id == worldType.id).execute()

# 自动保存爬取历史
def requestNet(url):
    try:
        successnum = len(History.select().where(
            (History.history_url == url) & (History.success == True)))
        if (successnum > 0):
            print("跳过该页--" + url )
            return ""
        else:
            r = urllib.request.urlopen(url).read().decode('utf-8', errors='ignore')

            history = History(history_url=url, success=True)
            if len(History.select().where((History.history_url == url))) == 0:
                history.save()
            else:
                History.update(success=True).where(History.history_url ==url).execute()
            return r
    except:
        if len(History.select().where(History.history_url == url)) == 0:
            history = History(history_url=url, success=False)
            print("History failed save" + history.history_url)
            history.save()
        else:
            print("History failed skip save" + url)
        return ""


# 获取分类下的所有诗句
def getword():
    for worldType in WordsType.select():
        lastpage=worldType.lastpage
        for i in range(1,lastpage+1):
            addurl = hosturl + worldType.url[:-2]+str(i)+"/"
            r =requestNet(addurl)
            if len(r)==0:
                break
            juzi = "﻿<!DOCTYPE html><html>" + str(
                BS(r, "html.parser").find_all('ul', class_='mingju')[0]) + "</body></html>"
            if juzi is None:
                print(addurl + " is null,please check")
            else:
                name = ""
                poet = ""
                woed = ""
                id = ""
                for li in BS(juzi, "html.parser").find_all("li"):
                    lihtml = "﻿<!DOCTYPE html><html>" + str(li) + "</body></html>"
                    for herf in BS(lihtml, "html.parser").find_all("a"):
                        if herf.get('href').startswith("/ju"):
                            woed = herf.get_text()
                        if herf.get('href').startswith("/shi/"):
                            patern = re.compile(r'/shi/(.*?).html', re.S)
                            r = patern.findall(herf.get('href'))
                            if (len(r) > 0) and not (r is None):
                                id = r[0]
                            else:
                                id = ""
                            name = herf.get_text()
                        if herf.get('href').startswith("/shiren"):
                            poet = herf.get_text()
                    saveWord(worldType, name, poet, id, woed)
                    name = ""
                    poet = ""
                    woed = ""
                    id = ""
# getlastpage()
# getword()
