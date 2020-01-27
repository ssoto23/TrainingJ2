from zeppelin_plugin.operators.zeppelin_notebook_operator import ZeppelinNotebookOperator
from airflow.plugins_manager import AirflowPlugin


class ZeppelinPlugin(AirflowPlugin):
    # The name of your plugin (str)
    name = "zeppelin_plugin"
    # A list of class(es) derived from BaseOperator
    operators = [ZeppelinNotebookOperator]
    # Leave in for explicitness
    hooks = []
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []