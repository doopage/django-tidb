import uuid

from django.conf import settings
from django.db.backends.base.operations import BaseDatabaseOperations
from django.utils import timezone
from django.utils.encoding import force_str
from django.db.backends.mysql.operations import (
    DatabaseOperations as MysqlDatabaseOperations,
)

class DatabaseOperations(MysqlDatabaseOperations):
    def explain_query_prefix(self, format=None, **options):
        analyze = options.pop('analyze', False)
        prefix = self.explain_prefix
        if analyze and self.connection.features.supports_explain_analyze:
            prefix += ' ANALYZE'
        if format and not analyze:
            # Only TiDB supports the analyze option with formats but with "ROW".
            prefix += ' FORMAT=\"%s\"' % format
        return prefix

    def regex_lookup(self, lookup_type):
        # REGEXP BINARY doesn't work correctly in MySQL 8+ and REGEXP_LIKE
        # doesn't exist in MySQL 5.x or in MariaDB.
        if lookup_type == 'regex':
            return '%s REGEXP BINARY %s'
        return '%s REGEXP %s'

    def lookup_cast(self, lookup_type, internal_type=None):
        lookup = '%s'
        if internal_type == 'JSONField':
            lookup = 'JSON_UNQUOTE(%s)'
        return lookup
