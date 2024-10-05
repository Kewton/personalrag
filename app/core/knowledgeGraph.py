from app.core.config import OPENAI_API_KEY
from openai import OpenAI
from neo4j import GraphDatabase
import json

# OpenAI APIキーを設定
chatgptapi_client = OpenAI(
  api_key=OPENAI_API_KEY
)


class KnowledgeGraph:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_labels_and_properties(self, tx):
        # すべてのラベルを取得するクエリ
        label_query = "CALL db.labels()"
        result = tx.run(label_query)
        
        labels = [record["label"] for record in result]
        
        # 各ラベルのプロパティを取得するクエリ
        label_properties = {}
        for label in labels:
            property_query = f"""
            MATCH (n:{label})
            WITH DISTINCT keys(n) AS props
            UNWIND props AS prop
            RETURN DISTINCT prop
            """
            prop_result = tx.run(property_query)
            properties = [record["prop"] for record in prop_result]
            label_properties[label] = properties
        
        return label_properties

    # LLMを使って文章を解析
    def analyze_text_with_llm_to_get_labellistAndpropertieslist(self, text):
        labellist = []
        propertieslist = []
        with self.driver.session() as session:
            label_properties = session.execute_read(self.get_labels_and_properties)

        # 結果を表示
        for label, properties in label_properties.items():
            labellist.append(label)
            propertieslist = propertieslist + properties

        labellist = list(set(labellist))
        propertieslist = list(set(propertieslist))

        print(f"Label: {labellist}")
        print(f"Properties: {propertieslist}")
        print("------------------------")

        _prompt = {
            "命令書": "neo4jにててナレッジグラフを作成しています。入力文を分析して入力labellistと入力propertiesに不足しているラベルと属性情報を抽出すること。",
            "制約条件": [
                "jsonフォーマットで出力すること",
                "出力結果はjson.loadsで正しくパースできること",
                "ラベルについては次の考え方に準拠すること。ラベルは大きな分類やエンティティの「型」や「カテゴリ」を表す際に使用します。ノードの種類（人、会社、製品など）や、ノードに対して持たせるべき主要な役割（顧客、従業員など）を示します。",
                "属性情報については次のの考え方に準拠すること。プロパティは個別のノードに関する詳細な情報や属性値を保存するのに適しています。特に、クエリのフィルタリング条件やソートの条件として頻繁に利用されるデータは、プロパティとして保存されるべきです。",
                "出力labellistと出力propertieslistは文字列のListとして出力すること"
            ],
            "入力labellist": labellist,
            "入力properties": propertieslist,
            "入力文": text,
            "出力文フォーマット": {
                "labellist": [],
                "propertieslist": []
            }
        }
        prompt_text = json.dumps(_prompt, ensure_ascii=False)
        input_messages = []
        input_messages.append({"role": "system", "content": "You are an assistant who helps extract knowledge from text."})
        input_messages.append({"role": "user", "content": prompt_text})

        response = chatgptapi_client.chat.completions.create(
            model="gpt-4o-mini",  # もしくは 'gpt-4' を指定可能
            messages=input_messages,
            response_format={"type": "json_object"},
        )
        
        print(response.choices[0].message.content)

        labellistAndpropertieslist_result = json.loads(response.choices[0].message.content)
        labellist = labellist + labellistAndpropertieslist_result['labellist']
        propertieslist = propertieslist + labellistAndpropertieslist_result['propertieslist']
        return list(set(labellist)), list(set(propertieslist))

    # LLMを使って文章を解析
    def analyze_text_with_llm(self, text, rabel_list, prop_list):
        _prompt = {
            "命令書": "次のテキストを分析して主要なエンティティと関係を抽出すること。また、各エンティティにラベルと属性情報を付与すること。",
            "制約条件": [
                "neo4jに入力可能であること",
                "網羅的であること",
                "jsonフォーマットで出力すること",
                "エンティティは実世界のオブジェクトや概念を表す（人、会社、製品など）こと",
                "一般名称をエンティティとして登録する場合は形容詞をつけて特定可能にすること",
                "独立したオブジェクトや概念を表す場合はエンティティで表現すること",
                "固有の属性（名前、年齢、価格など）を持たせたいときはエンティティとして表現すること",
                "エンティティ同士の関連性を示したい場合には、リレーションシップを使うこと",
                "リレーションシップには、since（開始日）、weight（関係の強度）などのプロパティを持たせることができるため、関係自体に追加の情報が必要な場合に使用すること",
                "出力結果はjson.loadsで正しくパースできること",
                "指定のラベルを使用すること",
                "指定のラベルが不足している場合、不足しているラベルを出力すること"
            ],
            "指定ラベル": rabel_list,
            "指定属性情報": prop_list,
            "入力文": text,
            "出力文フォーマット": {
                "entities": "",
                "relationships": ""
            },
            "サンプル": {
                "入力文サンプル": "Alice and Bob are friends. Alice has graduated from college and works for Tech Corporation.",
                "出力文サンプル": {
                    "entities": [
                        {
                            "name": "Alice",
                            "label": "Person",
                            "properties": {
                                "age": 30,
                                "city": "London"
                            }
                        },
                        {
                            "name": "Bob", 
                            "label": "Person",
                            "properties": {
                                "age": 33,
                                "city": "Tokyo"
                            }
                        },
                        {
                            "name": "TechCorp",
                            "label": "Company",
                            "properties": {
                                "age": 33,
                                "city": "Pari"
                            }
                        }
                    ],
                    "relationships": [
                        {"entity1": "Alice", "label1": "Person", "entity2": "Bob", "label2": "Person", "relationship": "FRIEND"},
                        {"entity1": "Alice", "label1": "Person", "entity2": "TechCorp", "label2": "Company", "relationship": "WORKS_AT"}
                    ]
                }
            }
        }
        prompt_text = json.dumps(_prompt, ensure_ascii=False)
        input_messages = []
        input_messages.append({"role": "system", "content": "You are an assistant who helps extract knowledge from text."})
        input_messages.append({"role": "user", "content": prompt_text})

        response = chatgptapi_client.chat.completions.create(
            model="gpt-4o-mini",  # もしくは 'gpt-4' を指定可能
            messages=input_messages,
            response_format={"type": "json_object"},
        )
        
        return response.choices[0].message.content

    # 解析結果をNeo4jに保存
    def store_knowledge_in_neo4j(self, entities, relationships):
        with self.driver.session() as session:
            # エンティティとリレーションシップをNeo4jに保存
            for entity in entities:
                session.write_transaction(self._create_entity, entity['name'], entity['label'], entity.get('properties', {}))
            for rel in relationships:
                session.write_transaction(self._create_relationship, rel['entity1'], rel['label1'], rel['entity2'], rel['label2'], rel['relationship'], rel.get('properties', {}))

    @staticmethod
    def _create_entity(tx, name, label, properties):
        # プロパティの動的な設定を準備
        properties_str = ', '.join([f"{key}: ${key}" for key in properties.keys()])
        # エンティティ（ノード）の作成クエリ
        query = (
            f"MERGE (e:{label} {{name: $name}}) "
        )
        # プロパティがある場合、それをセット
        if properties:
            query += f"SET e += {{{properties_str}}} "
        query += "RETURN e"
        
        # クエリ実行時にプロパティを渡す
        tx.run(query, name=name, **properties)

    @staticmethod
    def _create_relationship(tx, entity1, label1, entity2, label2, relationship, properties):
        # プロパティの動的な設定を準備
        properties_str = ', '.join([f"{key}: ${key}" for key in properties.keys()])
        # リレーションシップ作成クエリ
        query = (
            f"MATCH (a:{label1} {{name: $entity1}}), (b:{label2} {{name: $entity2}}) "
            f"MERGE (a)-[r:{relationship}]->(b) "
        )
        # プロパティがある場合、それをセット
        if properties:
            query += f"SET r += {{{properties_str}}} "
        query += "RETURN a, b, r"
        
        # クエリ実行時にプロパティを渡す
        tx.run(query, entity1=entity1, entity2=entity2, **properties)

    # テキスト解析とナレッジグラフの登録を一連の処理として実行
    def analyze_and_store_knowledge(self, text):
        # 0. テキストを解析しラベルと属性情報を取得
        labellist, propertieslist = self.analyze_text_with_llm_to_get_labellistAndpropertieslist(text)

        # 1. テキストを解析しエンティティとリレーションシップを取得
        analysis_result = self.analyze_text_with_llm(text, labellist, propertieslist)

        # 解析結果をパース（OpenAIの返答がJSON形式で返ってくると仮定）
        result = json.loads(analysis_result)

        print("---")
        print(result)
        print("---")
        entities = result['entities']
        relationships = result['relationships']

        # 2. Neo4jにエンティティとリレーションシップを保存
        self.store_knowledge_in_neo4j(entities, relationships)
    
    def do(self, text):
        self.analyze_and_store_knowledge(text)
        self.close()

