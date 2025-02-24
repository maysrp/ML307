# ML307
ML307 4G模块在 micropython下的使用  

AT指令版ML307R 中国移动  



## 例子
```
from ml307 import ML307

mm=ML307(6,7)
#UART初始化 rx为6 tx为7
c=mm.get("http://httpbin.org/get?id=33")
print(c)
#发起GET请求

mm.header=["User-Agent: MyCustomAgent/1.0","mam: i am hera"]
#添加请求头，不添加则使用默认空请求头，可用用于验证
info={"aa":23,"zz":11}
#设置POST的表单数据
cc=mm.post("http://httpbin.org/post",info)
print(cc)
```
## 注意
1. 在micropython下rxbuf和txbuf一般最大2048，所以要上传大文件可用另外想办法。
2. 若第一次请求失败返回false，请再发起一次请求
3. 若有端口号如 http://abc.com:800/aaa 则直接调用即可 mm.get("http://abc.com:800/aaa")
4. 只存在get与post两个方法
