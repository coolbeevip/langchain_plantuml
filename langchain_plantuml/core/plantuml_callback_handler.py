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

from abc import ABC, abstractmethod
from typing import List

from langchain.callbacks.base import BaseCallbackHandler


class BasePlantUMLCallbackHandler(BaseCallbackHandler, ABC):
    crlf: str = "⏎"
    note_max_length: int = 1000
    note_wrap_width: int = 500
    emojis = {
        "on_llm_start": "<:1f916:>",
        "on_llm_end": "<:1f916:>",
        "on_chain_start": "<:1f3af:>",
        "on_chain_end": "<:1f3af:>",
        "on_tool_start": "<:1f528:>",
        "on_tool_end": "<:1f528:>",
        "on_text": "<:1f4c6:>",
    }

    def __init__(self, note_max_length: int = 1000, note_wrap_width: int = 500):
        self.note_wrap_width = note_wrap_width
        self.note_max_length = note_max_length
        self.step = 0
        self.total_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.uml_content = []
        self.uml_content.append("@startuml")
        self.uml_content.append("skinparam dpi 300")
        self.uml_content.append(f"skinparam wrapWidth {self.note_wrap_width}")
        self.uml_content.append("skinparam shadowing false")
        self.uml_content.append("skinparam noteFontName Arial")
        self.uml_content.append("skinparam noteFontSize 10")
        self.uml_content.append("skinparam noteBackgroundColor #ECECEC")
        self.uml_content.append("skinparam noteBorderColor #C0C0C0")
        self.uml_content.append("skinparam noteFontColor #333333")
        self.uml_content.append("skinparam noteBorderThickness 0")
        self.uml_content.append("skinparam noteShadowing false")
        self.uml_content.append("skinparam noteArrow none")

    @abstractmethod
    def export_uml_content(self) -> List[str]:
        pass

    def save_uml_content(self, file_path: str):
        with open(file_path, "w") as f:
            for line in self.export_uml_content():
                f.write(str(line) + "\n")

    def _append_uml_line(self, line):
        self.uml_content.append(line)

    def _append_uml_multi_line(self, lines: List[str]):
        for line in lines:
            self.uml_content.append(line)

    def _wrapper_note(self, note: str) -> List[str]:
        new_note = note.strip()
        if len(new_note) > self.note_max_length:
            new_note = f"{new_note[:self.note_max_length]} ... (Omit {len(new_note) - self.note_max_length} words)"

        new_notes = [f"{line}{self.crlf}" for line in new_note.split("\n")]

        wrap_notes = [
            word
            for phrase in new_notes
            for word in (
                [
                    phrase[i : i + self.note_wrap_width]
                    for i in range(0, len(phrase), self.note_wrap_width)
                ]
                if len(phrase) > self.note_wrap_width
                else [phrase]
            )
        ]
        return wrap_notes
