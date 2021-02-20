from os import path


def get_template_plugin(plugin_name):
    file = open(get_template_plugin_path(plugin_name), mode="r")
    return file.read()


def get_template_plugin_path(plugin_name):
    return path.abspath(path.join(path.dirname(__file__), "..", "..", "template_plugin", f"{plugin_name}.txt"))
