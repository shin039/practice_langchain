from dotenv import load_dotenv
from langsmith import Client
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field

from langchain.smith import RunEvalConfig, run_on_dataset

# .envファイルから環境変数を読み込む
load_dotenv()

client = Client()
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ------------------------------------------------------------------------------
# Create inputs and reference outputs
# ------------------------------------------------------------------------------
# NOTE： 最初にデータセットは作成済み。
# examples = [
#     (
#         "Which country is Mount Kilimanjaro located in?",
#         "Mount Kilimanjaro is located in Tanzania.",
#     ),
#     (
#         "What is Earth's lowest point?",
#         "Earth's lowest point is The Dead Sea.",
#     ),
# ]
#
# inputs = [{"question": input_prompt} for input_prompt, _ in examples]
# outputs = [{"answer": output_answer} for _, output_answer in examples]
#
# # Programmatically create a dataset in LangSmith
# dataset = client.create_dataset(
#     dataset_name="Sample dataset", description="A sample dataset in LangSmith."
# )
#
# # Add examples to the dataset
# client.create_examples(inputs=inputs, outputs=outputs, dataset_id=dataset.id)


# ------------------------------------------------------------------------------
# Define what you want to evaluate
# ------------------------------------------------------------------------------
# Define the application logic you want to evaluate inside a target function
# The SDK will automatically send the inputs from the dataset to your target function
def target(inputs: dict) -> dict:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "次の質問に正確に答えてください"),
            ("user", "{question}"),
        ]
    )
    output = StrOutputParser()

    chain = prompt | model | output
    student_answer = chain.invoke(inputs["question"])
    return {"student_answer": student_answer}


# ------------------------------------------------------------------------------
# Define Evaluator
# ------------------------------------------------------------------------------
# Define instructions for the LLM judge evaluator
instructions = """
学生の解答を正解と比較して概念的類似性を評価し、真または偽と分類してください：
- 偽：概念的な一致と類似性がない
- 真：概念的な一致と類似性がほとんどあるか完全にある
- 主要基準：概念が一致すべきであり、正確な言い回しではない。
"""


# Define output schema for the LLM judge
class Grade(BaseModel):
    score: bool = Field(description="参照回答に対して応答が正確かどうかを示すブール値")


# Define LLM judge that grades the accuracy of the response relative to reference output
def accuracy(outputs: dict, reference_outputs: dict) -> bool:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", instructions),
            (
                "user",
                "本当の答え: {g_answer}; 学生の答え: {s_answer}",
            ),
        ]
    )
    chain = prompt | model.with_structured_output(Grade)
    response = chain.invoke(
        {
            "g_answer": reference_outputs[
                "answer"
            ],  # Datasetのreference_outputsのanswer
            "s_answer": outputs[
                "student_answer"
            ],  # targetメソッドのoutputsのstudentansser
        }
    )

    return response.score


def custome_metrics(outputs: dict, reference_outputs: dict) -> dict:
    return {"bool": True, "score": 30, "explanation": "This is a test"}


# ------------------------------------------------------------------------------
# Run and view results
# ------------------------------------------------------------------------------
# After running the evaluation, a link will be provided to view the results in langsmith
experiment_results = client.evaluate(
    target,
    data="Sample dataset",
    evaluators=[
        accuracy,
        custome_metrics,
    ],
    experiment_prefix="first-eval-in-langsmith",
    max_concurrency=2,
)

# ------------------------------------------------------------------------------
# Use LangChain.langsmigh run_on_dataset
#   -> https://api.python.langchain.com/en/latest/langchain/evaluation/langchain.evaluation.schema.EvaluatorType.html#langchain.evaluation.schema.EvaluatorType
# ------------------------------------------------------------------------------
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "次の質問に正確に答えてください"),
#         ("user", "{question}"),
#     ]
# )
# output = StrOutputParser()
# chain = prompt | model | output
#
# eval_config = RunEvalConfig(
#     evaluators=["qa"],
# )
#
# chain_results = run_on_dataset(
#     client,
#     dataset_name="Sample dataset",
#     llm_or_chain_factory=chain,
#     evaluation=eval_config,
# )
