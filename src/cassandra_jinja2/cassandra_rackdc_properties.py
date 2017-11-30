import logging

import cassandra_jinja2.base_config

logger = logging.getLogger(__name__)


class CassandraRackDcProperties(cassandra_jinja2.base_config.BaseConfig):
    """
    Class to parse a cassandra-rackdc.properties file and generate a Jinja2 template.

    Methods implemented in this class use regular expressions to match options in the jvm.options file.  Care must be
    taken to escape regular expression metacharacters: . ^ $ * + ? { } [ ] \ | ( )
    See: https://docs.python.org/3/howto/regex.html#matching-characters
    """

    def __init__(self, cassandra_version):
        super().__init__(cassandra_version)

    def generate_template(self):
        self.dc()
        self.rack()

    def dc(self):
        """
        dc=dc1
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(dc=)(.*)\n',
            jinja_variable='cassandra_rackdc_properties.dc')

    def rack(self):
        """
        rack=rack1
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(rack=)(.*)\n',
            jinja_variable='cassandra_rackdc_properties.rack')
