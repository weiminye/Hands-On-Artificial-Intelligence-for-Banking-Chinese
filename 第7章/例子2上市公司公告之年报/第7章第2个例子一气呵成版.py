print('请输入你的neo4j数据库密码')
# 读取用户输入的密码
neo4jpassword = input()
# neo4jpassword= "neo4jPassword"

'''*************************************
#1. Import relevant libraries and variables

'''
#custom made function
import lib_entitiesExtraction as entitiesExtraction
import lib_parser_pdf as pdf_parser
import json
import sqlite3

pdf_path = 'annualrpt/NYSE_DUK_2017.pdf'

print('parse PDF')
text_org = pdf_parser.convert_pdf_to_txt(pdf_path)

print('text cleansing')
text = text_org.replace('\r', ' ').replace('\n', ' ').replace('\s',' ')

'''*************************************
#2. NLP

'''
#Named Entity Extraction
print('ner')
#see if we need to convert everthing to lower case words - we keep the original format for this case
lower=False
common_words, sentences, words_list,verbs_list = entitiesExtraction.NER_topics(text,lower)
entities_in_sentences = entitiesExtraction.org_extraction(text)

ents_dict = {}

sentence_cnt = 0

#create this list to export the list of ent and cleanse them
f_ent = open('entities.txt','w+',encoding='utf-8')
ent_list=[]

print('looping sentences')
for sentence in entities_in_sentences:
    ents_dict[sentence_cnt] = {}
    for entity in sentence:
        ent_type = entity[1]
        ent_name = entity[0]
        ent_name = ent_name.strip()

        if len(ent_name)==0 or ent_name =='':
            continue
        
        if lower == True:
            ent_name = ent_name.lower()
            
        if ent_type in( 'ORG','PERSON','FAC','NORP','GPE','LOC','PRODUCT'):
            #take only upper case (1st pos)
            if ent_name[0].islower():
                continue

            if ent_type not in ents_dict[sentence_cnt]:
                ents_dict[sentence_cnt][ent_type]=[]

            ents_dict[sentence_cnt][ent_type].append(ent_name)

            if ent_name not in ent_list:
                ent_list.append(ent_name)
                f_ent.write(ent_name+'\t'+ent_name+'\n')
            ents_dict[sentence_cnt]['VERB'] = verbs_list[sentence_cnt]
        else:
            ents_dict[sentence_cnt][ent_type] = []

    #handle other type
    for entity in sentence:
        ent_type = entity[1]
        ent_name = entity[0]
        ent_name = ent_name.strip()
        if len(ent_name)==0 or ent_name =='':
            continue
        if ent_type not in('ORG','PERSON','FAC','NORP','GPE','LOC','PRODUCT'):
            ents_dict[sentence_cnt][ent_type].append(ent_name)

    sentence_cnt+=1

f_ent.close()

#Insert the entities into SQL database
print('insert')

f = open('result.json','w+')
json.dump(ents_dict,f)

#db file
db_path = 'parsed_network.db'
db_name = 'network_db'
db_name2 = 'sentence_db'

#sql db
conn = sqlite3.connect(db_path)
c = conn.cursor()

sqlstr = "drop table "+db_name
try:
    output = c.execute(sqlstr)
except Exception:
    print('non exists')

sqlstr = "drop table "+db_name2
try:
    output = c.execute(sqlstr)
except Exception:
    print('non exists')


entity_types = ['ORG','PERSON','FAC','NORP','GPE','LOC','PRODUCT']
relation_units = ['DATE','TIME','PERCENT','MONEY','QUANTITY','ORDINAL','CARDINAL']
#create if required
print('create')
sqlstr = "CREATE TABLE IF NOT EXISTS "+db_name+"(SOURCE TEXT, SENTENCE_NO INTEGER, CON_TYPE TEXT, ENTITY TEXT, RELATION_UNIT TEXT, RELATION_VAL TEXT,VERB_LIST TEXT )"
c.execute(sqlstr)
conn.commit()
sqlstr = "CREATE TABLE IF NOT EXISTS "+db_name2+"(SOURCE TEXT, SENTENCE_NO INTEGER, SENTENCE TEXT )"
c.execute(sqlstr)
conn.commit()

