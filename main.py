from flask import Flask,render_template,redirect,url_for,request,jsonify
from get_relation import *
from  chatbot_graph import *
app=Flask(__name__)
import json

@app.route('/test',methods=['GET'])
def test_get():
    # dic={"11":11}
    # answer={"22":22}
    # file=open("staticcizdata_mimini_aglin.json",'r',encoding="utf-8")
    # l=json.load(file)
    # dic = json.dumps(l,ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ': '))

    #获取Get数据
    question=request.args.get('question')
    print(question)
    # question=request.form['question']
    BIM = BertIntentModel()
    handler=ChatBotGraph()
    res=BIM.predict(question)
    qs_type=handler.sql.convert(res)
    qs_type1=handler.classifier.classify(question)
    if qs_type=='else' or qs_type!=qs_type1:#置信度过小ganm或不在训练模型中的类别都为else
        answer = handler.chat_main(question)
    else:
        answer = handler.chat_base_model(qs_type,question)
    answer=answer+"，注意健康哦！"
    print(answer)
    classify_res=handler.classifier.classify(question)
    if not classify_res:
        dic={}
    args = classify_res['args']
    entity_dict = handler.parser.build_entitydict(args)
    try:
        disease=entity_dict["disease"]
        print(disease)
        dic=get_relation(disease[0])
    except:
        dic={}
    print(dic)
    fi=open("vizdata.txt","w",encoding="utf-8")
    fi.write(json.dumps(dic,ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ': ')))
    return jsonify([dic,answer])


@app.route('/index',methods=['GET','POST'])
def main():
    if request.method == 'GET':
         return render_template('index.html')
    # else:
    #     question=request.form['question']
    #     BIM = BertIntentModel()
    #     handler=ChatBotGraph()
    #     res=BIM.predict(question)
    #     qs_type=handler.sql.convert(res)
    #     print(qs_type)
    #     if qs_type=='else':#置信度过小或不在训练模型中的类别都为else
    #         answer = handler.chat_main(question)
    #     else:
    #         answer = handler.chat_base_model(qs_type,question)
    #     answer="小原批: "+answer
    #     classify_res=handler.classifier.classify(question)
    #     if not classify_res:
    #         dic={}
    #     args = classify_res['args']
    #     entity_dict = handler.parser.build_entitydict(args)
    #     try:
    #         disease=entity_dict["disease"]
    #         dic=get_relation(disease)
    #     except:
    #         dic={}
    #     return render_template('index.html',dic=dic,answer=answer)
    
    
if __name__=='__main__':
    app.run(debug=True)
