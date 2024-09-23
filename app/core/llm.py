from openai import OpenAI
from app.core.config import OPENAI_API_KEY, CLAUDE_API_KEY
import anthropic
import json


chatgptapi_client = OpenAI(
  api_key=OPENAI_API_KEY
)

claude_client = anthropic.Anthropic(
    api_key=CLAUDE_API_KEY,
)


def personalrag(_inquery, _similarity_search_result):
    # context = "\n".join([document.page_content for document in _similarity_search_result])

    #context = json.loads(_similarity_search_result)
    context = _similarity_search_result
    # context = _similarity_search_result

    _prompt = f"""
    # 命令書:
    あなたは、優秀なAIアシスタントです。
    以下の制約条件とContextと入力文をもとに、最高の結果を出力してください。

    # 制約条件
    - 入力文を誤解を招かない明確な表現に是正してください
    - Contextの情報を誤解を招かない明確な表現に是正してください
    - Contextの情報の一部誤っている箇所については是正してください
    - Contextの情報の完全に誤っている箇所については削除してください
    - Contextの情報の入力文に対する回答のために不要な箇所は削除してください
    - Contextの情報が不足している場合は出力文の生成に必要な情報を補ってください
    - 出力文は以下のフォーマットに従ってください
    - 是正後の入力文
    - 是正後のContext
    - 補ったContext
    - 入力文に対する回答

    # Context:
    {context["similarity_search_result"]}

    # 入力文:
    {_inquery}

    # 出力文
    """

    _prompt = {
        "命令書": "あなたは、優秀なAIアシスタントです。以下の制約条件とContextと入力文をもとに、最高の結果を出力してください。",
        "制約条件": [
            "入力文を誤解を招かない明確な表現に是正してください",
            "Contextの情報を誤解を招かない明確な表現に是正してください",
            "Contextの情報の一部誤っている箇所については是正してください",
            "Contextの情報の完全に誤っている箇所については削除してください",
            "Contextの情報の入力文に対する回答のために不要な箇所は削除してください",
            "Contextの情報が不足している場合は出力文の生成に必要な情報を補ってください"
        ],
        "Context": context["similarity_search_result"],
        "入力文": _inquery,
        "出力文フォーマット": {
            "input_statement_after_correction": "",
            "context_after_correction": "",
            "supplemented_context": "",
            "answer_to_input_sentence": ""
        }
    }

    _prompt = json.dumps(_prompt, ensure_ascii=False, indent=4)

    messages = []
    messages.append({"role": "system", "content": "あなたは優秀なAIアシスタントです。"})
    messages.append({"role": "user", "content": _prompt})
    
    content, role = execLlmApi(selected_model="gpt-4o-mini", messages=messages, encoded_file="")
    print(role)
    #content = json.dumps(content, ensure_ascii=False, indent=4)
    content = json.loads(content)
    return content


def execLlmApi(selected_model, messages, encoded_file):
    """
    out:
        {}:content
        string:role
    """
    if "gpt" in selected_model:
        if "gpt-4o" == selected_model and len(encoded_file) > 0:
            _inpurt_messages = []
            _inpurt_messages.append(messages[0])
            _inpurt_messages.append(
                {"role": "user", "content": [
                    {"type": "text", "text": messages[1]["content"]},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_file}"}}
                ]}
            )
            response = chatgptapi_client.chat.completions.create(
                model=selected_model,
                messages=_inpurt_messages
            )
        else:
            response = chatgptapi_client.chat.completions.create(
                model=selected_model,
                messages=messages
            )
        #print("_messages = ")
        #print(messages)
        return response.choices[0].message.content, response.choices[0].message.role

    elif "claude" in selected_model:
        _inpurt_messages = []

        for _rec in messages:
            if _rec["role"] == "system":
                _systemrole = _rec["content"]
            elif _rec["role"] == "user":
                if len(encoded_file) > 0:
                    print("append image")
                    _content = []
                    _content.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": encoded_file
                        }
                    })
                    _content.append({
                        "type": "text",
                        "text": _rec["content"]
                    })
                    
                    _inpurt_messages.append(
                        {
                            "role": _rec["role"],
                            "content": _content
                        }
                    )
                else:
                    _inpurt_messages.append(_rec)

        response = claude_client.messages.create(
            max_tokens=4096,
            system=_systemrole,
            model=selected_model,
            messages=_inpurt_messages
        )

        return response.content[0].text, response.role
    else:
        return {}, ""
