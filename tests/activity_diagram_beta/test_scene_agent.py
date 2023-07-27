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

import unittest
from unittest import TestCase

import langchain

from langchain_plantuml import diagram
from tests.activity_diagram_beta.scene_agent import SceneAgent


class TestPlantUMLActivityDiagramCallbackHandler(TestCase):
    @classmethod
    def setUpClass(cls):
        langchain.debug = True
        cls._agent = SceneAgent()

    def test(self):
        activity_diagram_callback = diagram.activity_diagram_callback(note_max_length=2000, note_wrap_width=500)
        sequence_diagram_callback = diagram.sequence_diagram_callback(note_max_length=2000, note_wrap_width=500)
        question = "What did biden say about ketanji brown jackson in the state of the union address?"
        try:
            self._agent.run(question=question, callbacks=[activity_diagram_callback, sequence_diagram_callback])
        finally:
            activity_diagram_callback.save_uml_content("activity-plantuml.puml")
            sequence_diagram_callback.save_uml_content("sequence-plantuml.puml")


if __name__ == "__main__":
    unittest.main()
