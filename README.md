# Python爬虫

> 网络爬虫（又被称为网页蜘蛛，网络机器人，在FOAF社区中间，更经常的称为网页追逐者），是一种按照一定的规则，自动的抓取万维网信息的程序或者脚本。

[TOC]

## 爬虫概述
1. 什么是爬虫
爬虫，即网络爬虫，大家可以理解为在网络上爬行的一直蜘蛛，互联网就比作一张大网，而爬虫便是在这张网上爬来爬去的蜘蛛咯，如果它遇到资源，那么它就会抓取下来。
2. 浏览网页的过程
用户输入网址之后，经过DNS服务器，找到服务器主机，向服务器发出请求，服务器经过解析之后，发送给用户的浏览器***HTML、JS、CSS***等文件，浏览器解析出来，用户便可以看到形形色色的网页内容了。
因此，用户看到的网页实质是由 HTML 代码构成的，爬虫爬来的便是这些内容，通过分析和过滤这些***HTML***代码，实现对图片、文字等资源的获取。
3. URL的含义
URL，即统一资源定位符，也就是我们说的网址，统一资源定位符是对可以从互联网上得到的资源的位置和访问方法的一种简洁的表示，是互联网上标准资源的地址。互联网上的每个文件都有一个唯一的URL，它包含的信息指出文件的位置以及浏览器应该怎么处理它。URL的格式由三部分组成：
	1. 第一部分是协议(或称为服务方式)。
	2. 第二部分是存有该资源的主机IP地址(有时也包括端口号)。
	3. 第三部分是主机资源的具体地址，如目录和文件名等。

