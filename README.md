# tuwan_spider
tuwan网爬虫  
通过api漏洞对该网站的付费图片连接进行串行爬取  
api_url = https://api.tuwan.com/apps/Welfare/detail?type=image&dpr=3&id=1405&callback=jQuery1123016504855732614_1549779497538&_=1549779497543  
  
经测试发现该api有用的参数只有id....  
简化为https://api.tuwan.com/apps/Welfare/detail?id=1405  
GET方法请求这个链接会返回所有缩略图的地址  
  
例如这个缩略图链接http://img4.tuwandata.com/v3/thumb/jpg/OTE2YSwxNTgsMTU4LDksMywxLC0xLE5PTkUsLCw5MA==/u/GLDM9lMIBglnFv7YKftLBuURdOZOq8F9aPuqHgeODGD3E0OBJHaqkDtBsl7jkI23En0ctPY5sIUhzMP7z6wBniMfIhHZyHc32vaywkFlyGWn.jpg"  
中间的OTE2YSwxNTgsMTU4LDksMywxLC0xLE5PTkUsLCw5MA==这个路径后面的==暴露了他经过过base64 encode
decode该字符串后有得到这么几个参数['1e45', '158', '158', '9', '3', '1', '-1', 'NONE', '', '', '90']
第1,2个参数是图片的大小,直接换成0,0再b64encode组装回去就能请求到原图.......
['1e45', '0', '0', '9', '3', '1', '-1', 'NONE', '', '', '90']

这个api好像没有任何反爬机制,UA不改不拦截,多线程协程并发请求不拦截,无需设置随机访问间隔  
