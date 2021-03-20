from src.cli.prom_cli import execute_prom_cli


def list_packages():
    return execute_command("list")


def list_packages_json():
    response = list_packages()
    stdouts = response["stdout"]
    packages = list()
    for response in stdouts:
        response_parts = list(filter(lambda x: x != "", response.split(" ")))
        # TODO: Sera que pega todos?
        if response_parts.__len__() == 3 and (response_parts[0] == "A" or response_parts[0] == "I"):
            package = {"status": response_parts[0], "name": response_parts[1], "version": response_parts[2]}
            packages.append(package)
    return packages


def update_packages():
    return execute_command("update")


def install_packages(packages):
    [execute_command(f"change +{package}") for package in packages]


def remove_packages(packages):
    [execute_command(f"change x{package}") for package in packages]


def install_all_packages():
    packages = list_packages_json()
    packages_names = [package["name"] for package in packages]
    install_packages(packages_names)
    return list_packages_json()


def execute_command(command):
    return execute_prom_cli("ProM_PM_CLI.sh", command)
