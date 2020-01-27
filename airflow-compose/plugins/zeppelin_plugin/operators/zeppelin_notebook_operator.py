import http.client
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults


class ZeppelinNotebookOperator(BaseOperator):
    ui_color = '#0077b3'
    ui_fgcolor = '#ffffff'

    @apply_defaults
    def __init__(
            self,
            notebook_id: str,
            restart_interpreter: bool,
            interpreter_used: [],
            restart_before_start: bool = False,
            *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.notebook_id = notebook_id
        self.restart_interpreter = restart_interpreter
        self.interpreter_used = interpreter_used
        self.restart_before_start = restart_before_start

    def execute(self, context):
        if self.restart_before_start:
            self.restartInterpreters(http.client.HTTPConnection("zeppelin:8080"), self.interpreter_used)
        print("posting to zeppelin")
        url = "/api/notebook/job/%s" % (self.notebook_id,)
        print(url)
        conn = http.client.HTTPConnection("zeppelin:8080")
        conn.request("POST", url)
        res = conn.getresponse()
        conn.close()
        if self.restart_interpreter:
            self.restartInterpreters(http.client.HTTPConnection("zeppelin:8080"), self.interpreter_used)
        print (res.status, res.reason)
        return res.status, res.reason

    def restartInterpreters(self, conn, interpreters):
        for intr in interpreters:
            print("/api/interpreter/setting/restart/%s" % (intr,))
            conn.request("PUT", "/api/interpreter/setting/restart/%s" % (intr,))
            res = conn.getresponse()
            print (res.status, res.reason)
            conn.close()
