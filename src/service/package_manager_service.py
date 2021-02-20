from src.cli.prom_cli import execute_prom_cli


def list_packages():
    return execute_command("list")


def update_packages():
    return execute_command("update")


def install_packages(packages):
    [execute_command(f"change +{package}") for package in packages]


def remove_packages(packages):
    [execute_command(f"change x{package}") for package in packages]


def execute_command(command):
    return execute_prom_cli("ProM_PM_CLI.sh", command)
