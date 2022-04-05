'''
将使用Neo4j云服务，即Neo4j Aura导入，参考文档：https://neo4j.com/docs/aura/current/getting-started/importing-data/

如果有需要，可以先使用下面的命令清空测试数据（不建议删除和重建数据库，因为比较耗时）：
MATCH (n) DETACH DELETE n;

使用如下命令导入数据：

LOAD CSV WITH HEADERS FROM "" AS row
CREATE (c:客户 {客户id: row.客户});

LOAD CSV WITH HEADERS FROM "" AS row
CREATE (p:产品 {产品名称: row.产品});

LOAD CSV WITH HEADERS FROM "" AS line
WITH line
MATCH (c:客户 {客户id:line.客户})
MATCH (p:产品 {产品名称:line.产品})
MERGE (c)-[:拥有 {类型:line.类型, 值:toInteger(line.值)}]->(p)
RETURN count(*);

MATCH (c)-[cp]->(p) RETURN c,cp,p;

cheatsheet:
https://gist.github.com/DaniSancas/1d5265fc159a95ff457b940fc5046887
'''

#import libraries and define paramters
from neo4j import GraphDatabase
import spacy
import logging
logger = logging.getLogger("spacy")
logger.setLevel(logging.ERROR)

#define the parameters, host, query and keywords
uri = "neo4j+s://1144f8d0.databases.neo4j.io:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "VPrCeTO-8CzYElUogkj45D4Ec0x454oBgAqHIjHZG4k")) #enter your neo4j username and password instead of 'test'
session = driver.session()

图数据库查询用语句 = ("MATCH (c:`客户`)-[r:`拥有`]->(p:`产品`) " 
    "WHERE c.`客户id` = $customerid AND p.`产品名称` = $productname " 
    "RETURN DISTINCT properties(r)")

图数据库验证身份用语句 = ("MATCH (c:`客户`) " 
    "WHERE c.`客户id` = $customerid " 
    "RETURN DISTINCT c")

图数据库更新用语句 = ("MATCH (c:`客户`)-[r:`拥有`]->(p:`产品`) " 
    "WHERE c.`客户id` = $customerid AND p.`产品名称` = $productname "
    "and r.`类型` = $attribute "
    "SET r.`值` = toInteger($value) "
    "RETURN DISTINCT properties(r)")

意图字典 = {'查询':图数据库查询用语句, 'login':图数据库验证身份用语句, '更新':图数据库更新用语句}

#list of key intent, product and attribute
产品列表 = ['存款','贷款']
属性列表 = ['利率','账户余额']
意图列表 = ['查询','更新']

print('加载nlp模型')
nlp = spacy.load('zh_core_web_sm')
tokens_products = nlp(' '.join(product for product in 产品列表))
tokens_intent = nlp(' '.join(intent for intent in 意图列表))
tokens_attribute = nlp(' '.join(attribute for attribute in 属性列表))

#define relevant functions to execute differnet queries
def run_query(tx, query, cid, product, attribute,attribute_val):
    result_list=[]
    for record in tx.run(query, customerid=cid,productname=product, attribute=attribute,value=attribute_val):
        result_list.append(record[0])
    return result_list


