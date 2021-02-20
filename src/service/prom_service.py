from src.cli.prom_cli import execute_prom_cli


def execute_commands(commands):
    outputs = list(map(execute_command, commands))
    return outputs


def execute_command(command):
    return execute_prom_cli("ProM_CLI.sh", command)
