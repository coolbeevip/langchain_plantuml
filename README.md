# LangChain PlantUML CallBack Handler

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

## Exporting PlantUML to PNG

You can download [plantuml.1.2023.10.jar](https://github.com/plantuml/plantuml/releases/download/v1.2023.10/plantuml-1.2023.10.jar)

```shell
java -DPLANTUML_LIMIT_SIZE=81920 -jar plantuml-1.2023.10.jar scene_agent.puml
```