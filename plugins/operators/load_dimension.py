from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'
    
    insert_sql = """
        INSERT INTO {}
        {}
        ;
    """

    @apply_defaults
    def __init__(self,
                redshift_conn_id="",
                table="",
                sql_query="",
                insert = True,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_query = sql_query
        self.insert = insert

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        if self.insert == False:
            self.log.info("Clearing data from destination Redshift table")
            redshift.run("DELETE FROM {}".format(self.table))

        formatted_sql = LoadDimensionOperator.insert_sql.format(
            self.table,
            self.sql_query
        )        
        
        self.log.info("Load dimension table")
        redshift.run(formatted_sql)