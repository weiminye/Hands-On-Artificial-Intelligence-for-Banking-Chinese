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

'''
将使用Neo4j云服务，即Neo4j Aura导入，参考文档：https://neo4j.com/docs/aura/current/getting-started/importing-data/

LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/weiminye/Hands-On-Artificial-Intelligence-for-Banking-Chinese/main/%E7%AC%AC7%E7%AB%A0/%E4%BE%8B%E5%AD%902%E4%B8%8A%E5%B8%82%E5%85%AC%E5%8F%B8%E5%85%AC%E5%91%8A/%E8%8B%B1%E6%96%87%E5%8E%9F%E7%89%88%E4%BE%8B%E5%AD%90/node.csv" AS row
CREATE (:ENTITY {node: row.nodename});

CREATE INDEX ON :ENTITY(node);

LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/weiminye/Hands-On-Artificial-Intelligence-for-Banking-Chinese/main/%E7%AC%AC7%E7%AB%A0/%E4%BE%8B%E5%AD%902%E4%B8%8A%E5%B8%82%E5%85%AC%E5%8F%B8%E5%85%AC%E5%91%8A/%E8%8B%B1%E6%96%87%E5%8E%9F%E7%89%88%E4%BE%8B%E5%AD%90/edge.csv" AS row
MATCH (vertex1:ENTITY {node: row.nodename1})
MATCH (vertex2:ENTITY {node: row.nodename2})
MERGE (vertex1)-[:LINK]->(vertex2);

通过上面语句导入数据之后，执行下面语句查看数据
MATCH (n:ENTITY)-[:LINK]->(ENTITY) RETURN n;


'''
