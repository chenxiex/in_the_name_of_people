import networkx as nx
import urllib.request
import re
from bs4 import BeautifulSoup
import jieba

# 爬取百度百科中的电视剧列表
def urlget(url):
    response = urllib.request.urlopen(url).read().decode('utf-8')
    with open('response.txt','w',encoding='utf-8') as f:
        f.write(response)

response=open('response.txt','r',encoding='utf-8').read()
resp_soup=BeautifulSoup(response,'html.parser')

# 获取分集剧情
content = resp_soup.find_all('ul',{'id':'dramaSerialList'})
content = str(content)
content_plain = re.sub(r'<[^>]+>', '', content)
with open('drama_list.txt','w',encoding='utf-8') as f:
    f.write(content_plain)

# 获取人物名字
name_content=resp_soup.find_all('dl',attrs={'class':'info'})
with open('name.txt','w',encoding='utf-8') as f:
    for i in name_content:
        name_d=i.get_text().strip().split(u'\n')[0]
        name=name_d.split(u'\xa0')[2]
        f.write(name.encode('utf-8').decode()+'\n')

# 文本预处理
jieba.load_userdict('name.txt')

# 读取分集剧情
summary_text=open('drama_list.txt','r',encoding='utf-8').read()

# 分词
with open('content.txt','w',encoding='utf-8') as f:
    sentences=summary_text.split('。')
    for sentence in sentences:
        s=re.sub(r'，|！|？|：|“|”|；|、|（|）|《|》|……|「|」|『|』|〖|〗|【|】|〈|〉',' ',sentence)
        words=list(jieba.cut(s))
        out_str=' '.join(words)
        out_str=re.sub(r'   ',' ',out_str)
        f.write(out_str+'\n')