## 爬虫入门
1. python基础学习
	* [python基础教程](http://www.runoob.com/python/python-tutorial.html)
	* [廖雪峰Python教程](http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000)
2. 爬虫基础：urllib和urllib2
3. 爬虫工具：xpath、正则表达式
4. 爬虫IDE：Pycharm、sublime text2
5. 爬虫框架：scrapy、pyspider

### urllib和urllib2
1. 爬取[百度](http://www.baidu.com)
	```
	import urllib2

	response = urllib2.urlopen("http://www.baidu.com")
	print response.read()
	```
2. 方法说明：
	* `urlopen(url, data, timeout)`：第一个参数url即为URL，第二个参数data是访问URL时要传送的数据，第三个timeout是设置超时时间。第二三个参数是可以不传送的，data默认为空None，timeout默认为 socket._GLOBAL_DEFAULT_TIMEOUT
3. 构造Requset
	```
	import urllib2

	request = urllib2.Request("http://www.baidu.com")
	response = urllib2.urlopen(request)
	print response.read()
	```
4. GET和Post
	```
	import urllib
	import urllib2

	values = {"username":"18646083985@163.com","password":"199457"}
	data = urllib.urlencode(values) 
	url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
	request = urllib2.Request(url,data)
	response = urllib2.urlopen(request)
	print response.read()
	```
5. 设置headers
	* 设置请求身份***User-Agent***
	* 设置***referer***，防止网站屏蔽反倒链
	* 样例：`headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Referer':'http://www.zhihu.com/articles' }`
	* 关于headers的一些属性，下面内容需要额外注意：
		* User-Agent : 有些服务器或 Proxy 会通过该值来判断是否是浏览器发出的请求
		* Content-Type : 在使用 REST 接口时，服务器会检查该值，用来确定 HTTP Body 中的内容该怎样解析。
		* application/xml ： 在 XML RPC，如 RESTful/SOAP 调用时使用
		* application/json ： 在 JSON RPC 调用时使用
		* application/x-www-form-urlencoded ： 浏览器提交 Web 表单时使用
		* 在使用服务器提供的 RESTful 或 SOAP 服务时， Content-Type 设置错误会导致服务器拒绝服务
6. 代理设置
	* urllib2 默认会使用环境变量http_proxy来设置HTTP Proxy
	* 代理设置样例：
	```
	import urllib2

	enable_proxy = True
	proxy_handler = urllib2.ProxyHandler({"http" : 'http://some-proxy.com:8080'})
	null_proxy_handler = urllib2.ProxyHandler({})
	if enable_proxy:
	    opener = urllib2.build_opener(proxy_handler)
	else:
	    opener = urllib2.build_opener(null_proxy_handler)
	urllib2.install_opener(opener)
	```
7. timeout设置
	* 可以用来解决有些网站相应过慢，卡死的情况
	* 注意参数的位置，若无data参数，则明确指出`timeout=s`
8. 异常捕获
	* try...except捕获异常
	* URLError，产生原因：
		* 网络无连接，即本机无法上网
		* 连接不到特定的服务器
		* 服务器不存在
	* HTTPError
		* HTTPError是URLError的子类，在你利用urlopen方法发出一个请求时，服务器上都会对应一个应答对象response，其中它包含一个数字***“状态码”***,HTTPError捕获相应的错误***“状态码”***
	* 样例：
	```
	import urllib2

	req = urllib2.Request('http://blog.csdn.net/cqcre')
	try:
	    urllib2.urlopen(req)
	except urllib2.HTTPError, e:
	    print e.code
	except urllib2.URLError, e:
	    print e.reason
	else:
	    print "OK"
    ```
9. Cookie使用
	* cookielib：主要作用是提供可存储cookie的对象，以便于与urllib2模块配合使用来访问Internet资源。
	* 获取cookie内容：
	```
	import urllib2
	import cookielib

	#声明一个CookieJar对象实例来保存cookie
	cookie = cookielib.CookieJar()
	#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
	handler=urllib2.HTTPCookieProcessor(cookie)
	#通过handler来构建opener
	opener = urllib2.build_opener(handler)
	#此处的open方法同urllib2的urlopen方法，也可以传入request
	response = opener.open('http://www.baidu.com')
	for item in cookie:
	    print 'Name = '+item.name
	    print 'Value = '+item.value
	```
	* 保存cookie到文件：
	```
	import cookielib
	import urllib2

	#设置保存cookie的文件，同级目录下的cookie.txt
	filename = 'cookie.txt'
	#声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
	cookie = cookielib.MozillaCookieJar(filename)
	#利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
	handler = urllib2.HTTPCookieProcessor(cookie)
	#通过handler来构建opener
	opener = urllib2.build_opener(handler)
	#创建一个请求，原理同urllib2的urlopen
	response = opener.open("http://www.baidu.com")
	#保存cookie到文件
	cookie.save(ignore_discard=True, ignore_expires=True)
	```
---

### 网页解析工具
1. 正则表达式
	* 正则表达式是对字符串操作的一种逻辑公式，就是用事先定义好的一些特定字符、及这些特定字符的组合，组成一个“规则字符串”，这个“规则字符串”用来表达对字符串的一种过滤逻辑。
	* 正则表达式的大致匹配过程是：
		* 依次拿出表达式和文本中的字符比较，
		* 如果每一个字符都能匹配，则匹配成功；一旦有匹配不成功的字符则匹配失败。
		* 如果表达式中有量词或边界，这个过程会稍微有一些不同
	* python正则表达式支持：
	```
	#返回pattern对象
	re.compile(string[,flag])
	#以下为匹配所用函数
	re.match(pattern, string[, flags])
	re.search(pattern, string[, flags])
	re.split(pattern, string[, maxsplit])
	re.findall(pattern, string[, flags])
	re.finditer(pattern, string[, flags])
	re.sub(pattern, repl, string[, count])
	re.subn(pattern, repl, string[, count])
	```
2. xpath
	* XPath 是一门在 XML 文档中查找信息的语言。XPath 可用来在 XML 文档中对元素和属性进行遍历。XPath 是 W3C XSLT 标准的主要元素，并且 XQuery 和 XPointer 都构建于 XPath 表达之上。
	* python xpath支持[lxml库](http://lxml.de/index.html)
	* 基本用法：
	```
	from lxml import etree

	text = '''
	<div>
	    <ul>
	         <li class="item-0"><a href="link1.html">first item</a></li>
	         <li class="item-1"><a href="link2.html">second item</a></li>
	         <li class="item-inactive"><a href="link3.html">third item</a></li>
	         <li class="item-1"><a href="link4.html">fourth item</a></li>
	         <li class="item-0"><a href="link5.html">fifth item</a>
	     </ul>
	 </div>
	'''
	# 自动补全html标签
	html = etree.HTML(text)
	result = etree.tostring(html)
	print(result)
	```
3. Plantomjs
PhantomJS是一个无界面的,可脚本编程的WebKit浏览器引擎。它原生支持多种web 标准：DOM 操作，CSS选择器，JSON，Canvas 以及SVG。
4. Selenium
	* Selenium：自动化测试工具。它支持各种浏览器，包括 Chrome，Safari，Firefox 等主流界面式浏览器，如果你在这些浏览器里面安装一个 Selenium 的插件，那么便可以方便地实现Web界面的测试。
	* 快速体验
	```
	from selenium import webdriver

	browser = webdriver.Chrome()
	browser.get('http://www.baidu.com/')
	browser.close()
	browser.quit()
	```
	备注：[Chrome驱动下载](https://sites.google.com/a/chromium.org/chromedriver/downloads)
	* 动态爬虫三剑客：***Python + Selenium + PhantomJS***
		* PhantomJS 用来渲染解析JS
		* Selenium 用来驱动以及与 Python 的对接
		* Python 进行后期的处理
	* 官方doc[Selenium](http://selenium-python.readthedocs.io/)




## 爬虫实战

### DoubanSpider


### StockSpider
1. 爬取<http://batstrading.com/>上的报价与交易信息
2. 目前网站只会对访问过快，进行反爬虫，降低爬虫间歇即可，目前间歇设置为2s，可以稳定运行。
3. 网站返回数据提供json版本，直接请求json数据即可。
