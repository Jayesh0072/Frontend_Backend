from langchain import PromptTemplate
from jinja2 import Template



CHAIN_TEMPLATE = '''
A user has uploaded {num_files} files that they want to ask questions to. They are named: {filenames}. 
Please turn the following user prompt into the appropriate questions for each file in the format of: 
"{{"<filename1>": "<question>", "<filename2>": "<question>",...}} "

If the prompt should only result in a question for one of the files just return one file and question in your reply, don't feel the need to return back questions for all files, i.e. it is ok to return back: "{{"<filename1">: "<question>"}}". if the prompt isn't clear about which files to ask, just return the same question to be asked to both files. 

In some cases, the question for a given file may depend on the answer to a question to another file. For example, 
if the user asked: "Does the format of <filename2> match the format defined in <filename1>",  then we know the 
question to <filename2> depends on the answer to the question for <filename1>. If any of these dependencies exist, 
add a separate key in the json that you return back called "dependencies" where the key is the name of the file that 
has dependencies (in this case "<filename1>". And the value is a comma separated list of files it depends on (in this 
case ["<filename2>"]. 

Make sure to return the response in the format laid out above (json representation of a dictionary where the key is the filename and the value is the question, and an optional key called "dependencies").

DO NOT include a reference to the file in the question that you return. 
For example: 
Instead of "What is the definition of risk according to <filename>?" 
You should instead return: "What is the definition of risk"?

This is the user prompt:

{question}
'''

CHAIN_PROMPT = PromptTemplate(
    input_variables=["num_files", "filenames", "question"],
    template=CHAIN_TEMPLATE,
)


DEPENDENCY_TEMPLATE = """
A user has uploaded {num_files} that they want to ask questions to. They are named: {filenames}. 

In some cases the question they are asking requires first getting the result from one file, and then asking a question to the second file based on the results of the first file.
We call these dependencies.  
For example, if the user asked: "Does the format of <filename2> match the format defined in <filename1>",  then we know the question to <filename2> depends on the answer to the question for <filename1>. 
In some cases, a file may have multiple dependencies on other files.

In this example, the response format should be:

{{"dependencies": {{"<filename2>": ["<filename1>"]}}}}
If <filename1> also depended on the response to <filename2>, then the response should look like:

{{"dependencies": {{"<filename2>": ["<filename1>"], "<filename1>": ["<filename2>"]}}}}

If the user had mentioned three files (<filename1>, <filename2>, <filename3>). 
And we saw that the question to <filename3> depended on the answers to <filename1> and <filename2>, the response would look like:

{{"dependencies": {{"<filename3>": ["<filename1>", "<filename2>"]}}}}
If there are NO dependencies simply return:
{{"dependencies": {{}}}}

There should never be any files with mutual dependencies (i.e. they both depends on each other). If you do find that to be the case, pick just one to be the dependency.

Make sure that your response includes no other text other than the serialized json string.

This is the user question:

{question}
"""

DEPENDENCY_PROMPT = PromptTemplate(
    input_variables=["num_files", "filenames", "question"],
    template=DEPENDENCY_TEMPLATE,
)


QUESTION_WITH_DEPS_JINJA_PROMPT = """
A user has uploaded {{ num_files }} files that they want to ask questions to. They are named: {{ filenames }}. 
The question that the user is asking to {{ question_file }} depends on the answer(s) to the question(s) they asked to {{ dependency_filenames }}.

{% for dep in dependencies %}
Here is the question they asked to {{ dep.filename }}:
{{ dep.question }}

And here is the response from {{ dep.filename }}:
{{ dep.response }}
{% endfor %}

Here is the question the user wants to ask {{ question_file }}:

{{ question_to_ask }}

Given the above response(s) from {{ dependency_filenames }}, can you rewrite the question to {{ question_file }} to include the proper context from the responses?
The question you return should not reference any filenames, but instead include all the necessary context in the question itself.
"""

QUESTION_WITH_DEPS_JINJA_TEMPLATE = Template(QUESTION_WITH_DEPS_JINJA_PROMPT)


FINAL_QUESTION_JINJA_PROMPT = """
A user has uploaded {{ num_files }} files that they want to ask questions to. They are named: {{ filenames }}.
The user now wants to ask this question: 
{{ user_question }}

Based on that question, we first gathered info from all of the related uploaded files by asking contextual questions.
Here are the questions and responses we got from the relevant files:

{% for info in context %}
Here is the question that was asked to {{ info.filename }}:
{{ info.question }}

And here was the response from {{ info.filename }}:
{{ info.response }}
{% endfor %}

Given the user's question above and the relevant context provided, can you please respond with an appropriate answer to the user's question (and make sure to include relevant information from the context in your response)?
"""

FINAL_QUESTION_JINJA_TEMPLATE = Template(FINAL_QUESTION_JINJA_PROMPT)
