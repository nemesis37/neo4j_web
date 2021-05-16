
# coding=utf-8
from flask import Flask, jsonify, render_template
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "wzz900903")) #认证连接数据库



app = Flask(__name__) #flask框架必备

def buildNodes(nodeRecord): #构建web显示节点
    data = {"id": nodeRecord._id, "label": list(nodeRecord._labels)[0]} #将集合元素变为list，然后取出值
    data.update(dict(nodeRecord._properties))

    return {"data": data}


def buildEdges(relationRecord): #构建web显示边
    data = {"source": relationRecord.start_node._id,
            "target":relationRecord.end_node._id,
            "relationship": relationRecord.type}

    return {"data": data}


@app.route('/')#建立路由，指向网页
def index():
    return render_template('index.html')

@app.route('/graph')#两个路由指向同一个网页，返回图的节点和边的结构体
def get_graph():
    # nodes = list(map(buildNodes, graph.run('MATCH (n) RETURN n').data()))
    #
    # edges = list(map(buildEdges, graph.run('MATCH ()-[r]->() RETURN r').data()))
    # elements = {"nodes": nodes, "edges": edges}

    with driver.session() as session:
        results=session.run('MATCH (p1{name:"Laurence Fishburne"})-[r1:ACTED_IN]->(m)<-[r2:DIRECTED]-(p2)  RETURN p1,m,p2,r1,r2').values()
        nodeList=[]
        edgeList=[]
        for result in results:
            nodeList.append(result[0])
            nodeList.append(result[1])
            nodeList.append(result[2])
            nodeList=list(set(nodeList))
            edgeList.append(result[3])
            edgeList.append(result[4])

        nodes = list(map(buildNodes, nodeList))
        edges= list(map(buildEdges,edgeList))
    return jsonify(elements = {"nodes": nodes, "edges": edges})


if __name__ == '__main__':
    app.run(debug = True) #flask框架必备
