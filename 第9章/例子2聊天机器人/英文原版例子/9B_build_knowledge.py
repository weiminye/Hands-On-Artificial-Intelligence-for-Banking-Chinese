'''
将使用Neo4j云服务，即Neo4j Aura导入，参考文档：https://neo4j.com/docs/aura/current/getting-started/importing-data/

如果有需要，可以先使用下面的命令清空测试数据（不建议删除和重建数据库，因为比较耗时）：
MATCH (n) DETACH DELETE n;

使用如下命令导入数据：

LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/weiminye/Hands-On-Artificial-Intelligence-for-Banking-Chinese/main/%E7%AC%AC9%E7%AB%A0/%E4%BE%8B%E5%AD%902%E8%81%8A%E5%A4%A9%E6%9C%BA%E5%99%A8%E4%BA%BA/%E8%8B%B1%E6%96%87%E5%8E%9F%E7%89%88%E4%BE%8B%E5%AD%90/customer.csv" AS row
CREATE (c:Customer {customer_id: row.customer});

LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/weiminye/Hands-On-Artificial-Intelligence-for-Banking-Chinese/main/%E7%AC%AC9%E7%AB%A0/%E4%BE%8B%E5%AD%902%E8%81%8A%E5%A4%A9%E6%9C%BA%E5%99%A8%E4%BA%BA/%E8%8B%B1%E6%96%87%E5%8E%9F%E7%89%88%E4%BE%8B%E5%AD%90/product.csv" AS row
CREATE (p:Product {product_name: row.product});

LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/weiminye/Hands-On-Artificial-Intelligence-for-Banking-Chinese/main/%E7%AC%AC9%E7%AB%A0/%E4%BE%8B%E5%AD%902%E8%81%8A%E5%A4%A9%E6%9C%BA%E5%99%A8%E4%BA%BA/%E8%8B%B1%E6%96%87%E5%8E%9F%E7%89%88%E4%BE%8B%E5%AD%90/edge.csv" AS line
WITH line
MATCH (c:Customer {customer_id:line.customer})
MATCH (p:Product {product_name:line.product})
MERGE (c)-[:HAS {TYPE:line.type, VALUE:toInteger(line.value)}]->(p)
RETURN count(*);

MATCH (c)-[cp]->(p) RETURN c,cp,p;

cheatsheet:
https://gist.github.com/DaniSancas/1d5265fc159a95ff457b940fc5046887
'''

#import libraries and define paramters
from neo4j import GraphDatabase
import spacy

#define the parameters, host, query and keywords
uri = "你的Neo4j Aura服务器地址"
driver = GraphDatabase.driver(uri, auth=("neo4j", "你的Neo4j Aura密码")) 
session = driver.session()

check_q = ("MATCH (c:Customer)-[r:HAS]->(p:Product) " 
    "WHERE c.customer_id = $customerid AND p.product_name = $productname " 
    "RETURN DISTINCT properties(r)")

check_c = ("MATCH (c:Customer) " 
    "WHERE c.customer_id = $customerid " 
    "RETURN DISTINCT c")

update_q = ("MATCH (c:Customer)-[r:HAS]->(p:Product) " 
    "WHERE c.customer_id = $customerid AND p.product_name = $productname "
    "and r.TYPE = $attribute "
    "SET r.VALUE = toInteger($value) "
    "RETURN DISTINCT properties(r)")

intent_dict = {'check':check_q, 'login':check_c, 'update':update_q}

#list of key intent, product and attribute
product_list = ['deposit','loan']
attribute_list = ['pricing','balance']
intent_list = ['check','update']

print('loading nlp model')
nlp = spacy.load('en_core_web_lg')
tokens_products = nlp(' '.join(product for product in product_list))
tokens_intent = nlp(' '.join(intent for intent in intent_list))
tokens_attribute = nlp(' '.join(attribute for attribute in attribute_list))

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

    for token in tokens:
        for intent in tokens_intent:
            curr_intent_score = token.similarity(intent)
            if curr_intent_score > intent_score and curr_intent_score > threshold:
                intent_score = curr_intent_score
                final_intent = intent.text

        for product in tokens_product:
            curr_product_score = token.similarity(product)
            if curr_product_score > product_score and curr_product_score > threshold:
                product_score = curr_product_score
                final_product = product.text
                    
        for attribute in tokens_attribute:
            curr_attribute_score = token.similarity(attribute)
            if curr_attribute_score > attribute_score and curr_attribute_score > threshold:
                attribute_score = curr_attribute_score
                final_attribute = attribute.text

        if token.pos_ == 'NUM' and token.text.isdigit():
            final_attribute_value = token.text

    print('matching...')
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
        name = input('Hello, What is your name? ')
        print('Hi '+name)
        #check for login
        query_str = intent_dict['login']
        result = session.read_transaction(run_query, query_str, name, product,attribute,attribute_val)
        if len(result)==0:
            print('Failed to find '+name)
            print('Press http://packtpub.com to register your account')
            name =''
            continue
    
    #Sentences Intent and Entities Extraction
    input_sentence = input('What do you like to do? ')
    if input_sentence == "reset":
        reset = True 
    entities = intent_entity_attribute_extraction(nlp, input_sentence,tokens_intent, tokens_products, tokens_attribute)
    #actually can build another intent classifier here based on the scores and words matched as features, as well as previous entities
    intent = entities[0]
    product = entities[1]
    attribute = entities[2]
    attribute_val = entities[3]

    #cross-check for missing information
    while intent == '':
        input_sentence = input('What do you want to do?')
        entities = intent_entity_attribute_extraction(nlp, input_sentence,tokens_intent, tokens_products, tokens_attribute)
        intent = entities[0]

    while product == '':
        input_sentence = input('What product do you want to check?')
        entities = intent_entity_attribute_extraction(nlp, input_sentence,tokens_intent, tokens_products, tokens_attribute)
        product = entities[1]

    while attribute == '':
        input_sentence = input('What attribute of the ' + product +' that you want to '+intent+'?')
        entities = intent_entity_attribute_extraction(nlp, input_sentence,tokens_intent, tokens_products, tokens_attribute)
        attribute = entities[2]

    #execute the query to extract the answer
    query_str = intent_dict[intent]
    results = session.read_transaction(run_query, query_str, name,product,attribute,attribute_val)
    if len(results) >0:
        for result in results:
            if result['TYPE'] == attribute:
                print(attribute + ' of ' + product + ' is '+str(result['VALUE']))
    else:
        print('no record')