for key, value in ents_dict.items():
    con_type=''
    entity=''
    relation_unit = ''
    relation_val = ''
    verb_list = ''
    #key = sentence number
    sent_item = [(pdf_path, key, str(value))]
    sqlstr = 'insert into '+db_name2+'(SOURCE, SENTENCE_NO, SENTENCE) VALUES (?,?,?)'
    c.executemany(sqlstr, sent_item)
    
    for sub_key,sub_value in ents_dict[key].items():
        for entity_type in entity_types:
            try:
                entity = str(ents_dict[key][entity_type])[1:-1]
                con_type = entity_type
                verb_list = str(ents_dict[key]['VERB'])[1:-1]
            except Exception:
                continue
        for relation in relation_units:
            try:
                relation_val = ents_dict[key][relation][0]
                relation_unit = relation
            except Exception:
                continue
    if len(con_type+entity+relation_unit+relation_val+verb_list)>0:
        item = [(pdf_path, key, con_type,entity,relation_unit,relation_val,verb_list)]
        sqlstr = 'insert into '+db_name+'(SOURCE, SENTENCE_NO, CON_TYPE, ENTITY, RELATION_UNIT,RELATION_VAL,VERB_LIST) VALUES (?,?,?,?,?,?,?)'
        c.executemany(sqlstr, item)
    if key % 10 == 0:
        conn.commit()
    
#closing out and output the results
conn.commit()
c.close()

'''*************************************
#1. Import relevant libraries and variables

'''
#generate network
import sqlite3
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

#db file
db_path = 'parsed_network.db'
db_name = 'network_db'

#sql db
conn = sqlite3.connect(db_path)
c = conn.cursor()

sql_str = "select source, entity,CON_TYPE from network_db where con_type in ('ORG','PERSON','FAC','NORP','GPE','LOC','PRODUCT') and verb_list <> '[]' group by source,CON_TYPE, entity"
df_org = pd.read_sql_query(sql_str, conn)

network_dict={}
edge_list=[]
curr_source =''
curr_entity = ''
org_list = []
person_list = []

'''*************************************
#2. generate the network with all entities connected to Duke Energy - whose annual report is parsed

'''
target_name = 'Duke Energy'
#loop through the database to generate the network format data
for index, row in df_org.iterrows():
    if curr_entity != row['SOURCE']:
        curr_source = row['SOURCE']
        network_dict[curr_source]=[]
    curr_entity = row['ENTITY']
    if len(curr_entity)==0:
        continue
    curr_entities = curr_entity.split(',')
    if len(curr_entities)>1:
        entity1=curr_entities[0].strip()
        if entity1 == '' or entity1=="'":
            curr_entities=curr_entities[1:]
            entity1 = curr_entities[0]
        network_dict[entity1]=[]
        org_list.append(entity1)
        #all entity has relationship with target company
        entry = (target_name,entity1,{'weight':1})
        edge_list.append(entry)
        for entity in curr_entities[1:]:
            entity2=entity.strip()
            if entity2=='' or entity2 =="'":
                continue
            network_dict[entity1].append(entity2)
            entry = (entity1,entity2,{'weight':1})
            edge_list.append(entry)
            org_list.append(entity2)

            entry = (target_name,entity2,{'weight':1})
            edge_list.append(entry)

#Generate the output in networkX
print('networkx')

#output the network
G = nx.from_edgelist(edge_list)
pos = nx.spring_layout(G)
# nx.draw(G, with_labels=False, nodecolor='r',pos=pos, edge_color='b')
nx.draw(G, pos=pos)
plt.savefig('network.png')

#Generate output for Neo4J
print('prep data for neo4j')
f_org_node=open('node.csv','w+',encoding='utf-8')
f_org_node.write('nodename\n')

f_person_node=open('node_person.csv','w+')
f_person_node.write('nodename\n')

f_vertex=open('edge.csv','w+',encoding='utf-8')
f_vertex.write('nodename1,nodename2,weight\n')

unique_org = set(org_list)
for entity in unique_org:
    f_org_node.write(entity+'\n')
f_org_node.close()

unique_person = set(person_list)
for entity in unique_person:
    f_person_node.write(entity+'\n')
f_person_node.close()

for edge in edge_list:
    node1, node2, weight_dict = edge
    weight = weight_dict['weight']
    f_vertex.write(node1+','+node2+','+str(weight)+'\n')
f_vertex.close()

uri = "bolt://localhost:7687"

from neo4j import GraphDatabase

driver = GraphDatabase.driver(uri, auth=("neo4j", neo4jpassword)) 
session = driver.session()

print('开始往neo4j写数据')
session.run("MATCH (n) DETACH DELETE n;")

节点df = pd.read_csv('node.csv')

#遍历节点df
for index, row in 节点df.iterrows():
    session.run("CREATE (:ENTITY {node:$node});", node=row['nodename'])

关系df = pd.read_csv('edge.csv')

#遍历节点df
for index, row in 关系df.iterrows():
    session.run("MATCH (vertex1:ENTITY {node: $node1}) MATCH (vertex2:ENTITY {node: $node2}) MERGE (vertex1)-[:LINK]->(vertex2);", node1=row['nodename1'], node2=row['nodename2'])

print('关闭neop4j连接')
session.close()
driver.close()
print('neo4j数据写入完成。可以去neo4j执行以下语句查看数据了：')
print('MATCH (n:ENTITY)-[:LINK]->(ENTITY) RETURN n;')
