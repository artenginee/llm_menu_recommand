import gradio as gr
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# LLM invoke 호출하여 food 변수값 얻어옴
def generate_food_name(food: str) -> dict[str, str]:
    # 모델 설정
    model = ChatOpenAI(model="gpt-3.5-turbo")
    # str 타입 출력을 위한 파서 설정
    parser = StrOutputParser()
    # 프롬프트 작성
    system_template = "점심 메뉴로 {food} 음식 중에 랜덤하게 1개를 추천해줘. 음식 이름만 말해줘"
    # 프롬프트 템플릿 사용하여 입출력 설정
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template)]
    )
    # Langchain 활용 : 템플릿 > 모델 > 파서 순서로 동작
    chain = prompt_template | model | parser

    result = chain.invoke({"food": food})
    print(result)
    return result

# LLM API 호출하여 응답 수신
def update_outputs(food: str) -> tuple[str, str]:
    response = generate_food_name(food)

    return f"# {response}"

# Gradio UI 
with gr.Blocks() as app:
    gr.Markdown("# 1. 음식 메뉴 추천")

    # with gr.Row():
    #     # 선호 음식 input
    #     with gr.Column(scale=1) as left:
    #         input_food = gr.Dropdown(
    #             ["한식", "중식", "일식", "양식", "무작위"],
    #             label="어떤 종류 음식을 먹고 싶나요?",
    #         )

    #     # 추천 음식 output
    #     with gr.Column(variant="panel", scale=4) as right:
    #         out_menu_name = gr.Markdown()
    #         out_menu_reason = gr.Markdown()
            
    #         # Dropdown 변경 시 LLM 호출
    #         input_food.change(
    #             fn=update_outputs,
    #             inputs=input_food,
    #             outputs=out_menu_name,
    #         )

# gradio app 실행
app.launch()
