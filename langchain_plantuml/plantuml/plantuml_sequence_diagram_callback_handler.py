# Copyright 2023 Lei Zhang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
from typing import Any, Dict, List, Optional, Union

from langchain.schema import AgentAction, AgentFinish, LLMResult

from langchain_plantuml.core.plantuml_callback_handler import \
    BasePlantUMLCallbackHandler

DEFAULT_SKIN_PARAM = [
    "skinparam maxMessageSize 50",
    "skinparam roundcorner 20",
    "skinparam sequenceArrowThickness 2",
    "skinparam ParticipantPadding 20",
]

UML_PARTICIPANTS_FLAG = "-participants-"


class PlantUMLSequenceDiagramCallbackHandler(BasePlantUMLCallbackHandler):
    _runs_metrics: dict = {}

    def __init__(
        self,
        color: Optional[str] = None,
        skin_param: List[str] = DEFAULT_SKIN_PARAM,
        note_max_length: int = 1000,
        note_wrap_width: int = 500,
    ) -> None:
        super().__init__(
            note_max_length=note_max_length, note_wrap_width=note_wrap_width
        )
        for param in skin_param:
            self.uml_content.append(param)
        self.uml_content.append(UML_PARTICIPANTS_FLAG)
        self.participants = {}
        self.participant_name_indexes = []
        self.color = color

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        run_metric = self._get_run_object(serialized=serialized, **kwargs)
        activity_name = self._wrapper_sequence_name(
            self.on_llm_start.__name__,
            run_metric["parent_run_name"],
            run_metric["name"],
        )
        self._append_uml_sequence(
            line=activity_name,
            activate=True,
            participant=run_metric["name"],
            color="#A9DCDF",
        )
        self._append_uml_notes(
            align="left", color="#A9DCDF", notes=self._wrapper_note(prompts[0])
        )

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        run_metric = self._get_run_object(**kwargs)
        time_cost = run_metric["end_time"] - run_metric["begin_time"]
        self.prompt_tokens += response.llm_output["token_usage"].prompt_tokens
        self.completion_tokens += response.llm_output["token_usage"].completion_tokens
        self.total_tokens += response.llm_output["token_usage"].total_tokens
        activity_name = self._wrapper_sequence_name(
            method_name=self.on_llm_end.__name__,
            parent_run_name=run_metric["name"],
            run_name=run_metric["parent_run_name"],
            message=f"Time cost: {time_cost:.2f}s",
        )
        self._append_uml_sequence(
            line=activity_name, activate=False, participant=run_metric["name"]
        )
        for chats in response.generations:
            for chat in chats:
                self._append_uml_notes(
                    align="right", color="#A9DCDF", notes=self._wrapper_note(chat.text)
                )

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        run_metric = self._get_run_object(**kwargs)
        activity_name = self._wrapper_sequence_name(
            self.on_llm_new_token.__name__,
            run_metric["name"],
            run_metric["parent_run_name"],
        )
        self._append_uml_sequence(
            line=activity_name, activate=True, participant=run_metric["name"]
        )
        self._append_uml_notes(
            align="right", color="#FEFECE", notes=self._wrapper_note(token)
        )

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        run_metric = self._get_run_object(**kwargs)
        activity_name = self._wrapper_sequence_name(
            self.on_llm_error.__name__,
            run_metric["name"],
            run_metric["parent_run_name"],
            "#red",
        )
        self._append_uml_sequence(
            line=activity_name, activate=False, participant=run_metric["name"]
        )
        self._append_uml_notes(
            align="right", color="#red", notes=self._wrapper_note(str(error))
        )

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        run_metric = self._get_run_object(serialized, **kwargs)
        activity_name = self._wrapper_sequence_name(
            self.on_chain_start.__name__,
            run_metric["parent_run_name"],
            run_metric["name"],
        )
        self._append_uml_sequence(
            line=activity_name, activate=True, participant=run_metric["name"]
        )
        self._append_uml_notes(
            align="left", color="#FEFECE", notes=self._wrapper_note(str(inputs))
        )

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        run_metric = self._get_run_object(**kwargs)
        activity_name = self._wrapper_sequence_name(
            self.on_chain_end.__name__,
            run_metric["name"],
            run_metric["parent_run_name"],
        )
        self._append_uml_sequence(
            line=activity_name, activate=False, participant=run_metric["name"]
        )
        self._append_uml_notes(
            align="right", color="#A9DCDF", notes=self._wrapper_note(str(outputs))
        )

    def on_chain_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        run_metric = self._get_run_object(**kwargs)
        activity_name = self._wrapper_sequence_name(
            self.on_chain_error.__name__,
            run_metric["name"],
            run_metric["parent_run_name"],
            "#red",
        )
        self._append_uml_sequence(
            line=activity_name, activate=False, participant=run_metric["name"]
        )
        self._append_uml_notes(
            align="right", color="#red", notes=self._wrapper_note(str(error))
        )

    def on_agent_action(
        self, action: AgentAction, color: Optional[str] = None, **kwargs: Any
    ) -> Any:
        run_metric = self._get_run_object(**kwargs)
        if "parent_run_name" in run_metric:
            activity_name = self._wrapper_sequence_name(
                self.on_agent_action.__name__,
                run_metric["parent_run_name"],
                run_metric["name"],
            )
            self._append_uml_sequence(
                line=activity_name, activate=True, participant=run_metric["name"]
            )

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs: Any,
    ) -> None:
        pass
        run_metric = self._get_run_object(serialized, **kwargs)
        activity_name = self._wrapper_sequence_name(
            self.on_tool_start.__name__,
            run_metric["parent_run_name"],
            run_metric["name"],
        )
        self._append_uml_sequence(
            line=activity_name,
            activate=True,
            participant=run_metric["name"],
            color="#orange",
        )
        self._append_uml_notes(
            align="left", color="#FEFECE", notes=self._wrapper_note(input_str)
        )

    def on_tool_end(
        self,
        output: str,
        color: Optional[str] = None,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        run_metric = self._get_run_object(**kwargs)
        activity_name = self._wrapper_sequence_name(
            self.on_tool_end.__name__, run_metric["name"], run_metric["parent_run_name"]
        )
        self._append_uml_sequence(
            line=activity_name, activate=False, participant=run_metric["name"]
        )
        self._append_uml_notes(
            align="right", color="#A9DCDF", notes=self._wrapper_note(output)
        )

    def on_tool_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        run_metric = self._get_run_object(**kwargs)
        activity_name = self._wrapper_sequence_name(
            self.on_tool_end.__name__,
            run_metric["name"],
            run_metric["parent_run_name"],
            "#red",
        )
        self._append_uml_sequence(
            line=activity_name, activate=False, participant=run_metric["name"]
        )
        self._append_uml_notes(
            align="right", color="#red", notes=self._wrapper_note(str(error))
        )

    def on_text(
        self,
        text: Any,
        color: Optional[str] = None,
        end: str = "",
        **kwargs: Any,
    ) -> None:
        run_metric = self._get_run_object(**kwargs)
        if type(text) == list:
            activity_name = self._wrapper_sequence_name(
                self.on_text.__name__, run_metric["parent_run_name"], run_metric["name"]
            )
            self._append_uml_sequence(activity_name)
            self._append_uml_notes(
                align="left",
                color="#FEFECE",
                notes=[
                    f"Step{index}.{step.value}\n" for index, step in enumerate(text)
                ],
            )

    def on_agent_finish(
        self, finish: AgentFinish, color: Optional[str] = None, **kwargs: Any
    ) -> None:
        run_metric = self._get_run_object(**kwargs)
        activity_name = self._wrapper_sequence_name(
            self.on_agent_finish.__name__,
            run_metric["name"],
            run_metric["parent_run_name"],
        )
        self._append_uml_sequence(
            line=activity_name, activate=False, participant=run_metric["name"]
        )

    def export_uml_content(self) -> List[str]:
        new_uml_content = []
        for line in self.uml_content:
            if line == UML_PARTICIPANTS_FLAG:
                for participant_name in self.participant_name_indexes:
                    new_uml_content.append(self.participants[participant_name])
            else:
                new_uml_content.append(line)

        new_uml_content.append("note left")
        new_uml_content.append(
            f"* prompt_tokens: {self.prompt_tokens} \n"
            f"* completion_tokens: {self.completion_tokens} \n"
            f"* total_tokens: {self.total_tokens}"
        )
        new_uml_content.append("end note")
        new_uml_content.append("@enduml")
        return new_uml_content

    def _get_run_object(self, serialized: Dict[str, Any] = None, **kwargs: Any) -> Dict:
        run_id = str(kwargs["run_id"])
        if run_id not in self._runs_metrics:
            self._runs_metrics[run_id] = {}

        if "begin_time" not in self._runs_metrics[run_id]:
            self._runs_metrics[run_id]["begin_time"] = time.time()
        else:
            self._runs_metrics[run_id]["end_time"] = time.time()

        if kwargs["parent_run_id"] is not None:
            parent_run_id = str(kwargs["parent_run_id"])
            self._runs_metrics[run_id]["parent_run_id"] = parent_run_id
            self._runs_metrics[run_id]["parent_run_name"] = self._runs_metrics[
                parent_run_id
            ]["name"]

        if serialized is not None:
            run_name = (
                serialized.get("name")
                if serialized.get("name") is not None
                else serialized["id"][len(serialized["id"]) - 1]
            )
            self._runs_metrics[run_id]["name"] = run_name.replace(" ", "_")

        return self._runs_metrics[run_id]

    def _append_uml_sequence(
        self,
        line,
        activate: bool = False,
        participant: str = None,
        color: str = "#FEFECE",
    ):
        self.uml_content.append(line)
        if activate:
            self.uml_content.append(f'activate "{participant}" {color}')
        else:
            self.uml_content.append(f'deactivate "{participant}"')
        self.step += 1

    def _append_uml_notes(
        self, align: str = "left", notes: List[str] = [], color: str = ""
    ):
        if len(notes) > 0:
            self._append_uml_line(f"note {align} {color}")
            self._append_uml_multi_line(notes)
            self._append_uml_line("end note")

    def _wrapper_sequence_name(
        self,
        method_name: str,
        parent_run_name: str,
        run_name: str,
        color: str = None,
        message: str = "",
    ) -> str:
        if parent_run_name not in self.participants:
            self.participants[
                parent_run_name
            ] = f'participant "{self.emojis[method_name] if method_name in self.emojis else ""} {parent_run_name}" as {parent_run_name}'
            self.participant_name_indexes += [parent_run_name]

        if run_name not in self.participants:
            self.participants[
                run_name
            ] = f'participant "{self.emojis[method_name] if method_name in self.emojis else ""} {run_name}" as {run_name}'
            self.participant_name_indexes += [run_name]

        return f'"{parent_run_name}" -{[color] if color is not None else ""}-> "{run_name}": {self.step} {message}'
