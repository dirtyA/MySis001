#coding=utf-8

import sys;
import mysql;
import mysql.connector;
import requests;
import re;
import json;
import threading;
import time;
from bs4 import BeautifulSoup as bs;
import requests;
from ThreadPool import ThreadPool as Pool;
import random;
import traceback;

#线程池(线程个数)
pool = Pool(5);
#页面抓取失败时进行重试的次数
RETRY_TIMES = 10;
HOST = "127.0.0.1";
PORT = "3306";
USER = "sis001";
PWD = "sis001";
DBNAME = "SisDB";
#页面抓取延迟时间, 不想延迟可以直接改0
TIME_DELAY = [0, 15];
#页面拉取失败时, 暂停时间
ERR_TIME_SLEEP = [5, 30];
TAG_EXCLUDE = ["版务"];

#地址与数据库表映射
#TBName->URL
URL_MAP = {
    "original":"http://www.sis001.com/forum/forum-143-{0}.htm",
    "reprint":"http://www.sis001.com/forum/forum-25-{0}.html",
    "c_original":"http://sis001.com/forum/forum-230-{0}.html",
    "c_reprint":"http://sis001.com/forum/forum-58-{0}.html"
};

headers = {
    "Referer":"http://www.sis001.com/forum/index.php",
    "User-Agent":"Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.122 Mobile Safari/537.36"
};      

RE_COMMENT_VIEW_FETCH = re.compile("\s*(\d+)\s*/\s*(\d+)\s*"); 
RE_FIND_STORAGE = re.compile("\s*([0-9\.]+)\s*([A-Za-z]*)\s*");

def transToMB(vStor):
    num, string = RE_FIND_STORAGE.findall(vStor)[0];
    if(string == "GB" or string == "G"):
        num = float(num) * 1024;
    return int(float(num));
        
def getPageText(url):
    text = "";
    for i in range(RETRY_TIMES):
        try:
            req = requests.get(url, headers = headers);
            req.encoding = "gbk";
            text = req.text;
            break;
        except Exception as e:
            print("Request failed, except:{0}".format(str(e)));
            time.sleep(random.randint(ERR_TIME_SLEEP[0], ERR_TIME_SLEEP[1]));
    return text;
    
def parseCommentViewString(tString):
    comment = 0;
    view = 0;
    try:
        sc, sv = RE_COMMENT_VIEW_FETCH.findall(tString)[0];
        comment = int(sc);
        view = int(sv);
    except Exception as e:
        print("Parse comment, view failed, string:{0}, except:{1}".format(tString, str(e)));
    return comment, view;
    
def parseCapVideoTypeString(tString):
    tString = tString.strip();
    storage = 0;
    vType = "";
    try:
        if("/" in tString):
            tStor, tType = tString.split("/", 1);
            vType = tType.strip();
            storage = transToMB(tStor);
        elif(len(tStirng) == 0):
            pass;
        elif(tString[0].isalpha()):
            vType = tString;
    except Exception as e:
        print("Catch exception, except:{0}, string:{1}".format(str(e), tString));
    return storage, vType;
    
def fetch(*args):
    time.sleep(random.randint(TIME_DELAY[0], TIME_DELAY[1]));
    soup = bs(getPageText(args[1]), "html.parser");
    items = soup.find_all("tbody");
    conn, cursor = createConnection();
    count = 0;
    print("Record count:{0}".format(len(items)));
    for item in items:
        try:
            tag = "";
            try:
                tag = item.tr.th.em.a.text;
            except:
                pass;
            if(tag in TAG_EXCLUDE):
                continue;
            tid = item.tr.th.span["id"];
            title = item.tr.th.span.a.text.replace("'", "");
            #parse comment, view
            comment, view = parseCommentViewString(
                item.tr.find("td", attrs = {"class":"nums"}).text
            );
            capacity, videoType = parseCapVideoTypeString(
                item.tr.find_all("td", attrs = {"class":"nums"})[1].text
            );
            postTime = "";
            try:
                postTime = item.tr.find("td", class_ = "author").em.text;
            except Exception as e:
                print("Catch exception, except:{0}".format(str(e)));
            url = item.tr.a["href"];
            
            #insert to mysql
            sql = "insert into {0}(tid, tag, title, url, posttime, capacity, videotype, view, comment) values('{1}', '{2}', '{3}', '{4}', '{5}', {6}, '{7}', {8}, {9})".format(
                args[0], 
                tid, 
                tag, 
                title,
                url,
                postTime, 
                capacity,
                videoType,
                view,
                comment
            );
            #print("SQL:{0}".format(sql));
            cursor.execute(sql);
            count = count + 1;
        except mysql.connector.errors.IntegrityError as e:
            pass;
        except Exception as e:
            print("Exception catch, except:{0}".format(str(e)));
            print(traceback.format_exc());
    
    cursor.close();
    conn.commit();
    conn.close();
    print("Insert into db count:{0}".format(count));
    
def showHelp():
    print("python My1024.py {count | start, end}");
    sys.exit(0);
    
def createConnection():
    conn = None;
    cursor = None;
    while(True):
        try:
            conn = mysql.connector.Connect(host = HOST, port = PORT, user = USER, passwd = PWD, db = DBNAME, charset = "utf8");
            cursor = conn.cursor();
            break;
        except Exception as e:
            print("Connect to mysql failed, exception:{0}".format(str(e)));
            time.sleep(15);
    return conn, cursor;
    
def fetchOutSide(start, end):
    for i in range(start, end):
        for tbName in URL_MAP.keys():
            pool.addTask(fetch, tbName, URL_MAP[tbName].format(i));
            #fetch(tbName, URL_MAP[tbName].format(i));
        if(i % 10 == 0):
            time.sleep(10);
    
def main():
    start = 1;
    end = 2;
    if(len(sys.argv) == 3):
        print("Got args, start = {0}, end = {1}".format(sys.argv[1], sys.argv[2]));
        try:
            start = int(sys.argv[1]);
            end = int(sys.argv[2]);
        except:
            print("Parse args failed, use default");
    elif(len(sys.argv) == 2):
        print("Got args, count = {0}".format(sys.argv[1]));
        try:
            end = start + int(sys.argv[1]);
        except:
            print("Parse args failed, use default");
    elif(len(sys.argv) > 3):
        showHelp();
    pool.start();
    fetchOutSide(start, end);
    pool.shutdown();
    
if(__name__ == "__main__"):
    main();
