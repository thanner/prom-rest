import subprocess
from os import path


def execute_prom_cli(script, command):
    filepath = path.abspath(path.join(path.dirname(__file__), "..", "..", "prom", "script", script))
    output = subprocess.run(['sh', filepath, command], capture_output=True, text=True)
    return {"args": output.args, "stdout": output.stdout.split("\n"), "stderr": output.stderr.split("\n"),
            "returnCode": output.returncode}
