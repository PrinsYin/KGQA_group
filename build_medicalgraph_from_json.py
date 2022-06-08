# coding: utf-8


import os
import json
from py2neo import Graph,Node

class MedicalGraphFromJson:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'newdata')
        self.g =Graph("bolt://localhost:7687", auth=("neo4j", "123456"))

        self.rel_file='relations.json'
        self.node_file='entities.json'


    def build_graph(self):
        res=self.build_nodes()
        if res==-1:
            print('no nodes file, can not create relations')
            return
        self.build_rels()

    def build_nodes(self):
        node_file=os.path.join(self.data_path,self.node_file)
        print( node_file)
        if not os.path.exists(node_file):
            return -1
        nodes=json.load(open(node_file))
        for node in nodes:
            self.create_node(node)
        return 0

    def create_node(self,node):
        label=node['label']
        if label != 'Disease':
            n=Node(label,name=str(node['name']))
        else:
            name=node['name']
            n=Node(label,name=str(node['name']['name']),desc=str(name['desc']),
                        prevent=str(name['prevent']) ,cause=str(name['cause']),
                        easy_get=str(name['easy_get']),cure_lasttime=str(name['cure_lasttime']),
                        cured_prob=str(name['cured_prob']))
        self.g.create(n)

    def build_rels(self):
        rel_file=os.path.join(self.data_path,self.rel_file)
        if not os.path.exists(rel_file):
            print(self.rel_file,'not exist, skip')
            return
        relations=json.load(open(rel_file))
        for rel in relations:
            self.create_rel(rel)


    def create_rel(self,rels_set):
        cnt=0
        start_entity_type=rels_set['start_entity_type']
        end_entity_type=rels_set['end_entity_type']
        rel_type=rels_set['rel_type']
        rel_name=rels_set['rel_name']
        rels=rels_set['rels']
        for rel in rels:
            p=rel['start_entity_name']
            q=rel['end_entity_name']
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_entity_type, end_entity_type, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                cnt+=1
            except Exception as e:
                print(e)
        return

if __name__ == '__main__':
    handler = MedicalGraphFromJson()
    #handler.g.delete_all()
    handler.build_graph()

