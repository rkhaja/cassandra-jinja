import logging

import cassandra_jinja2.base_config

logger = logging.getLogger(__name__)


class JvmOptions(cassandra_jinja2.base_config.BaseConfig):
    """
    Class to parse a jvm.options file and generate a Jinja2 template.

    Methods implemented in this class use regular expressions to match options in the jvm.options file.  Care must be
    taken to escape regular expression metacharacters: . ^ $ * + ? { } [ ] \ | ( )
    See: https://docs.python.org/3/howto/regex.html#matching-characters
    """

    def __init__(self, cassandra_version):
        super().__init__(cassandra_version)

    def generate_template(self):
        self.min_heap_size()
        self.max_heap_size()
        self.heap_newsize()
        self.use_par_new_gc()
        self.use_conc_mark_sweep_gc()
        self.cms_parallel_remark_enabled()
        self.survivor_ratio()
        self.max_tenuring_threshold()
        self.cms_initiating_occupancy_fraction()
        self.use_cms_initiating_occupancy_only()
        self.cms_wait_duration()
        self.cms_parallel_initial_mark_enabled()
        self.cms_eden_chunk_record_always()
        self.cms_class_unloading_enabled()
        self.use_g1_gc()
        self.g1r_set_updating_pause_millis()
        self.max_gc_pause_millis()
        self.initiating_heap_occupancy_percent()
        self.parallel_gc_threads()
        self.conc_gc_threads()
        self.print_gc_details()
        self.print_gc_date_stamps()
        self.print_heap_at_gc()
        self.print_tenuring_distribution()
        self.print_gc_application_stopped_time()
        self.print_promotion_failure()
        self.print_fls_statistics()
        self.log_gc()
        self.use_gc_log_file_rotation()
        self.number_of_gc_log_files()
        self.gc_log_file_size()
        self.extra_opts()

    def min_heap_size(self):
        """
        #-Xms4G
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^#(-Xms)(.*)\n',
            jinja_variable='jvm_options.min_heap_size')

    def max_heap_size(self):
        """
        #-Xmx4G
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^#(-Xmx)(.*)\n',
            jinja_variable='jvm_options.max_heap_size')

    def heap_newsize(self):
        """
        #-Xmn800M
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^#(-Xmn)(.*)\n',
            jinja_variable='jvm_options.heap_newsize')

    def use_par_new_gc(self):
        """
        -XX:+UseParNewGC
        :return:
        """
        # Escape +
        self.add_jinja_to_comment_option_conditionally(
            option_pattern=r'^(-XX:\+UseParNewGC)\n',
            jinja_variable='jvm_options.use_g1_gc')
        self.add_jinja_for_flag_option(
            option_pattern=r'^(-XX:\+UseParNewGC)\n',
            jinja_variable='jvm_options.use_par_new_gc')

    def use_conc_mark_sweep_gc(self):
        """
        -XX:+UseConcMarkSweepGC
        :return:
        """
        # Escape +
        self.add_jinja_to_comment_option_conditionally(
            option_pattern=r'^(-XX:\+UseConcMarkSweepGC)\n',
            jinja_variable='jvm_options.use_g1_gc')
        self.add_jinja_for_flag_option(
            option_pattern=r'^(-XX:\+UseConcMarkSweepGC)\n',
            jinja_variable='jvm_options.use_conc_mark_sweep_gc')

    def cms_parallel_remark_enabled(self):
        """
        -XX:+CMSParallelRemarkEnabled
        :return:
        """
        # Escape +
        self.add_jinja_to_comment_option_conditionally(
            option_pattern=r'^(-XX:\+CMSParallelRemarkEnabled)\n',
            jinja_variable='jvm_options.use_g1_gc')
        self.add_jinja_for_flag_option(
            option_pattern=r'^(-XX:\+CMSParallelRemarkEnabled)\n',
            jinja_variable='jvm_options.cms_parallel_remark_enabled')

    def survivor_ratio(self):
        """
        -XX:SurvivorRatio=8
        :return:
        """
        self.add_jinja_to_comment_option_conditionally(
            option_pattern=r'^(-XX:SurvivorRatio=)(.*)\n',
            jinja_variable='jvm_options.use_g1_gc')
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(-XX:SurvivorRatio=)(.*)\n',
            jinja_variable='jvm_options.survivor_ratio')

    def max_tenuring_threshold(self):
        """
        -XX:MaxTenuringThreshold=1
        :return:
        """
        self.add_jinja_to_comment_option_conditionally(
            option_pattern=r'^(-XX:MaxTenuringThreshold=)(.*)\n',
            jinja_variable='jvm_options.use_g1_gc')
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(-XX:MaxTenuringThreshold=)(.*)\n',
            jinja_variable='jvm_options.max_tenuring_threshold')

    def cms_initiating_occupancy_fraction(self):
        """
        -XX:CMSInitiatingOccupancyFraction=75
        :return:
        """
        self.add_jinja_to_comment_option_conditionally(
            option_pattern=r'^(-XX:CMSInitiatingOccupancyFraction=)(.*)\n',
            jinja_variable='jvm_options.use_g1_gc')
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(-XX:CMSInitiatingOccupancyFraction=)(.*)\n',
            jinja_variable='jvm_options.cms_initiating_occupancy_fraction')

    def use_cms_initiating_occupancy_only(self):
        """
        -XX:+UseCMSInitiatingOccupancyOnly
        :return:
        """
        # Escape +
        self.add_jinja_to_comment_option_conditionally(
            option_pattern=r'^(-XX:\+UseCMSInitiatingOccupancyOnly)\n',
            jinja_variable='jvm_options.use_g1_gc')
        self.add_jinja_for_flag_option(
            option_pattern=r'^(-XX:\+UseCMSInitiatingOccupancyOnly)\n',
            jinja_variable='jvm_options.use_cms_initiating_occupancy_only')

    def cms_wait_duration(self):
        """
        -XX:CMSWaitDuration=10000
        :return:
        """
        self.add_jinja_to_comment_option_conditionally(
            option_pattern=r'^(-XX:CMSWaitDuration=)(.*)\n',
            jinja_variable='jvm_options.use_g1_gc')
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(-XX:CMSWaitDuration=)(.*)\n',
            jinja_variable='jvm_options.cms_wait_duration')

    def cms_parallel_initial_mark_enabled(self):
        """
        -XX:+CMSParallelInitialMarkEnabled
        :return:
        """
        # Escape +
        self.add_jinja_to_comment_option_conditionally(
            option_pattern=r'^(-XX:\+CMSParallelInitialMarkEnabled)\n',
            jinja_variable='jvm_options.use_g1_gc')
        self.add_jinja_for_flag_option(
            option_pattern=r'^(-XX:\+CMSParallelInitialMarkEnabled)\n',
            jinja_variable='jvm_options.cms_parallel_initial_mark_enabled')

    def cms_eden_chunk_record_always(self):
        """
        -XX:+CMSEdenChunksRecordAlways
        :return:
        """
        # Escape +
        self.add_jinja_to_comment_option_conditionally(
            option_pattern=r'^(-XX:\+CMSEdenChunksRecordAlways)\n',
            jinja_variable='jvm_options.use_g1_gc')
        self.add_jinja_for_flag_option(
            option_pattern=r'^(-XX:\+CMSEdenChunksRecordAlways)\n',
            jinja_variable='jvm_options.cms_eden_chunk_record_always')

    def cms_class_unloading_enabled(self):
        """
        -XX:+CMSClassUnloadingEnabled
        :return:
        """
        # Escape +
        self.add_jinja_to_comment_option_conditionally(
            option_pattern=r'^(-XX:\+CMSClassUnloadingEnabled)\n',
            jinja_variable='jvm_options.use_g1_gc')
        self.add_jinja_for_flag_option(
            option_pattern=r'^(-XX:\+CMSClassUnloadingEnabled)\n',
            jinja_variable='jvm_options.cms_class_unloading_enabled')

    def use_g1_gc(self):
        """
        #-XX:+UseG1GC
        :return:
        """
        # Escape +
        self.add_jinja_for_commented_flag_option(
            option_pattern=r'^#(-XX:\+UseG1GC)\n',
            jinja_variable='jvm_options.use_g1_gc')

    def g1r_set_updating_pause_millis(self):
        """
        #-XX:G1RSetUpdatingPauseTimePercent=5
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^#(-XX:G1RSetUpdatingPauseTimePercent=)(.*)\n',
            jinja_variable='jvm_options.g1r_set_updating_pause_millis')

    def max_gc_pause_millis(self):
        """
        #-XX:MaxGCPauseMillis=500
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'#(-XX:MaxGCPauseMillis=)(.*)\n',
            jinja_variable='jvm_options.max_gc_pause_millis')

    def initiating_heap_occupancy_percent(self):
        """
        #-XX:InitiatingHeapOccupancyPercent=70
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^#(-XX:InitiatingHeapOccupancyPercent=)(.*)\n',
            jinja_variable='jvm_options.initiating_heap_occupancy_percent')

    def parallel_gc_threads(self):
        """
        #-XX:ParallelGCThreads=16
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^#(-XX:ParallelGCThreads=)(.*)\n',
            jinja_variable='jvm_options.parallel_gc_threads')

    def conc_gc_threads(self):
        """
        #-XX:ConcGCThreads=16
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^#(-XX:ConcGCThreads=)(.*)\n',
            jinja_variable='jvm_options.conc_gc_threads')

    def print_gc_details(self):
        """
        -XX:+PrintGCDetails
        :return:
        """
        # Escape +
        self.add_jinja_for_flag_option(
            option_pattern=r'^(-XX:\+PrintGCDetails)\n',
            jinja_variable='jvm_options.print_gc_details')

    def print_gc_date_stamps(self):
        """
        -XX:+PrintGCDateStamps
        :return:
        """
        # Escape +
        self.add_jinja_for_flag_option(
            option_pattern=r'^(-XX:\+PrintGCDateStamps)\n',
            jinja_variable='jvm_options.print_gc_date_stamps')

    def print_heap_at_gc(self):
        """
        -XX:+PrintHeapAtGC
        :return:
        """
        # Escape +
        self.add_jinja_for_flag_option(
            option_pattern=r'^(-XX:\+PrintHeapAtGC)\n',
            jinja_variable='jvm_options.print_heap_at_gc')

    def print_tenuring_distribution(self):
        """
        -XX:+PrintTenuringDistribution
        :return:
        """
        # Escape +
        self.add_jinja_for_flag_option(
            option_pattern=r'^(-XX:\+PrintTenuringDistribution)\n',
            jinja_variable='jvm_options.print_tenuring_distribution')

    def print_gc_application_stopped_time(self):
        """
        -XX:+PrintGCApplicationStoppedTime
        :return:
        """
        # Escape +
        self.add_jinja_for_flag_option(
            option_pattern=r'^(-XX:\+PrintGCApplicationStoppedTime)\n',
            jinja_variable='jvm_options.print_gc_application_stopped_time')

    def print_promotion_failure(self):
        """
        -XX:+PrintPromotionFailure
        :return:
        """
        # Escape +
        self.add_jinja_for_flag_option(
            option_pattern=r'^(-XX:\+PrintPromotionFailure)\n',
            jinja_variable='jvm_options.print_promotion_failure')

    def print_fls_statistics(self):
        """
        #-XX:PrintFLSStatistics=1
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^#(-XX:PrintFLSStatistics=)(.*)\n',
            jinja_variable='jvm_options.print_fls_statistics')

    def log_gc(self):
        """
        #-Xloggc:/var/log/cassandra/gc.log
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^#(-Xloggc:)(.*)\n',
            jinja_variable='jvm_options.log_gc')

    def use_gc_log_file_rotation(self):
        """
        -XX:+UseGCLogFileRotation
        :return:
        """
        # Escape +
        self.add_jinja_for_flag_option(
            option_pattern=r'^(-XX:\+UseGCLogFileRotation)\n',
            jinja_variable='jvm_options.use_gc_log_file_rotation')

    def number_of_gc_log_files(self):
        """
        -XX:NumberOfGCLogFiles=10
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(-XX:NumberOfGCLogFiles=)(.*)\n',
            jinja_variable='jvm_options.number_of_gc_log_files')

    def gc_log_file_size(self):
        """
        -XX:GCLogFileSize=10M
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(-XX:GCLogFileSize=)(.*)\n',
            jinja_variable='jvm_options.gc_log_file_size')

    def extra_opts(self):
        """
        :return:
        """
        jinja_variable='jvm_options.extra_opts'
        replacement = '{%- if ' + jinja_variable + ' is defined %}\n'
        replacement += '### Extra JVM Options\n'
        replacement += '{%- for opt in ' + jinja_variable + ' %}\n'
        replacement += '{{ opt }}\n'
        replacement += '{%- endfor %}\n'
        replacement += '{%- endif -%}\n'
        self.content += replacement
