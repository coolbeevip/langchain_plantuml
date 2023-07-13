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
        callback_handler = diagram.activity_diagram_callback()
        question = "What did biden say about ketanji brown jackson in the state of the union address?"
        try:
            self._agent.run(question=question, callbacks=[callback_handler])
        finally:
            plantuml_content = callback_handler.export_uml_content()
            with open("scene_agent-activity-diagram.puml", "w") as f:
                for line in plantuml_content:
                    f.write(str(line) + "\n")


if __name__ == '__main__':
    unittest.main()
