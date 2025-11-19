
from chain import Chain 

from typing import NamedTuple
from PIL import Image
from chatbot import ChatBot


USER = "user"
ASSISTANT = "assistant"


class ChatResponse(NamedTuple):
    content: str
    llm_history: list  


def _get_runner(files):
    return chatbot_runner

 


def chatbot_runner(query, files, llm_history):
    chain = Chain(fileNm=files)
    chain.add_history(llm_history)
    response = chain.ask(query)
    llm_history.append((query, response))

    return ChatResponse(content=response, llm_history=llm_history)

def run_1(filePath,query): 
    files =filePath #"occ.pdf"#st.file_uploader("Upload your documents", type=["pdf", "csv"], accept_multiple_files=True)
    print('files ')
    print(files)

    if files:
        print('inside if')
        runner = _get_runner(files)

         

        chat_response = runner(query, files, [])
        print(chat_response.content)
        return chat_response.content

