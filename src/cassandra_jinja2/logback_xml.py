import logging

import cassandra_jinja2.base_config

logger = logging.getLogger(__name__)


class LogbackXml(cassandra_jinja2.base_config.BaseConfig):
    """
    Class to parse a logback.xml file and generate a Jinja2 template.

    This class has been coded using regular expressions to be consistent with parsing of other Cassandra configuration
    files but could be coded using xml.etree.ElementTree or lxml.etree.ElementTree.  Regular expressions will be used
    unless there is a more compelling reason to use a Python module for parsing XML data.

    Methods implemented in this class use regular expressions to match options in the jvm.options file.  Care must be
    taken to escape regular expression metacharacters: . ^ $ * + ? { } [ ] \ | ( )
    See: https://docs.python.org/3/howto/regex.html#matching-characters
    """

    def __init__(self, cassandra_version):
        super().__init__(cassandra_version)

    def generate_template(self):
        self.systemlog_logdir()
        self.systemlog_rolling_logdir()
        self.systemlog_maxindex()
        self.debuglog_logdir()
        self.debuglog_rolling_logdir()
        self.debuglog_maxindex()

    def systemlog_logdir(self):
        """
        <file>${cassandra.logdir}/system.log</file>
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(\s*<file>)(.*)(/system.log</file>)\n',
            jinja_variable='logback_xml.systemlog_logdir')

    def systemlog_rolling_logdir(self):
        """
        <fileNamePattern>${cassandra.logdir}/system.log.%i.zip</fileNamePattern>
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(\s*<fileNamePattern>)(.*)(/system.log.%i.zip</fileNamePattern>)\n',
            jinja_variable='logback_xml.systemlog_rolling_logdir')

    def systemlog_maxindex(self):
        """
        In this method, the option_pattern specified is:
            r'^(\s*<appender name="SYSTEMLOG"(?:.*\n)+?\s*<maxIndex>)(\d+)(</maxIndex>)\n'
        A portion of the regular expression above denoted by (?:.*\n)+?\s* requires some explanation. First, (?:...)
        denotes a non-capturing version of regular parentheses. Thus, after matching "SYSTEMLOG", we match any number of
        characters, up and including a newline, one or more times, in a non-greedy fashion.  Then, preceding <maxIndex>
        we match any number of whitespace characters.  It is important to match in a non-greedy fashion, which matches 
        as little text as possible because if we didn't, the regex would match other text up until the last <maxIndex> 
        tag later in the logback.xml file which would not be the desired result.

        <appender name="SYSTEMLOG" ... <maxIndex>20</maxIndex>
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(\s*<appender name="SYSTEMLOG"(?:.*\n)+?\s*<maxIndex>)(\d+)(</maxIndex>)\n',
            jinja_variable='logback_xml.systemlog_maxindex')

    def debuglog_logdir(self):
        """
        <file>${cassandra.logdir}/debug.log</file>
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(\s*<file>)(.*)(/debug.log</file>)\n',
            jinja_variable='logback_xml.debuglog_logdir')

    def debuglog_rolling_logdir(self):
        """
         <fileNamePattern>${cassandra.logdir}/debug.log.%i.zip</fileNamePattern>
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(\s*<fileNamePattern>)(.*)(/debug.log.%i.zip</fileNamePattern>)\n',
            jinja_variable='logback_xml.debuglog_rolling_logdir')

    def debuglog_maxindex(self):
        """
        In this method, the option_pattern specified is:
            r'^(\s*<appender name="DEBUGLOG"(?:.*\n)+?\s*<maxIndex>)(\d+)(</maxIndex>)\n'
        A portion of the regular expression above denoted by (?:.*\n)+?\s* requires some explanation. First, (?:...)
        denotes a non-capturing version of regular parentheses. Thus, after matching "DEBUGLOG", we match any number of
        characters, up and including a newline, one or more times, in a non-greedy fashion.  Then, preceding <maxIndex>
        we match any number of whitespace characters.  It is important to match in a non-greedy fashion, which matches 
        as little text as possible because if we didn't, the regex would match other text up until the last <maxIndex> 
        tag later in the logback.xml file which would not be the desired result.

        <appender name="DEBUGLOG" ... <maxIndex>20</maxIndex>
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(\s*<appender name="DEBUGLOG"(?:.*\n)+?\s*<maxIndex>)(\d+)(</maxIndex>)\n',
            jinja_variable='logback_xml.debuglog_maxindex')
