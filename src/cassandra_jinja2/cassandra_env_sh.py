import logging
import re

import cassandra_jinja2.base_config

logger = logging.getLogger(__name__)


class CassandraEnvSh(cassandra_jinja2.base_config.BaseConfig):
    """
    Class to parse a cassandra-env.sh file and generate a Jinja2 template.

    Methods implemented in this class use regular expressions to match options in the jvm.options file.  Care must be
    taken to escape regular expression metacharacters: . ^ $ * + ? { } [ ] \ | ( )
    See: https://docs.python.org/3/howto/regex.html#matching-characters
    """

    def __init__(self, cassandra_version):
        super().__init__(cassandra_version)

    def generate_template(self):
        self.log_gc()
        self.max_heap_size()
        self.heap_newsize()
        self.malloc_arena_max()
        self.prefer_ipv4_stack()
        self.local_jmx()
        self.jmx_port()
        self.jmxremote_authenticate()
        self.jmxremote_password_file()
        self.jvm_extra_opts()

    def log_gc(self):
        """
        JVM_OPTS="$JVM_OPTS -Xloggc:${CASSANDRA_HOME}/logs/gc.log"
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(JVM_OPTS="\$JVM_OPTS -Xloggc:)(.*)(/gc.log")\n',
            jinja_variable='cassandra_env_sh.log_gc')

    def max_heap_size(self):
        """
        #MAX_HEAP_SIZE="4G"
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^#(MAX_HEAP_SIZE=")(.*)(")\n',
            jinja_variable='cassandra_env_sh.max_heap_size')

    def heap_newsize(self):
        """
        #HEAP_NEWSIZE="800M"
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^#(HEAP_NEWSIZE=")(.*)(")\n',
            jinja_variable='cassandra_env_sh.heap_newsize')

    def malloc_arena_max(self):
        """
        #export MALLOC_ARENA_MAX=4
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^#(export MALLOC_ARENA_MAX=)(.*)\n',
            jinja_variable='cassandra_env_sh.malloc_arena_max')

    def prefer_ipv4_stack(self):
        """
        This option should be left uncommented if using IPv4 and commented out if using IPv6.
        The cassandra-env.sh file says:
        # comment out this entry to enable IPv6 support
        Therfore, we use the method add_jinja_for_flag_option() to toggle between uncommented and commented values.
        JVM_OPTS="$JVM_OPTS -Djava.net.preferIPv4Stack=true"
        :return:
        """
        self.add_jinja_for_flag_option(
            option_pattern=r'^(JVM_OPTS="\$JVM_OPTS -Djava.net.preferIPv4Stack=true")\n',
            jinja_variable='cassandra_env_sh.prefer_ipv4_stack')

    def local_jmx(self):
        """
        This method needs its own implementation for the jinja produced because of formatting reasons (ie. we do not
        want to affect leading spaces preceding LOCAL_JMX=).
        LOCAL_JMX=yes
        :return:
        """
        option_pattern = r'^(\s*LOCAL_JMX=)(yes)\n'
        jinja_variable = 'cassandra_env_sh.local_jmx'
        compiled_pattern = re.compile(option_pattern, re.MULTILINE)
        match = compiled_pattern.search(self.content)
        if match:
            replacement = '{%- if ' + jinja_variable + ' | default(true) %}\n'
            replacement += match.group(0)
            replacement += '{%- else %}\n'
            replacement += match.group(1) +'no' + '\n'
            replacement += '{%- endif %}\n'
            self.content = compiled_pattern.sub(replacement, self.content)

    def jmx_port(self):
        """
        JMX_PORT="7199"
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'(JMX_PORT=")(\d+)(")\n',
            jinja_variable='cassandra_env_sh.jmx_port')

    def jmxremote_authenticate(self):
        """
        JVM_OPTS="$JVM_OPTS -Dcom.sun.management.jmxremote.authenticate=true"
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(\s*JVM_OPTS="\$JVM_OPTS -Dcom.sun.management.jmxremote.authenticate=)(.*)(")\n',
            jinja_variable='cassandra_env_sh.jmxremote_authenticate')

    def jmxremote_password_file(self):
        """
        JVM_OPTS="$JVM_OPTS -Dcom.sun.management.jmxremote.password.file=/etc/cassandra/jmxremote.password"
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(\s*JVM_OPTS="\$JVM_OPTS -Dcom.sun.management.jmxremote.password.file=)(.*)(")\n',
            jinja_variable='cassandra_env_sh.jmxremote_password_file')

    def jvm_extra_opts(self):
        """
        This method needs its own implementation for the jinja produced because a new condition must be added, which
        joins a list of jvm_extra_opts with spaces.
        JVM_OPTS="$JVM_OPTS $JVM_EXTRA_OPTS"
        :return:
        """
        option_pattern = r'^(\s*JVM_OPTS="\$JVM_OPTS \$JVM_EXTRA_OPTS)(")\n'
        jinja_variable = 'cassandra_env_sh.jvm_extra_opts'
        compiled_pattern = re.compile(option_pattern, re.MULTILINE)
        match = compiled_pattern.search(self.content)
        if match:
            replacement = '{% if ' + jinja_variable + ' is defined -%}\n'
            replacement += 'JVM_EXTRA_OPTS="$JVM_EXTRA_OPTS {{ ' + jinja_variable + ' | join(' ') }}"\n'
            replacement += '{%- endif -%}\n'
            replacement += match.group(0)
            self.content = compiled_pattern.sub(replacement, self.content)

