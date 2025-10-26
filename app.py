from dotenv import load_dotenv
load_dotenv()

#条件の整理
#画面に入力フォームを１つ用意
#入力フォームから送信したテキストをLangChainを使ってLLMにプロンプトとして
#渡し、その回答が画面に表示されるようにする
#ラジオボタンでLLMに振舞わせる専門家の種類を選択
#Aを選択：金融の専門家として振舞う
#Bを選択：健康管理の専門家として振舞う
#LLMに選択値に応じてLLMに渡すプロンプトのシステムメッセージを変える
#「入力テキスト」と「ラジオボタンでの選択値」を引数として受け取り
#LLMからの回答を戻り値として返す関数を定義して利用する
#WEBアプリの概要と操作方法をユーザーに明示するためのテキストを表示する
#Streamlit Community Cloudにデプロイすることを想定してコードを書く
#デプロイするときのPythonのバージョンは「3.11」を選択する

#必要な環境設定をインポート
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

#llm呼び出し関数
def get_llm_response(user_input: str, expert_type: str) -> str:
    """
    入力テキストと専門家タイプを基にLLMからの回答を取得する関数
    """
    if expert_type == "金融の専門家":
        system_prompt = "あなたは金融の専門家です。専門的な知識に基づき、わかりやすく説明してください。"
    elif expert_type == "健康の専門家":
        system_prompt = "あなたは健康の専門家です。栄養、運動、生活習慣などの観点から適切に助言してください。"
    else:
        system_prompt = "あなたは質問者に丁寧に応対する優秀なアシスタントです。"

    chat = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    response = chat(messages)
    return response.content

#st.set_page_config(page_title="専門家AIアシスタント", page_icon="💬")

st.title("💬 専門家AIアシスタント")
st.write("""
このアプリは **LangChain + Streamlit** を利用したサンプルアプリです。  
下記の手順で操作できます👇
1. 「専門家の種類」を選択  
2. テキストを入力  
3. 「送信」ボタンを押すと、選んだ専門家としてAIが回答します。
""")

# ラジオボタンで専門家を選択
expert_type = st.radio(
    "AIの専門家としての役割を選択してください：",
    ("金融の専門家", "健康の専門家")
)

# テキスト入力フォーム
user_input = st.text_area("質問や相談内容を入力してください：", height=150)

# 送信ボタン
if st.button("送信"):
    if user_input.strip():
        with st.spinner("AIが回答を生成中です..."):
            answer = get_llm_response(user_input, expert_type)
        st.success("回答：")
        st.write(answer)
    else:
        st.warning("テキストを入力してください。")

st.caption("※ このアプリはデモ用です。実際の専門的判断を代替するものではありません。")
