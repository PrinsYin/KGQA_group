# -*- coding:utf-8 -*-
import tensorflow as tf 
from keras.backend.tensorflow_backend import set_session
from bert4keras.tokenizers import Tokenizer

from bert_model import build_bert_model

global graph,model,sess 


config = tf.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.Session(config=config)
graph = tf.get_default_graph()
set_session(sess)

class BertIntentModel(object):
    def __init__(self):
        super(BertIntentModel, self).__init__()
        self.dict_path = 'pre_model/vocab.txt'
        self.config_path='pre_model/bert_config_rbt3.json'
        self.checkpoint_path='pre_model/bert_model.ckpt'

        self.label_list = [line.strip() for line in open('label','r',encoding='utf8')]
        self.id2label = {idx:label for idx,label in enumerate(self.label_list)}

        self.tokenizer = Tokenizer(self.dict_path)
        self.model = build_bert_model(self.config_path,self.checkpoint_path,13)
        self.model.load_weights('model/best_model.weights')

    def predict(self,text):
        token_ids, segment_ids = self.tokenizer.encode(text, maxlen=60)
        proba = self.model.predict([[token_ids], [segment_ids]])
        rst = {l:p for l,p in zip(self.label_list,proba[0])}
        rst = sorted(rst.items(), key = lambda kv:kv[1],reverse=True)
        name,confidence = rst[0]
        return {"name":name,"confidence":float(confidence)}
    
        
BIM = BertIntentModel()


if __name__ == '__main__':

    r = BIM.predict("感冒吃什么")
    print(r)