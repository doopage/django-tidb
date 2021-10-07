from django.db.backends.mysql.schema import (
    DatabaseSchemaEditor as MysqlDatabaseSchemaEditor,
)
import re


class DatabaseSchemaEditor(MysqlDatabaseSchemaEditor):
    @property
    def sql_delete_check(self):
        return 'ALTER TABLE %(table)s DROP CHECK %(name)s'

    @property
    def sql_rename_column(self):
        return 'ALTER TABLE %(table)s CHANGE %(old_column)s %(new_column)s %(type)s'

    def skip_default_on_alter(self, field):
        return False

    @property
    def _supports_limited_data_type_defaults(self):
        return True

    def _field_should_be_indexed(self, model, field):
        return False

    def execute(self, sql, params=()):
        # TiDB does not support adding new column with UNIQUE,
        # it will throw django.db.utils.OperationalError:
        # (8200, "unsupported add column 'col' constraint UNIQUE KEY when altering 'table'").
        # So split it into 2 sql, one adds a new column and the other add unique constraint
        if re.match(r"ALTER TABLE .* ADD COLUMN .* UNIQUE.*", sql):
            sql = re.sub(r'(^ALTER TABLE (.*) ADD COLUMN (.*?) .*) UNIQUE(.*)',
                         r'\1; ALTER TABLE \2 ADD CONSTRAINT \3 UNIQUE (\3)',
                         sql) # remove UNIQUE keyword

        super().execute(sql, params)