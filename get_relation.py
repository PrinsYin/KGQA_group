import os
from py2neo import Graph
from functools import reduce
# links=[]
# nodes=[]

def get_node_and_link(name,relation,source,value,_class,group,size,type,links,nodes):
    g =Graph("bolt://localhost:7687", auth=("neo4j", "123456"))
    link={}
    node={}
    if type=="name":
        query= "MATCH (m:Disease)-[r:{relation}]->(n:{_class}) where m.name = '{name}' return n.name".format(relation=relation,_class=_class,name=name)
    else:
        query= "MATCH (n:Disease) where n.name ='{name}' return n.{type}".format(name=name,type=type)
    link["relation"]=relation
    link["source"]=source
    link["target"]=[]
    res = g.run(query).data()
    res= reduce(lambda x, y: y in x and x or x + [y], res, [])
    word="n.{0}".format(type)
    if res!=[]:
        for i in res:
            link["target"].append(i[word])
    else:
        return {},{}
    link["value"]=value
    node["class"]=_class
    node["group"]=group
    node["id"]=[]
    for i in res:
        node["id"].append(i[word])
    node["size"]=size
    # node["id"]='、'.join(node["id"])
    # link["target"]='、'.join(link["target"])
    # links.append(link)
    # nodes.append(node)
    print(link,node)
    l1={}
    l1["relation"]=link["relation"]
    l1["source"]=source
    l1["target"]=link["relation"]
    l1["value"]=6
    links.append(l1)
    for i in range(len(link["target"])):
        l2={}
        l2["relation"]=""
        l2["source"]=link["relation"]
        l2["target"]=link["target"][i]
        l2["value"]=12
        links.append(l2)
    l3={}
    l3["class"]=_class
    l3["group"]=1
    l3["id"]=link["relation"]
    l3["size"]=16
    nodes.append(l3)
    for i in range(len(link["target"])):
        l4={}
        l4["class"]=_class
        l4["group"]=2
        l4["id"]=link["target"][i]
        l4["size"]=12
        nodes.append(l4)
        
    print("aaa",links,nodes,"links111")
    return link,node

def get_relation(name):
    links=[]
    nodes=[]
    dic={}
    link,node=get_node_and_link(name,"do_eat",name,3,"Food",2,8,"name",links,nodes)
    
    # if not (link =={} or node=={}):
    #     links.append(link)
    #     nodes.append(node)
        
    link,node=get_node_and_link(name,"cure_way",name,3,"Cure",2,8,"name",links,nodes)
    # if not (link =={} or node=={}):
    #     links.append(link)
    #     nodes.append(node)
        
    link,node=get_node_and_link(name,"has_symptom",name,3,"Symptom",2,8,"name",links,nodes)
    # if not (link =={} or node=={}):
    #     links.append(link)
    #     nodes.append(node)
    
    link,node=get_node_and_link(name,"common_drug",name,3,"Drug",2,8,"name",links,nodes)
    # if not (link =={} or node=={}):
    #     links.append(link)
    #     nodes.append(node)
        
    link,node=get_node_and_link(name,"预防",name,3,"Prevent",2,8,"prevent",links,nodes)
    # if not (link =={} or node=={}):
    #     links.append(link)
    #     nodes.append(node)
        
    link,node=get_node_and_link(name,"原因",name,3,"Cause",2,8,"cause",links,nodes)
    # if not (link =={} or node=={}):
    #     links.append(link)
    #     nodes.append(node)
        
    link,node=get_node_and_link(name,"治愈率",name,3,"Cured_prob",2,8,"cured_prob",links,nodes)
    # if not (link =={} or node=={}):
    #     links.append(link)
    #     nodes.append(node)
        
    tmp={}    
    tmp["class"]="Disease"   
    tmp["group"]=0
    tmp["id"]=name
    tmp["size"]=32
        
    dic["links"]=links
    dic["nodes"]=nodes
    print(links,nodes,"links111")
    if not len(dic)==0:
        dic["nodes"].append(tmp)
    print(links,nodes,"links111")
    return dic
    
    
if __name__ == '__main__':
    print(get_relation("头痛"))