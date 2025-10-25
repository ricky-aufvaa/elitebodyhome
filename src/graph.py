from langgraph.graph import StateGraph,START,END
from state import AgentState
from nodes import *

from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()


# Workflow
workflow = StateGraph(AgentState)
workflow.add_node("question_rewriter", question_rewriter)
workflow.add_node("question_classifier", question_classifier)
workflow.add_node("off_topic_response", off_topic_response)
workflow.add_node("retrieve", retrieve)
workflow.add_node("retrieval_grader", retrieval_grader)
workflow.add_node("generate_answer", generate_answer)
workflow.add_node("refine_question", refine_question)
workflow.add_node("cannot_answer", cannot_answer)

workflow.add_edge("question_rewriter", "question_classifier")
workflow.add_conditional_edges(
    "question_classifier",
    on_topic_router,
    {
        "retrieve": "retrieve",
        "off_topic_response": "off_topic_response",
    },
)
workflow.add_edge("retrieve", "retrieval_grader")
# workflow.add_conditional_edges(
#     "retrieval_grader",
#     proceed_router,
#     {
#         "generate_answer": "generate_answer",
#         "refine_question": "refine_question",
#         "cannot_answer": "cannot_answer",
#     },
# )
# workflow.add_edge("refine_question", "retrieve")
workflow.add_edge("retrieval_grader", "generate_answer")
workflow.add_edge("generate_answer", END)
# workflow.add_edge("cannot_answer", END)
workflow.add_edge("off_topic_response", END)
workflow.set_entry_point("question_rewriter")
graph = workflow.compile(checkpointer=checkpointer)
# input_data = {"question": HumanMessage(content="how to improve my skin?")}
# graph.invoke(input=input_data, config={"configurable": {"thread_id": 1}})
# from IPython.display import Image, display
# (Image(display(graph.get_graph().draw_ascii())))
