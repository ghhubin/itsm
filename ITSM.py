# -*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib
import httplib
import re
import string
import datetime

class ITSM:
    def __init__(self):
    	self.SiteIPandPort = '192.168.0.1:7001'
    	self.username = 'uuuuu'
    	self.passwd = 'ppppppppppppppppp'
    	self.cookie = cookielib.CookieJar()
    	self.jobIDs_str = ''
        self.headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
                   'Accept': 'text/html, application/xhtml+xml, */*',
                   'Accept-Language': 'zh-CN',
                   'Referer': 'http://192.168.0.1:7001/index.jsp',
                   'Content-Type': 'text/xml; charset=UTF-8',
                   'Pragma': 'no-cache'}
        self.ndaysago = 200
        self.beginDate = (datetime.datetime.now() - datetime.timedelta(days=self.ndaysago)).strftime("%Y-%m-%d")
        self.endDate = datetime.datetime.now().strftime("%Y-%m-%d")

        if self.login() != 0:
            print u'网站登陆错误!'.encode('gbk', 'ignore')
        

    def login(self):
        url = 'http://'+self.SiteIPandPort+'/j_security_check?flag=1'
        data = '<UserInfo forceLogin="-1" autoLogin="0" loginType="0" isAllowUnSys="false">\<j_username>'\
            + self.username +'</j_username><j_password>'\
            + self.passwd + '</j_password></UserInfo>'
                        
        handler = urllib2.HTTPCookieProcessor(self.cookie)
        opener = urllib2.build_opener(handler)
        req = urllib2.Request(url,headers=self.headers)
        try:
            response = opener.open(req,data,timeout=15)
            #for item in self.cookie:
            #    print 'Name = '+item.name
            #    print 'Value = '+item.value
            #print response.getcode()
            #print response.read()
        except Exception, e:
            print e
            return -1
        return 0
    

    def getJobID(self):
        page = ''
        data = '<root><result id="111100002" key="111100002" ref="sqlResult" hasField="0" filedsearch="" excelTitle="">'\
             + '<param name="V_JOB_NAME" type="STRING" isMultiple="0BF"></param>'\
             + '<param name="V_JOB_CYCLE" type="STRING" isMultiple="0BF"></param>'\
             + '<param name="V_EXEC_STAFF_ID" type="STRING" isMultiple="0BF"></param>'\
             + '<param name="V_REGION_ID" type="STRING" isMultiple="0BF"></param>'\
             + '<param name="BEGIN_DATE" type="STRING" isMultiple="0BF">' + self.beginDate + '</param>'\
             + '<param name="END_DATE" type="STRING" isMultiple="0BF">' + self.endDate + '</param>'\
             + '</result></root>'
         
        url = 'http://'+self.SiteIPandPort+'/servlet/result.do?method=getEncodeResultXml&getType=FORCE'
        #print values
        try:
            req = urllib2.Request(url,headers=self.headers)
            #利用urllib2的build_opener方法创建一个opener
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
            response = opener.open(req,data,timeout=15)
            # print response.status
            # print response.reason
            # print response.getheaders()
            page = response.read()
            print page
        except Exception, e:
            print e
            return -1

        jobID_p = re.compile('<C_2>(.*?)</C_2>', re.S)
        jobID_list  = re.findall(jobID_p, page)      # 按条取出项目
        self.jobIDs_str = ','.join(jobID_list)
        print self.jobIDs_str
        return 0

    def commitJob(self):
    	if self.getJobID()  != 0:
    		return -1
        data = '<?xml version=\"1.0\" encoding=\"UTF-8\"?><root><rowSet>'\
             + '<JOB_IDS>' + self.jobIDs_str + '</JOB_IDS>'\
             + '<START_TIME>' + self.beginDate + '</START_TIME><END_TIME>' + self.endDate + '</END_TIME>'\
             + '<AUDIT_RESULT>1</AUDIT_RESULT><AUDIT_CONTENT></AUDIT_CONTENT><AUDIT_SCORE>5</AUDIT_SCORE><TYPE>GD</TYPE>'\
             + '</rowSet></root>';
        url = 'http://'+self.SiteIPandPort+'/servlet/maintjobinstanceservlet?tag=19'
        try:
            req = urllib2.Request(url,headers=self.headers)
            #利用urllib2的build_opener方法创建一个opener
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
            response = opener.open(req,data,timeout=15)
            # print response.status
            # print response.reason
            # print response.getheaders()
            page = response.read()
            print page
        except Exception, e:
            print e
            return -1


if __name__ == '__main__':
	itsm = ITSM() 
	itsm.commitJob()
	