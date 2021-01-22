from typing import List, Callable
import re
import signal


def handler(signum: int, frame):
    raise Exception("End of time")

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
        self.pattern = re.compile(self.symbolic_expression)
        signal.signal(signal.SIGALRM, self.run)
        
    def run(self):
        outputs = []
        for exemplar in self.exemplars["train"]["inputs"]:
            signal.alarm(1)
            result = self.pattern.match(exemplar)
            if result is None:
                result = 0
            else:
                result = 1
            outputs.append(result)

        return outputs
