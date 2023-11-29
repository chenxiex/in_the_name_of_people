import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import networkx as nx
import csv
font_sarasa=fm.FontProperties(fname='sarasa-ui-sc-regular.ttf')
#读取分好词的剧情和姓名
with open('content.txt','r',encoding='utf-8') as f:
    contents=f.read()
with open('name.txt','r',encoding='utf-8') as f:
    names=[line.strip('\n') for line in f.readlines()]

#计算剧情中名字的出现次数
def name_count():
    count=[]
    for name in names:
        count.append([name,contents.count(name)])
    count.sort(key=lambda x:x[1])
    return count

#画图
def name_draw():
    count=name_count()
    _,ax=plt.subplots()
    numbers=[x[1] for x in count[-10:]]
    names=[x[0] for x in count[-10:]]
    ax.barh(range(len(numbers)),numbers,color='blue',alpha=0.5)
    ax.set_yticks(range(len(numbers)))
    ax.set_yticklabels(names,fontsize=20,fontproperties=font_sarasa)
    ax.set_title('人物出场次数',fontsize=20,fontproperties=font_sarasa)
    plt.show()

# 社交网络分析
def social_network():
    content=contents.split('\n')
    count=name_count()
    graph=nx.Graph()
    for item in count:
        graph.add_node(item[0],weight=item[1])
    name_len=len(names)
    for colindex in range(name_len):
        for rowindex in range(name_len):
            weight=0
            for sentence in content:
                if names[colindex] in sentence and names[rowindex] in sentence:
                    weight+=1
            if weight!=0 and names[colindex]!=names[rowindex]:
                graph.add_edge(names[colindex],names[rowindex],weight=weight)
    nodes=[]
    for node in count:
        nodes.append([node[0],node[0],node[1]])
    with open('node.csv','w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['Id','Label','Weight'])
        writer.writerows(nodes)
    edges=[]
    for edge in graph.edges(data=True):
        edges.append([edge[0],edge[1],edge[2]['weight'],'undirected'])
    with open('edge.csv','w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['Source','Target','Weight','Type'])
        writer.writerows(edges)

if __name__=='__main__':
    name_draw()
    social_network()