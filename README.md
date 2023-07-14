# LangChain PlantUML Callback Handler

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPi version](https://img.shields.io/pypi/v/langchain-plantuml.svg)](https://pypi.org/project/langchain-plantuml/)
[![lint](https://github.com/coolbeevip/langchain_plantumlactions/workflows/lint.yml/badge.svg)](https://github.com/coolbeevip/langchain_plantuml/actions/workflows/lint.yml)
[![Build status](https://github.com/coolbeevip/langchain_plantuml/actions/workflows/release.yml/badge.svg)](https://github.com/coolbeevip/langchain_plantuml/actions)
[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![](https://img.shields.io/pypi/dm/langchain-plantuml)](https://pypi.org/project/langchain-plantuml/)

Subscribe to events using a callback and store them in PlantUML format. You can easily subscribe to events and keep them in a form that is easy to visualize and analyze.

![](screenshot/scene_agent.png)

## Quick Start

Install this library:

```shell
pip install langchain-plantuml
```

Then:

1. Add import langchain_plantuml as the first import in your Python entrypoint file
2. Create a callback using the activity_diagram_callback function
3. Hook into your LLM application
4. Call the export_uml_content method of activity_diagram_callback to export the PlantUML content
5. Save PlantUML content to a file
6. Exporting PlantUML to PNG

Running the minimal example.

```python
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory

from langchain_plantuml import diagram

template = """You are a chatbot having a conversation with a human.

{chat_history}
Human: {human_input}
Chatbot:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"], template=template
)
memory = ConversationBufferMemory(memory_key="chat_history")

callback_handler = diagram.activity_diagram_callback()

llm_chain = LLMChain(
    llm=OpenAI(),
    prompt=prompt,
    verbose=True,
    memory=memory,
    callbacks=[callback_handler]
)

llm_chain.predict(human_input="Hi there my friend")
llm_chain.predict(human_input="Not too bad - how are you?")

plantuml_content = callback_handler.export_uml_content()
with open("example.puml", "w") as f:
    for line in plantuml_content:
        f.write(str(line) + "\n")
```

You will get the following PlantUML activity diagram

![](screenshot/example.png)

## Exporting PlantUML to PNG

You can download [plantuml.1.2023.10.jar](https://github.com/plantuml/plantuml/releases/download/v1.2023.10/plantuml-1.2023.10.jar)

```shell
java -DPLANTUML_LIMIT_SIZE=81920 -jar plantuml-1.2023.10.jar example.puml
```

