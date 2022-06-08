from classify import *
from question_parser import *
from answer_search import *
from sql_base_model import *
from app import *
import jieba

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()
        self.sql=qs_convedrt()

    def chat_main(self, sent):
        answer = '您好！欢迎进行疾病咨询！'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        print(res_sql)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

    def chat_base_model(self,qs_type,question):
        answer = '您好！欢迎进行疾病咨询！'
        sqls=self.sql.get_sql(qs_type,question)
        final_answers = self.searcher.search_main(sqls)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)
        
        


if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        BIM = BertIntentModel()
        res=BIM.predict(question)
        qs_type=handler.sql.convert(res)
        qs_type1=handler.classifier.classify(question)
        print(qs_type)
        print(qs_type1)
        if qs_type=='else' or qs_type!=qs_type1 :#置信度过小或不在训练模型中的类别都为else
            answer = handler.chat_main(question)
        else:
            answer = handler.chat_base_model(qs_type,question)
        print('小原批:', answer)

