# coding: utf-8

import os
import jieba
from py2neo import Graph

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.g =Graph("bolt://localhost:7687", auth=("neo4j", "123456"))
        
        
        #　特征词路径
        self.disease_path = os.path.join(cur_dir, 'dict/disease.txt')
        self.drug_path = os.path.join(cur_dir, 'dict/drug.txt')
        self.food_path = os.path.join(cur_dir, 'dict/food.txt')
        self.symptom_path = os.path.join(cur_dir, 'dict/symptom.txt')
        self.deny_path = os.path.join(cur_dir, 'dict/deny.txt')
        # 将字典导入
        jieba.load_userdict(self.drug_path)
        jieba.load_userdict(self.disease_path)
        jieba.load_userdict(self.food_path)
        jieba.load_userdict(self.symptom_path)
        
        # 加载特征词
        self.disease_wds= [i.strip() for i in open(self.disease_path,encoding='UTF-8') if i.strip()]
        self.drug_wds= [i.strip() for i in open(self.drug_path,encoding='UTF-8') if i.strip()]
        self.food_wds= [i.strip() for i in open(self.food_path,encoding='UTF-8') if i.strip()]
        self.symptom_wds= [i.strip() for i in open(self.symptom_path,encoding='UTF-8') if i.strip()]
        self.region_words = set(self.disease_wds  + self.drug_wds + self.food_wds + self.symptom_wds)
        self.deny_words = [i.strip() for i in open(self.deny_path,encoding='UTF-8') if i.strip()]
        
        # 问句疑问词
        self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现']
        self.cause_qwds = ['原因','成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致', '会造成']
        self.acompany_qwds = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现']
        self.food_qwds = ['饮食', '饮用', '吃', '食', '伙食', '膳食', '喝', '菜' ,'忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物','补品']
        self.drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
        self.prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止','躲避','逃避','避开','免得','逃开','避开','避掉','躲开','躲掉','绕开',
                             '怎样才能不', '怎么才能不', '咋样才能不','咋才能不', '如何才能不',
                             '怎样才不', '怎么才不', '咋样才不','咋才不', '如何才不',
                             '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                             '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        self.cureway_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治']
        self.cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
                          '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要']
        self.lasttime_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年']
        self.cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医','治愈率','概率']
        print('model init finished ......')

        return
    
    def get_type(self, words):
        types=[]
        query="MATCH (n:Disease) where n.name ='{words}' return n.name".format(words=words)
        ress = self.g.run(query).data()
        if ress!=[]:
            types.append("disease")
        
        query="MATCH (n:Drug) where n.name ='{words}' return n.name".format(words=words)
        ress = self.g.run(query).data()
        if ress!=[]:
            types.append("drug")
        
        query="MATCH (n:Food) where n.name ='{words}' return n.name".format(words=words)
        ress = self.g.run(query).data()
        if ress!=[]:
            types.append("food")
        
        query="MATCH (n:Symptom) where n.name ='{words}' return n.name".format(words=words)
        ress = self.g.run(query).data()
        if ress!=[]:
            types.append("symptom")
        
        return types
        
        
    def get_medical_information(self, question):
            words = list(jieba.cut(question, cut_all=False))
            wd_dict = dict()
            for i in words:
                type=self.get_type(i)
                if type!=[]:
                    wd_dict[i]=type
            return wd_dict
    
            
    
    def classify(self, question):
        data = {}
        medical_dict = self.get_medical_information(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        print(medical_dict)
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 症状
        if self.check_words(self.symptom_qwds, question) and ('disease' in types):
            question_type = 'disease_symptom'
            question_types.append(question_type)
        #症状推疾病
        if self.check_words(self.symptom_qwds, question) and ('symptom' in types):
            question_type = 'symptom_disease'
            question_types.append(question_type)
        #治愈率
        if self.check_words(self.cureprob_qwds, question) and ('disease' in types):
            question_type = 'disease_cureprob'
            question_types.append(question_type)
        #治愈时间
        if self.check_words(self.lasttime_qwds, question) and ('disease' in types):
            question_type = 'disease_cured_time'
            question_types.append(question_type)
        # 原因
        if self.check_words(self.cause_qwds, question) and ('disease' in types):
            question_type = 'disease_cause'
            question_types.append(question_type)
        # 并发症
        if self.check_words(self.acompany_qwds, question) and ('disease' in types):
            question_type = 'disease_acompany'
            question_types.append(question_type)

        # 推荐食品
        if self.check_words(self.food_qwds, question) and 'disease' in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'disease_not_food'
            else:
                question_type = 'disease_do_food'
            question_types.append(question_type)


        # 推荐药品
        if self.check_words(self.drug_qwds, question) and 'disease' in types:
            question_type = 'disease_drug'
            question_types.append(question_type)

        # 药品治啥病
        if self.check_words(self.cure_qwds, question) and 'drug' in types:
            question_type = 'drug_disease'
            question_types.append(question_type)


        #　症状防御
        if self.check_words(self.prevent_qwds, question) and 'disease' in types:
            question_type = 'disease_prevent'
            question_types.append(question_type)


        # 疾病治疗方式
        if self.check_words(self.cureway_qwds, question) and 'disease' in types:
            question_type = 'disease_cureway'
            question_types.append(question_type)
            
        if question_types == [] and 'symptom' in types:
            question_types = ['symptom_disease']

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'disease' in types:
            question_types = ['disease_desc']


        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data
    
    
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False
    
if __name__ == '__main__':
    handler = QuestionClassifier()
    print(handler.classify("发烧是什么病"))
    #print(handler.get_type('发烧'))
    