# coding: utf-8
import jieba
from py2neo import Graph
import os

class qs_convedrt:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.g =Graph("bolt://localhost:7687", auth=("neo4j", "123456"))
        
        
    def convert(self,predict_res):
        print(predict_res)
        qs_type=predict_res['name']
        confidence=predict_res['confidence']
        question_type=''
        if qs_type == '定义':
            question_type='disease_desc'
        elif qs_type == '病因':
            question_type='disease_cause'
        elif qs_type == '预防':
            question_type='disease_prevent'
        elif qs_type == '临床表现(病症表现)':
            question_type='symptom_disease'
        elif qs_type == '相关病症':
            question_type='disease_acompany'
        elif qs_type == '治疗方法':
            question_type='disease_cureway'
        elif qs_type == '治愈率':
            question_type='disease_disease_cureprob' 
        elif qs_type == '禁忌':
            question_type='disease_not_food' 
        elif qs_type == '治疗时间':
            question_type='disease_cured_time' 
        if question_type=='' or confidence < 0.9:
            question_type='else'
        return question_type

    def get_disease(self,question):
        words = list(jieba.cut(question, cut_all=False))
        for i in words:
            query="MATCH (n:Disease) where n.name ='{0}' return n.name".format(i)
            ress = self.g.run(query).data()
            if ress!=[]:
                return i
            query="MATCH (n:Symptom) where n.name ='{0}' return n.name".format(i)
            ress = self.g.run(query).data()
            if ress!=[]:
                return i
        return ''
    
    def get_sql(self,qs_type,question):
        medical_type=self.get_disease(question)
        if medical_type =='':
            return []
        question_type=qs_type
        sql=[]
        if question_type == 'disease_desc':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.desc".format(medical_type)]
        elif question_type == 'disease_cause':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cause".format(medical_type)]
        elif question_type == 'disease_prevent':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(medical_type)]
        elif question_type == 'disease_symptom':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(medical_type)]
        elif question_type == 'disease_acompany':
            sql1 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where m.name = '{0}' return m.name, r.name, n.name".format(medical_type)]
            sql2 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where n.name = '{0}' return m.name, r.name, n.name".format(medical_type)]
            sql = sql1 + sql2
        elif question_type == 'disease_cureway':
            sql = ["MATCH (m:Disease)-[r:cure_way]->(n:Cure) where m.name = '{0}' return m.name, r.name, n.name".format(medical_type)]
        elif question_type == 'disease_cured_prob':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cured_prob".format(medical_type)]
        elif question_type == 'disease_cured_time':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_lasttime".format(medical_type)]
        elif question_type == 'disease_not_food':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(medical_type)]
        sql_ = {}
        sqls=[]
        sql_['question_type'] = question_type
        if sql:
            sql_['sql'] = sql
            sqls.append(sql_)
        return sqls
        
        
