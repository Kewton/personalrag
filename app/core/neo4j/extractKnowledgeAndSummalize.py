from app.core.config import OPENAI_API_KEY
from openai import OpenAI
from neo4j import GraphDatabase
import json

# OpenAI APIキーを設定
chatgptapi_client = OpenAI(
  api_key=OPENAI_API_KEY
)


class ExtractKnowledgeAndSummalize:

    def __init__(self, uri, user, password):
        # Neo4jドライバの作成
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # ドライバのクローズ
        self.driver.close()

    # Neo4jからラベルの一覧を取得
    def get_labels(self):
        with self.driver.session() as session:
            result = session.run("CALL db.labels() YIELD label RETURN label")
            return [record["label"] for record in result]

    # LLMを使って入力文を解析し、エンティティとリレーションシップを抽出
    def analyze_text_with_llm(self, text, labels):
        _prompt = {
            "命令書": "Analyze the following text and extract entities and keywords based on the available labels.",
            "制約条件": [
                "neo4jに入力可能であること",
                "網羅的であること",
                "jsonフォーマットで出力すること"
            ],
            "ラベル": labels,
            "入力文": text,
            "出力文フォーマット": {
                "entities": "",
                "keywords": ""
            },
            "サンプル": {
                "入力文サンプル": "Alice and Bob are friends. Alice works at TechCorp.",
                "出力文サンプル": {"entities": [{"name": "Alice", "label": "Person"}], "keywords": ["friends", "TechCorp"]}
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
        
        #print("----")
        #print(response.choices[0].message.content)
        #print("----")
        return response.choices[0].message.content

    # Neo4jにエンティティやキーワードを基にクエリを実行してナレッジを抽出
    def query_knowledge_from_neo4j(self, entities, keywords):
        keywordslist = keywords
        resutllist = []
        with self.driver.session() as session:
            # エンティティに基づくナレッジを抽出
            for entity in entities:
                keywordslist.append(entity['name'])
                print("----")
                print(f"Extracting knowledge for entity: {entity['name']}")
                print("----")
                label = entity.get('label', 'DefaultLabel')  # ラベルがない場合はデフォルトにフォールバック
                if label not in self.get_labels():
                    print(f"Warning: Label '{label}' does not exist in the database. Skipping...")
                    continue
                result = session.execute_read(self._query_entity_knowledge, entity['name'], label)
                for record in result:
                    _result = self.format_result(record)
                    print("@"*50)
                    print(_result)
                    # return f"Entity: {entity}, Relationship: {relationship}, Related Entity: {related_entity}"
                    keywordslist.append(_result["Entity"])
                    keywordslist.append(_result["relationship"])
                    keywordslist.append(_result["Related Entity"])
                    # resutllist.append(_result)
            unique_keywordslist = list(set(keywordslist))

            print("-- unique_keywordslist --")
            print(unique_keywordslist)
            # キーワードに基づくナレッジを抽出
            for keyword in unique_keywordslist:
                print("----")
                print(f"Extracting knowledge for keyword: {keyword}")
                result = session.execute_read(self._query_keyword_knowledge, keyword)
                #print("----")
                #for record in result:
                #    _result = self.format_result(record)
                #    print(_result)
                #    # resutllist.append(_result)

                for record in result:
                    print("####")
                    # エンティティ e
                    entity = record['e']
                    entity_properties = record['entity_properties']
                    print(f"Entity: {entity['name']} ({', '.join(entity.labels)})")
                    print(f"Properties: {entity_properties}")
                    
                    # リレーションシップ r
                    relationship_type = record['relationship_type']
                    relationship_properties = record['relationship_properties']
                    print(f"Relationship: {relationship_type}")
                    print(f"Relationship Properties: {relationship_properties}")
                    
                    # 関連するエンティティ related_entity
                    related_entity = record['related_entity']
                    related_entity_properties = record['related_entity_properties']
                    print(f"Related Entity: {related_entity['name']} ({', '.join(related_entity.labels)})")
                    print(f"Related Entity Properties: {related_entity_properties}")
                    print("-" * 50)

                    resutllist.append({
                        "Entity": f"{entity['name']} ({', '.join(entity.labels)})",
                        "Properties": f"{entity_properties}",
                        "Relationship": relationship_type,
                        "Relationship Properties": relationship_properties,
                        "Related Entity": f"{related_entity['name']} ({', '.join(related_entity.labels)})",
                        "Related Entity Properties": related_entity_properties
                    })

        return resutllist

    @staticmethod
    def _query_entity_knowledge(tx, entity_name, entity_label):
        # エンティティに関連するナレッジを検索するクエリ
        query = (
            f"MATCH (e:{entity_label} {{name: $entity_name}})-[r]->(related_entity) "
            "RETURN e, r, related_entity"
        )
        result = tx.run(query, entity_name=entity_name)
        return list(result)  # 結果をリストにしてトランザクションが閉じられても使用できるようにする

    @staticmethod
    def _query_keyword_knowledge(tx, keyword):
        # 特定のプロパティにキーワードが含まれるかを検索
        query = (
            "MATCH (e)-[r]->(related_entity) "
            "WHERE e.name CONTAINS $keyword OR "
            "      related_entity.name CONTAINS $keyword OR "
            "      e.description CONTAINS $keyword OR "
            "      related_entity.description CONTAINS $keyword OR "
            "      r.comment CONTAINS $keyword "
            "RETURN e, properties(e) AS entity_properties, "
            "       r, type(r) AS relationship_type, properties(r) AS relationship_properties, "
            "       related_entity, properties(related_entity) AS related_entity_properties"
        )
        result = tx.run(query, keyword=keyword)
        return list(result)

    @staticmethod
    def format_result(record):
        """結果をフォーマットして出力"""
        entity = record['e']['name']
        related_entity = record['related_entity']['name']
        relationship = record['r'].type  # 修正: .type() ではなく .type に変更
        result = {
            "Entity": entity,
            "relationship": relationship,
            "Related Entity": related_entity
        }
        # return f"Entity: {entity}, Relationship: {relationship}, Related Entity: {related_entity}"
        return result

    def analyze_and_extract_knowledge(self, text):
        # 1. Neo4jからラベルの一覧を取得
        labels = self.get_labels()
        print(f"-- labels --\n{labels}\n------------")

        # 2. LLMで入力文を解析し、ラベルに基づいたエンティティとキーワードを抽出
        analysis_result = self.analyze_text_with_llm(text, labels)
        print(f"----\n{analysis_result}\n----")

        # 3. 解析結果をパース
        result = json.loads(analysis_result)
        entities = result.get('entities', [])
        keywords = result.get('keywords', [])

        # 4. Neo4jからナレッジを抽出
        return self.query_knowledge_from_neo4j(entities, keywords)

    def generate_summary_with_llm(self, text, knowledge):
        summary_prompt = {
            "命令書": "ナレッジグラフを入力文に関連づけて人間が理解可能な要約文を生成すること",
            "制約条件": [
                ""
            ],
            "入力文": text,
            "ナレッジグラフ": knowledge
        }
        
        prompt_text = json.dumps(summary_prompt, ensure_ascii=False)
        input_messages = []
        input_messages.append({"role": "system", "content": "You are a knowledge summarizer."})
        input_messages.append({"role": "user", "content": prompt_text})
        print("====")
        print(prompt_text)
        print("====")
        response = chatgptapi_client.chat.completions.create(
            model="gpt-4o-mini",  # もしくは 'gpt-4' を指定可能
            messages=input_messages
        )
        return response.choices[0].message.content
    
    def do(self, text):
        # テキストを解析してNeo4jからナレッジを抽出
        resutllist = self.analyze_and_extract_knowledge(text)

        analysis_result = self.generate_summary_with_llm(text, resutllist)
        print(analysis_result)
        #result = json.loads(analysis_result)
        #print(result)

        # 接続を終了
        self.close()
        return analysis_result