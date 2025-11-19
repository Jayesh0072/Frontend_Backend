from chatbot import ChatBot
from file import File
from langchain import OpenAI, LLMChain
from templates import CHAIN_PROMPT, DEPENDENCY_PROMPT, QUESTION_WITH_DEPS_JINJA_TEMPLATE, FINAL_QUESTION_JINJA_TEMPLATE
from collections import defaultdict
import json
from langchain import PromptTemplate
from utils import extract_json_from_string


class ChainGraph:
    def __init__(self, filenames, dependencies=None):
        self.filenames: list[str] = filenames
        self.dependencies: dict[str, list[str]] = dependencies if dependencies is not None else {}
        self.stages: dict[int, list[str]] = defaultdict(list)
        self._calculate_stages()

    def _calculate_stages(self):
        filename_to_stage = {}
        i = 0
        while i < len(self.filenames):
            found_all = True
            for filename in self.filenames:
                if filename in filename_to_stage:
                    continue

                stage = self._calculate_stage(filename, filename_to_stage)
                if stage < 0:
                    found_all = False
                    continue

                filename_to_stage[filename] = stage
                self.stages[stage].append(filename)
            if found_all:
                break
            i += 1

    def _calculate_stage(self, filename: str, filename_to_stage):
        if filename not in self.dependencies:
            return 0

        deps = self.dependencies.get(filename)
        max_stage = -1
        for dep in deps:
            if dep not in filename_to_stage:
                return -1
            max_stage = max(max_stage, filename_to_stage[dep])
        return max_stage + 1

    def get_stages(self):
        i = 0
        while len(self.stages[i]) > 0:
            yield self.stages[i]
            i += 1


class Chain:
    def __init__(self,fileNm:str=None, files= None,):
        self.is_multifile =False# len(files) > 1
        # self.files: list[File] = [File(content=f, type=f.type.split("/")[1], name=f.name) for f in files]
        # self.bots: dict[str, ChatBot] = {f.name: ChatBot(file=f) for f in self.files}
        self.bot:  ChatBot =  ChatBot(filename=fileNm)  
        self.question_generator_llm = LLMChain(llm=OpenAI(), prompt=CHAIN_PROMPT)
        self.dependency_llm = LLMChain(llm=OpenAI(), prompt=DEPENDENCY_PROMPT)

    def ask(self, question):
        if self.is_multifile:
            return self._ask_multifile(question)         
        return self.bot.ask(question)

    def _ask_multifile(self, question):
        question_response = self.question_generator_llm(inputs={
            "num_files": len(self.files),
            "filenames": ", ".join(self.bots.keys()),
            "question": question})

        files_to_questions = extract_json_from_string(question_response["text"])
        files_to_questions = {k: v for k, v in files_to_questions.items() if k in self.bots}

        dep_response = self.dependency_llm(inputs={
            "num_files": len(self.files),
            "filenames": ", ".join(self.bots.keys()),
            "question": question})

        dependencies = extract_json_from_string(dep_response["text"]).get("dependencies")

        chain_graph = ChainGraph(files_to_questions.keys(), dependencies)
        for stage in chain_graph.get_stages():
            for filename in stage:
                question = files_to_questions.get(filename)
                dependency_filenames = dependencies.get(filename, None)
                dependency_question = self._get_question_with_dependencies(
                    question_to_ask=question,
                    question_file=filename,
                    dependency_filenames=dependency_filenames
                )
                chatbot = self.bots.get(filename)
                chatbot.ask(dependency_question)

        response = self._get_final_response(question, files_to_questions.keys())
        return response

    def _get_question_with_dependencies(self, question_to_ask="", question_file="", dependency_filenames=None):
        if not dependency_filenames:
            return question_to_ask

        dependencies = []
        for filename in dependency_filenames:
            chatbot = self.bots.get(filename)
            dependencies.append({
                "filename": filename,
                "question": chatbot.get_last_question(),
                "response": chatbot.get_last_response()
            })

        prompt = QUESTION_WITH_DEPS_JINJA_TEMPLATE.render(
            num_files=len(self.files),
            filenames=", ".join(self.bots.keys()),
            dependency_filenames=", ".join(dependency_filenames),
            dependencies=dependencies,
            question_file=question_file,
            question_to_ask=question_to_ask
        )
        final_question = LLMChain(llm=OpenAI(), prompt=PromptTemplate(template=prompt, input_variables=[]))(inputs={})["text"]
        return final_question

    def _get_final_response(self, user_question, contextual_filenames):
        context = []
        for filename in contextual_filenames:
            chatbot = self.bots.get(filename)
            context.append({
                "filename": filename,
                "question": chatbot.get_last_question(),
                "response": chatbot.get_last_response(),
            })
        prompt = FINAL_QUESTION_JINJA_TEMPLATE.render(
            user_question=user_question,
            context=context,
            num_files=len(self.files),
            filenames=", ".join(self.bots.keys()),
        )
        return LLMChain(llm=OpenAI(), prompt=PromptTemplate(template=prompt, input_variables=[]))(inputs={})["text"]

    def add_history(self, history):
        pass
        # [bot.add_history(history) for _, bot in self.bots.items()]