def intent_entity_attribute_extraction(nlp, sentence, tokens_intent, tokens_product, tokens_attribute):
    #please implement your sentence classification here to extract the intent
    tokens = nlp(sentence)
    #use the NER to extract the entity regarding product

    intent_score= 0
    product_score = 0
    attribute_score = 0
    final_intent = ''
    final_product = ''
    final_attribute = ''
    final_attribute_value = ''

    threshold = 0.8

    print('AI开始思考——提取意图：')

    # 将tokens列表通过\合并成一个字符串
    tokens_str = ' '.join(token.text for token in tokens)
    print('分词结果为:', tokens_str)

    for token in tokens:
        for intent in tokens_intent:            
            curr_intent_score = token.similarity(intent)
            print(token.text,'与',intent.text,'的相似度为:', curr_intent_score)
            之前的意图分数最高值 = intent_score
            if curr_intent_score > intent_score and curr_intent_score > threshold:
                intent_score = curr_intent_score
                final_intent = intent.text
                print('因为分词短语中的“' + token.text + '”与意图“' + intent.text + '”的相似度为' + str(curr_intent_score) + '，大于之前的意图分数最高值' + str(之前的意图分数最高值) + '，并且超过阈值' + str(threshold) + '，所以AI认为当前用户意图是“' + intent.text + '”。')

        for product in tokens_product:
            curr_product_score = token.similarity(product)
            之前的产品分数最高值 = product_score
            if curr_product_score > product_score and curr_product_score > threshold:
                product_score = curr_product_score
                final_product = product.text
                print('因为分词短语中的“' + token.text + '”与产品“' + product.text + '”的相似度为' + str(curr_product_score) + '，大于之前的产品分数最高值' + str(之前的产品分数最高值) + '，并且超过阈值' + str(threshold) + '，所以AI认为当前用户谈到的产品是“' + product.text + '”。')
                    
        for attribute in tokens_attribute:
            curr_attribute_score = token.similarity(attribute)
            之前的属性分数最高值 = attribute_score
            if curr_attribute_score > attribute_score and curr_attribute_score > threshold:
                attribute_score = curr_attribute_score
                final_attribute = attribute.text
                print('因为分词短语中的“' + token.text + '”与属性“' + attribute.text + '”的相似度为' + str(curr_attribute_score) + '，大于之前的属性分数最高值' + str(之前的属性分数最高值) + '，并且超过阈值' + str(threshold) + '，所以AI认为当前用户谈到的产品属性是“' + attribute.text + '”。')

        if token.pos_ == 'NUM' and token.text.isdigit():
            final_attribute_value = token.text

    print('请稍等...')
    print(final_intent, final_product, final_attribute, final_attribute_value)
    return (final_intent, final_product, final_attribute, final_attribute_value)

name = ''
product = ''
attribute = ''
attribute_val = ''
reset = False

while True:
    
    #Authentication
    if name == '' or reset:
        name = input('你好, 请问你叫什么名字? ')
        print('Hi '+name)
        #check for login
        query_str = 意图字典['login']
        result = session.read_transaction(run_query, query_str, name, product,attribute,attribute_val)
        if len(result)==0:
            print('没有'+name + '这个客户')            
            name =''
            continue
    
    #Sentences Intent and Entities Extraction
    input_sentence = input('你需要做什么? ')
    if input_sentence == "重置":
        reset = True 
    entities = intent_entity_attribute_extraction(nlp, input_sentence,tokens_intent, tokens_products, tokens_attribute)
    #actually can build another intent classifier here based on the scores and words matched as features, as well as previous entities
    intent = entities[0]
    product = entities[1]
    attribute = entities[2]
    attribute_val = entities[3]

    #cross-check for missing information
    while intent == '':
        input_sentence = input('你需要做什么?')
        entities = intent_entity_attribute_extraction(nlp, input_sentence,tokens_intent, tokens_products, tokens_attribute)
        intent = entities[0]

    while product == '':
        input_sentence = input('你想查询什么产品？')
        entities = intent_entity_attribute_extraction(nlp, input_sentence,tokens_intent, tokens_products, tokens_attribute)
        product = entities[1]

    while attribute == '':
        input_sentence = input('你想' + intent + product +'的什么？')
        entities = intent_entity_attribute_extraction(nlp, input_sentence,tokens_intent, tokens_products, tokens_attribute)
        attribute = entities[2]

    #execute the query to extract the answer
    query_str = 意图字典[intent]
    results = session.read_transaction(run_query, query_str, name,product,attribute,attribute_val)
    if len(results) >0:
        for result in results:
            if result['类型'] == attribute:
                print(product  + '的' + attribute + '为'+str(result['值']))
    else:
        print('没有相关记录')
