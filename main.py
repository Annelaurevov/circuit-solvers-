from code.IO.AlgorithmRunner import AlgorithmRunner
from code.IO.parse_command_line import parse_command_line


if __name__ == "__main__":
    runner = AlgorithmRunner(*parse_command_line())
    runner.run()

