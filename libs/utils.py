import time
import json


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def getDistListFromObjectList(objectList):
    dictList = []
    for item in objectList:
        dictList.append(item.__dict__)
    return dictList


# def json_response(data):
#     """
#     data为字典或列表
#     本函数返回 json 格式的 body 数据
#     前端的 ajax 函数就可以用 JSON.parse 解析出格式化的数据
#     """
#     # 注意, content-type 现在是 application/json 而不是 text/html
#     # 这个不是很要紧, 因为客户端可以忽略这个
#     header = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
#     # json.dumps 用于把 list 或者 dict 转化为 json 格式的字符串
#     # ensure_ascii=False 可以正确处理中文
#     # indent=2 表示格式化缩进, 方便好看用的
#     body = json.dumps(data, ensure_ascii=False, indent=2)
#     r = header + '\r\n' + body
#     return r.encode(encoding='utf-8')
