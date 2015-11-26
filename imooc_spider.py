#-*_coding:utf8-*-
import requests
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class spider(object):
    def __init__(self):
        print 'Spider Starts...'

    def getsource(self,url):
        html = requests.get(url)
        return html.text

    def changepage(self,url,total_page):
        now_page = int(re.search('page=(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(now_page, total_page+1):
            link = re.sub('page=\d+','page=%s'%i,url,re.S)
            page_group.append(link)
        return page_group

    def geteveryclass(self,source):
        everyclass = re.findall('<li class="course-one">(.*?)</li>',source,re.S)
        return everyclass

    def getinfo(self,eachclass):
        info = {}
        info['title'] = re.search('<span>(.*?)</span>',eachclass,re.S).group(1)
        info['content'] = re.search('"text-ellipsis">(.*?)</p>',eachclass,re.S).group(1)
        timeandlevel = re.search('"time-label">(.*?)</span>',eachclass,re.S).group(1).split("|")
        info['classtime'] = timeandlevel[0]
        info['classlevel'] = timeandlevel[1]
        learnnum_full = re.search('<span class="l ml20">(.*?)</span>',eachclass,re.S).group(1)
        info['learnnum'] = re.findall(r'\d+', learnnum_full, re.S)[0]
        return info

    def saveinfo(self,classinfo):
        f = open('info.txt','a')
        for each in classinfo:
            f.writelines('title:' + each['title'] + '\n')
            f.writelines('content:' + each['content'] + '\n')
            f.writelines('classtime:' + each['classtime'].strip(' \t\n\r') + '\n')
            f.writelines('classlevel:' + each['classlevel'].strip(' \t\n\r') + '\n')
            f.writelines('learnnum:' + each['learnnum'].strip(' \t\n\r') + '\n\n')
        f.close()


if __name__ == '__main__':

    classinfo = []
    url = 'http://www.imooc.com/course/list?page=1'
    coursespider = spider()
    all_links = coursespider.changepage(url,23)
    for link in all_links:
        print 'loading: ' + link
        html = coursespider.getsource(link)
        everyclass = coursespider.geteveryclass(html)
        for each in everyclass:
            info = coursespider.getinfo(each)
            classinfo.append(info)
    coursespider.saveinfo(classinfo)
            
        
