import subprocess
from os import path


def execute_commands(commands):
    outputs = list(map(execute_command, commands))
    return outputs


def execute_command(command):
    filepath = path.abspath(path.join(path.dirname(__file__), "..", "..", "prom", "ProM_CLI.sh"))
    output = subprocess.run(['sh', filepath, command], capture_output=True, text=True)
    return {"args": output.args, "stdout": output.stdout.split("\n"), "stderr": output.stderr.split("\n"),
            "returnCode": output.returncode}
