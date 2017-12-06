import logging
import re

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
        self.shutdown_hook()
        self.systemlog_logdir()
        self.systemlog_rolling_logdir()
        self.systemlog_maxindex()
        self.systemlog_maxfilesize()
        self.debuglog_logdir()
        self.debuglog_rolling_logdir()
        self.debuglog_maxindex()
        self.debuglog_maxfilesize()
        self.root_log_level()
        self.appender_systemlog_enabled()
        self.appender_stdout_enabled()
        self.appender_asyncdebuglog_enabled()
        self.cassandra_logger_level()
        self.thrift_logger_level()

    def shutdown_hook(self):
        """
        <!-- No shutdown hook; we run it ourselves in StorageService after shutdown -->
        :return:
        """
        option_pattern = r'^(\s*)(<!-- No shutdown hook; we run it ourselves in StorageService after shutdown -->)\n'
        jinja_variable = 'logback_xml.shutdown_hook'
        compiled_pattern = re.compile(option_pattern, re.MULTILINE)
        match = compiled_pattern.search(self.content)
        if match:
            replacement = '{%- if ' + jinja_variable + ' | default(false) %}\n'
            replacement += match.group(1) + '<shutdownHook class="{{ ' + jinja_variable + ' }}"/>\n'
            replacement += '{%- else %}\n'
            replacement += match.group(0)
            replacement += '{%- endif %}\n'
            self.content = compiled_pattern.sub(replacement, self.content)

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
            r'^(\s*<appender name="SYSTEMLOG"(?:.*\n)+?\s*<maxIndex>)(\w+)(</maxIndex>)\n'
        A portion of the regular expression above denoted by (?:.*\n)+?\s* requires some explanation. First, (?:...)
        denotes a non-capturing version of regular parentheses. Thus, after matching "SYSTEMLOG", we match any number of
        characters, up to and including a newline, one or more times, in a non-greedy fashion.  Then, preceding <maxIndex>
        we match any number of whitespace characters.  It is important to match in a non-greedy fashion, which matches
        as little text as possible because if we didn't, the regex would match other text up until the last <maxIndex>
        tag later in the logback.xml file which would not be the desired result.

        <appender name="SYSTEMLOG" ... <maxIndex>20</maxIndex>
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(\s*<appender name="SYSTEMLOG"(?:.*\n)+?\s*<maxIndex>)(\w+)(</maxIndex>)\n',
            jinja_variable='logback_xml.systemlog_maxindex')

    def systemlog_maxfilesize(self):
        """
        In this method, the option_pattern specified is:
            r'^(\s*<appender name="SYSTEMLOG"(?:.*\n)+?\s*<maxFileSize>)(\w+)(</maxFileSize>)\n'
        A portion of the regular expression above denoted by (?:.*\n)+?\s* requires some explanation. First, (?:...)
        denotes a non-capturing version of regular parentheses. Thus, after matching "SYSTEMLOG", we match any number of
        characters, up to and including a newline, one or more times, in a non-greedy fashion.  Then, preceding <maxFileSize>
        we match any number of whitespace characters.  It is important to match in a non-greedy fashion, which matches
        as little text as possible because if we didn't, the regex would match other text up until the last <maxFileSize>
        tag later in the logback.xml file which would not be the desired result.

        <appender name="SYSTEMLOG" ... <maxFileSize>20</maxFileSize>
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(\s*<appender name="SYSTEMLOG"(?:.*\n)+?\s*<maxFileSize>)(\w+)(</maxFileSize>)\n',
            jinja_variable='logback_xml.systemlog_maxfilesize')

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
            r'^(\s*<appender name="DEBUGLOG"(?:.*\n)+?\s*<maxIndex>)(\w+)(</maxIndex>)\n'
        A portion of the regular expression above denoted by (?:.*\n)+?\s* requires some explanation. First, (?:...)
        denotes a non-capturing version of regular parentheses. Thus, after matching "DEBUGLOG", we match any number of
        characters, up to and including a newline, one or more times, in a non-greedy fashion.  Then, preceding <maxIndex>
        we match any number of whitespace characters.  It is important to match in a non-greedy fashion, which matches
        as little text as possible because if we didn't, the regex would match other text up until the last <maxIndex>
        tag later in the logback.xml file which would not be the desired result.

        <appender name="DEBUGLOG" ... <maxIndex>20</maxIndex>
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(\s*<appender name="DEBUGLOG"(?:.*\n)+?\s*<maxIndex>)(\w+)(</maxIndex>)\n',
            jinja_variable='logback_xml.debuglog_maxindex')

    def debuglog_maxfilesize(self):
        """
        In this method, the option_pattern specified is:
            r'^(\s*<appender name="DEBUGLOG"(?:.*\n)+?\s*<maxFileSize>)(\w+)(</maxFileSize>)\n'
        A portion of the regular expression above denoted by (?:.*\n)+?\s* requires some explanation. First, (?:...)
        denotes a non-capturing version of regular parentheses. Thus, after matching "DEBUGLOG", we match any number of
        characters, up to and including a newline, one or more times, in a non-greedy fashion.  Then, preceding <maxFileSize>
        we match any number of whitespace characters.  It is important to match in a non-greedy fashion, which matches
        as little text as possible because if we didn't, the regex would match other text up until the last <maxFileSize>
        tag later in the logback.xml file which would not be the desired result.

        <appender name="DEBUGLOG" ... <maxFileSize>20</maxFileSize>
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(\s*<appender name="DEBUGLOG"(?:.*\n)+?\s*<maxFileSize>)(\w+)(</maxFileSize>)\n',
            jinja_variable='logback_xml.debuglog_maxfilesize')

    def root_log_level(self):
        """
        <root level="INFO">
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(\s*<root level=")(.*)(">)\n',
            jinja_variable='logback_xml.root_log_level')

    def appender_systemlog_enabled(self):
        """
        <appender-ref ref="SYSTEMLOG" />
        :return:
        """
        self.add_jinja_to_comment_xml_option(
            option_pattern=r'^(\s*)(<appender-ref ref="SYSTEMLOG" />)\n',
            jinja_variable='logback_xml.appender_systemlog_enabled')

    def appender_stdout_enabled(self):
        """
        <appender-ref ref="STDOUT" />
        :return:
        """
        self.add_jinja_to_comment_xml_option(
            option_pattern=r'^(\s*)(<appender-ref ref="STDOUT" />)\n',
            jinja_variable='logback_xml.appender_stdout_enabled')

    def appender_asyncdebuglog_enabled(self):
        """
        <appender-ref ref="ASYNCDEBUGLOG" /> <!-- Comment this line to disable debug.log -->
        :return:
        """
        self.add_jinja_to_comment_xml_option(
            option_pattern=r'^(\s*)(<appender-ref ref="ASYNCDEBUGLOG" />)(.*)\n',
            jinja_variable='logback_xml.appender_asyncdebuglog_enabled')

    def cassandra_logger_level(self):
        """
        <logger name="org.apache.cassandra" level="DEBUG"/>
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(\s*<logger name="org.apache.cassandra" level=")(.*)("/>)\n',
            jinja_variable='logback_xml.cassandra_logger_level')

    def thrift_logger_level(self):
        """
        <logger name="com.thinkaurelius.thrift" level="ERROR"/>
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(\s*<logger name="com.thinkaurelius.thrift" level=")(.*)("/>)\n',
            jinja_variable='logback_xml.cassandra_logger_level')
