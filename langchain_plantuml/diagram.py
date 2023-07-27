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

from langchain.callbacks.base import BaseCallbackHandler

from langchain_plantuml.plantuml.plantuml_activity_diagram_beta_callback_handler import \
    PlantUMLActivityDiagramCallbackHandler
from langchain_plantuml.plantuml.plantuml_sequence_diagram_callback_handler import \
    PlantUMLSequenceDiagramCallbackHandler


def activity_diagram_callback(
    note_max_length: int = 1000, note_wrap_width: int = 500
) -> BaseCallbackHandler:
    return PlantUMLActivityDiagramCallbackHandler(
        note_max_length=note_max_length, note_wrap_width=note_wrap_width
    )


def sequence_diagram_callback(
    note_max_length: int = 1000, note_wrap_width: int = 500
) -> BaseCallbackHandler:
    return PlantUMLSequenceDiagramCallbackHandler(
        note_max_length=note_max_length, note_wrap_width=note_wrap_width
    )
