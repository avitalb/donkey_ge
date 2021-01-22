from typing import List, Callable
import re


class Regex:
    """
    Evaluate a regex

    Attributes:
        exemplars
        symbolic_expression
    """

    def __init__(
        self, exemplars, symbolic_expression):
        self.exemplars = exemplars
        self.symbolic_expression = symbolic_expression

    def run(self):
        pattern = re.compile(self.symbolic_expression)
        outputs = []
        for exemplar in self.exemplars["train"]["inputs"]:
            result = pattern.match(exemplar)
            if result is None:
                result = 0
            outputs.append(result)

        return outputs
