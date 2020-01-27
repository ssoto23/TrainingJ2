from enum import Enum

class Notebooks(Enum):
    KafkaReader = '2EXBGWKU1'
    ExportToSchema = '2EXQEGYMG'
    PrepareFilesToLoad = '2EXQP4H7Q'
    PrepareRedshiftDb = '2EXW4GMRD'
    RedshiftLoadFiles = '2EXSBN97B'
    SetUpClusterDeps = '2EZ5YG7UK'

class Interpreters(Enum):
    SPARK = 'spark'
    REDSHIFT = 'redshift'
    POSTGRES = 'jdbc'
