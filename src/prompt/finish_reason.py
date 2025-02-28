from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

# .envファイルから環境変数を読み込む
load_dotenv()


# LLM の初期化
llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=500)
parser = StrOutputParser()


# 継続的に出力を取得する関数
def fetch_full_response(question):
    messages = [{"role": "user", "content": question}]
    full_response = ""
    finish_reason = None

    while finish_reason != "stop":
        response = llm.invoke(messages)  # LLM にリクエスト
        content = response.content
        finish_reason = response.response_metadata[
            "finish_reason"
        ]  # finish_reasonを取得

        # DEBUG: 途中経過の出力を出す。
        print(f"------ Finish_Reason: {finish_reason}")
        print(content)

        full_response += content
        messages.append({"role": "assistant", "content": content})

        if finish_reason == "stop":
            break  # 生成が完了したらループを抜ける

    return full_response


# LCELでRunnableとして構築
chain = RunnableLambda(fetch_full_response)

# 実行
question = "AIの歴史について詳しく説明してください。"
result = chain.invoke(question)  # ここを str に修正
print(result)
