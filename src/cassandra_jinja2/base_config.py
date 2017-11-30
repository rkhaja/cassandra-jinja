import jinja2
import logging
import os
import re

logger = logging.getLogger(__name__)


class BaseConfig(object):

    def __init__(self, cassandra_version):
        self.cassandra_version = cassandra_version
        self.content = ''

    def read(self, file):
        with open(file, 'r') as f:
            self.content = f.read()
        f.close()

    def write(self, file):
        directory = os.path.dirname(file)
        if not os.path.exists(directory):
            logger.info('directory: [{}] does not exist. Creating directory.'.format(directory))
            os.makedirs(directory)
        else:
            logger.info('directory: [{}] already exists. Nothing to do.'.format(directory))
        with open(file, 'w') as f:
            f.write(self.content)
        f.close()

    @staticmethod
    def render(template_file, render_file, context):
        template_directory = os.path.dirname(template_file)
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_directory))
        template = env.get_template(os.path.basename(template_file))
        render_directory = os.path.dirname(render_file)
        if not os.path.exists(render_directory):
            logger.info('directory: [{}] does not exist. Creating directory.'.format(render_directory))
            os.makedirs(render_directory)
        else:
            logger.info('directory: [{}] already exists. Nothing to do.'.format(render_directory))
        with open(render_file, 'w') as f:
            f.write(template.render(context) + '\n')
        f.close()

    def add_jinja_for_option_with_default_value(self, option_pattern, jinja_variable):
        """

            Examples:
            (1)
            (2) JVM_OPTS="$JVM_OPTS -Dcom.sun.management.jmxremote.authenticate=true"
                  => option_pattern=r'^(\s*JVM_OPTS="\$JVM_OPTS -Dcom.sun.management.jmxremote.authenticate=)(.*)(")\n
            (3) cluster_name: 'Test Cluster'  =>  option_pattern=r"^(cluster_name: ')(.*)(')\n"
            (4) <file>${cassandra.logdir}/system.log</file> => option_pattern=r'^(\s*<file>)(.*)(/system.log</file>\n)'

        :param option_pattern:
        :param jinja_variable:
        :return:
        """
        compiled_pattern = re.compile(option_pattern, re.MULTILINE)
        match = compiled_pattern.search(self.content)
        if match:
            # If the value is either true of false, it must be made lower case, otherwise when jinja templates are
            # filled with pillars using Salt-Stack, it is possible that they will be rendered as True or False as is the
            # convention in Python.
            if match.group(2) == 'true' or match.group(2) == 'false':
                if compiled_pattern.groups == 3:
                    replacement = match.group(1) + '{{ ' + jinja_variable + ' | default("' + match.group(2) \
                                  + '") | lower }}' + match.group(3) + '\n'
                else:
                    replacement = match.group(1) + '{{ ' + jinja_variable + ' | default("' + match.group(2) \
                                  + '") | lower }}' + '\n'
            else:
                if compiled_pattern.groups == 3:
                    replacement = match.group(1) + '{{ ' + jinja_variable + ' | default("' + match.group(2) \
                                  + '") }}' + match.group(3) + '\n'
                else:
                    replacement = match.group(1) + '{{ ' + jinja_variable + ' | default("' + match.group(2) \
                                  + '") }}' + '\n'
            self.content = compiled_pattern.sub(replacement, self.content)

    def add_jinja_for_commented_option_with_default_value(self, option_pattern, jinja_variable):
        """
        Essentially, there is a kind of option that you typically see in a config file that is commented out, beginning
        with a #.  You do not want to uncomment it and set your own value because then you would lose the information of
        what the default value might be.  Instead, you want to append an uncommented version of the variable that has
        your value assigned.

        Examples:
            (1) #-Xmx4G                                =>  option_pattern=r'^#(-Xmx)(.*)\n'
            (2) #-XX:MaxGCPauseMillis=500              =>  option_pattern=r'^#(--XX:MaxGCPauseMillis=)(.*)\n'
            (3) #MAX_HEAP_SIZE="4G"                    =>  option_pattern=r'^#(MAX_HEAP_SIZE=")(.*)(")\n'
            (4) # listen_interface_prefer_ipv6: false  =>  option_pattern=r'^# (listen_interface_prefer_ipv6: )(.*)\n'

        In the first example, the option_pattern memoizes the option denoted by -Xmx.  It is not necessary to memoize
        the value, because typically, if one is setting this variable, it would be overriding the default value
        specified by the commented option.

        The second example is a little more complicated in that we also need to memoize the delimiter that is separating
        the option and the value (in this case an = sign).  Thus, if a delimeter exists, remember to memoize the
        delimiter as part of the regex that is memoizing the option.

        Third, sometimes options may have characters surrounding their value.  In the third example, not only is the
        option and value separated by a delimiter, but the value is surrounded by quotes. In this case, we need to
        memoize as the first match group, the variable, delimiter and first surrounding character, and as the second
        match group we need to memoize the second surrounding character.

        Finally, in the fourth example, it is important to memoize the value because this ensures that the jinja has
        logic to lowercase true/false values.

        :param option_pattern:
        :param option_group:
        :param jinja_variable:
        :param option_value_seperator:
        :return:
        """
        # TODO: Assert that the option_pattern is a raw string and that it begins with ^#.
        compiled_pattern = re.compile(option_pattern, re.MULTILINE)
        match = compiled_pattern.search(self.content)
        if match:
            replacement = match.group(0)
            replacement += '{%- if ' + jinja_variable + ' is defined %}\n'
            if match.group(2) == 'true' or match.group(2) == 'false':
                if compiled_pattern.groups == 3:
                    replacement += match.group(1) + '{{ ' + jinja_variable + ' | lower }}' + match.group(3) + '\n'
                else:
                    replacement += match.group(1) + '{{ ' + jinja_variable + ' | lower }}' + '\n'
            else:
                if compiled_pattern.groups == 3:
                    replacement += match.group(1) + '{{ ' + jinja_variable + ' }}' + match.group(3) + '\n'
                else:
                    replacement += match.group(1) + '{{ ' + jinja_variable + ' }}' + '\n'
            replacement += '{%- endif %}\n'
            self.content = compiled_pattern.sub(replacement, self.content)

    def add_jinja_for_option_with_no_default_value(self, option_pattern, jinja_variable):
        compiled_pattern = re.compile(option_pattern, re.MULTILINE)
        match = compiled_pattern.search(self.content)
        if match:
            replacement = '{% if ' + jinja_variable + ' is defined -%}\n'
            replacement += match.group(1) + ' {{ ' + jinja_variable + ' }}' + '\n'
            replacement += '{%- else -%}\n'
            replacement += match.group(0)
            replacement += '{%- endif %}\n'
            self.content = compiled_pattern.sub(replacement, self.content)

    def add_jinja_for_commented_option_with_no_default_value(self, option_pattern, jinja_variable):
        compiled_pattern = re.compile(option_pattern, re.MULTILINE)
        match = compiled_pattern.search(self.content)
        if match:
            replacement = match.group(0)
            replacement += '{%- if ' + jinja_variable + ' is defined %}\n'
            replacement += match.group(1) + ' {{ ' + jinja_variable + ' }}' + '\n'
            replacement += '{%- endif %}\n'
            self.content = compiled_pattern.sub(replacement, self.content)

    def add_jinja_for_flag_option(self, option_pattern, jinja_variable):
        compiled_pattern = re.compile(option_pattern, re.MULTILINE)
        match = compiled_pattern.search(self.content)
        if match:
            replacement = '{% if ' + jinja_variable + ' | default(true) -%}\n'
            replacement += match.group(0)
            replacement += '{%- else -%}\n'
            replacement += '#' + match.group(0)
            replacement += '{%- endif %}\n'
            self.content = compiled_pattern.sub(replacement, self.content)

    def add_jinja_for_commented_flag_option(self, option_pattern, jinja_variable):
        compiled_pattern = re.compile(option_pattern, re.MULTILINE)
        match = compiled_pattern.search(self.content)
        if match:
            replacement = match.group(0)
            replacement += '{%- if ' + jinja_variable + ' | default(false) -%}\n'
            replacement += match.group(1) + '\n'
            replacement += '{%- endif %}\n'
            self.content = compiled_pattern.sub(replacement, self.content)

    def add_jinja_to_comment_option_conditionally(self, option_pattern, jinja_variable):
        compiled_pattern = re.compile(option_pattern, re.MULTILINE)
        match = compiled_pattern.search(self.content)
        if match:
            replacement = '{% if ' + jinja_variable + ' | default(false) -%}\n'
            replacement += '#' + match.group(0)
            replacement += '{%- else -%}\n'
            replacement += match.group(0)
            replacement += '{%- endif %}\n'
            self.content = compiled_pattern.sub(replacement, self.content)
