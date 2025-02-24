from machine import UART
import time

class ML307(object):
    def __init__(self,rx,tx,u_num=1):
        self.uart=UART(u_num,115200,rx=rx,tx=tx,rxbuf=2048,txbuf=2048)
        self.header=[]
        time.sleep(3)
    def command(self,cmd,t=1):
        self.uart.write(cmd+'\r\n')
        time.sleep(t*0.1)
        return self.uart.read()
    def get_response(self,info):
        nx=info.split(b'MHTTPURC: "content"')
        rep_1=nx[1].split(b",")
        rep=b"".join(rep_1[5:])
        return rep
    def get_url(self,url_1,url_2,t=15):
        self.command('AT+MHTTPCREATE="'+url_1+'"')
        self.header_def()
        info=self.command('AT+MHTTPREQUEST=0,1,0,"'+url_2+'"',t)
        self.command('AT+MHTTPHEADER=0')
        return self.get_response(info)
    def get_url_ssl(self,url_1,url_2,t=15):
        self.command('AT+MHTTPCREATE="'+url_1+'"')
        self.command('AT+MHTTPCFG="ssl",0,1,1')
        self.header_def()
        info=self.command('AT+MHTTPREQUEST=0,1,0,"'+url_2+'"',t)
        self.command('AT+MHTTPHEADER=0')
        return self.get_response(info)
    def make_url(self,url):
        url_1="/".join(url.split("/")[0:3])
        url_2="/"+"/".join(url.split("/")[3:])
        return [url_1,url_2]
    def get(self,url):
        ua=self.make_url(url)
        try:
            if "https" in ua[0]:
                ba=self.get_url_ssl(ua[0],ua[1])
            else:
                ba=self.get_url(ua[0],ua[1])
            return ba
        except Exception as e:
            return False
    def post_form(self,info):
        form=""
        for key in info:
            form=form+key+"="+str(info[key])+"&"
        return form
    def post_url(self,url_1,url_2,form_str,t=15):
        self.command('AT+MHTTPCREATE="'+url_1+'"')
        self.header_def()
        self.command('AT+MHTTPHEADER=0,0,0,"Content-Type: application/x-www-form-urlencoded"')
        self.command('AT+MHTTPCONTENT=0,0,0,"'+form_str+'"')
        info=self.command('AT+MHTTPREQUEST=0,2,0,"'+url_2+'"',t)
        self.command('AT+MHTTPHEADER=0')
        return self.get_response(info)
    def post_url_ssl(self,url_1,url_2,form_str,t=15):
        self.command('AT+MHTTPCREATE="'+url_1+'"')
        self.command('AT+MHTTPCFG="ssl",0,1,1')
        self.header_def()
        self.command('AT+MHTTPHEADER=0,0,0,"Content-Type: application/x-www-form-urlencoded"')
        self.command('AT+MHTTPCONTENT=0,0,0,"'+form_str+'"')
        info=self.command('AT+MHTTPREQUEST=0,2,0,"'+url_2+'"',t)
        self.command('AT+MHTTPHEADER=0')
        return self.get_response(info)
    def post(self,url,dic_info):
        form_str=self.post_form(dic_info)
        ua=self.make_url(url)
        try:
            if "https" in ua[0]:
                ba=self.post_url_ssl(ua[0],ua[1],form_str)
            else:
                ba=self.post_url(ua[0],ua[1],form_str)
            return ba
        except Exception as e:
            return False
    def header_def(self):
        lh=len(self.header)
        if lh>1:
            for i in range(lh):
                if i <lh-1:
                    self.command('AT+MHTTPHEADER=0,1,0,"'+self.header[i]+'"')
                else:
                    self.command('AT+MHTTPHEADER=0,0,0,"'+self.header[i]+'"')
        elif lh==1:
            self.command('AT+MHTTPHEADER=0,0,0,"'+self.header[0]+'"')
        else:
            pass
