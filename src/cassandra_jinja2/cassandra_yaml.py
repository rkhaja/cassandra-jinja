import logging
import re

import cassandra_jinja2.base_config

logger = logging.getLogger(__name__)


class CassandraYaml(cassandra_jinja2.base_config.BaseConfig):
    """
    Class to parse a cassandra.yaml file and generate a Jinja2 template.

    Methods implemented in this class use regular expressions to match options in the jvm.options file.  Care must be
    taken to escape regular expression metacharacters: . ^ $ * + ? { } [ ] \ | ( )
    See: https://docs.python.org/3/howto/regex.html#matching-characters
    """

    def __init__(self, cassandra_version):
        super().__init__(cassandra_version)

    def generate_template(self):
        # TODO: There may be a way to simplify this using introspection, by iterating through and executing all
        # methods, but possibly excluding some methods like __init__(), and this method itself, and inherited methods.
        # This would be helpful to make this class more easily maintainable.
        self.cluster_name()
        self.num_tokens()
        self.allocate_tokens_for_keyspace()
        self.initial_token()
        self.hinted_handoff_enabled()
        self.hinted_handoff_disabled_datacenters()
        self.max_hint_window_in_ms()
        self.hinted_handoff_throttle_in_kb()
        self.max_hints_delivery_threads()
        self.hints_directory()
        self.hints_flush_period_in_ms()
        self.max_hints_file_size_in_mb()
        self.hints_compression()
        self.batchlog_replay_throttle_in_kb()
        self.authenticator()
        self.authorizer()
        self.role_manager()
        self.roles_validity_in_ms()
        self.roles_update_interval_in_ms()
        self.permissions_validity_in_ms()
        self.permissions_update_interval_in_ms()
        self.partitioner()
        self.data_file_directories()
        self.commitlog_directory()
        self.disk_failure_policy()
        self.commit_failure_policy()
        self.key_cache_size_in_mb()
        self.key_cache_save_period()
        self.key_cache_keys_to_save()
        self.row_cache_class_name()
        self.row_cache_size_in_mb()
        self.row_cache_save_period()
        self.row_cache_keys_to_save()
        self.counter_cache_size_in_mb()
        self.counter_cache_save_period()
        self.counter_cache_keys_to_save()
        self.saved_caches_directory()
        self.commitlog_sync()
        self.commitlog_sync_period_in_ms()
        self.commitlog_segment_size_in_mb()
        self.commitlog_compression()
        self.seeds()
        self.concurrent_reads()
        self.concurrent_writes()
        self.concurrent_counter_writes()
        self.concurrent_materialized_view_writes()
        self.file_cache_size_in_mb()
        self.buffer_pool_use_heap_if_exhausted()
        self.disk_optimization_strategy()
        self.memtable_heap_space_in_mb()
        self.memtable_offheap_space_in_mb()
        self.memtable_cleanup_threshold()
        self.memtable_allocation_type()
        self.commitlog_total_space_in_mb()
        self.memtable_flush_writers()
        self.index_summary_capacity_in_mb()
        self.index_summary_resize_interval_in_minutes()
        self.trickle_fsync()
        self.trickle_fsync_interval_in_kb()
        self.storage_port()
        self.ssl_storage_port()
        self.listen_address()
        self.listen_interface()
        self.listen_interface_prefer_ipv6()
        self.broadcast_address()
        self.listen_on_broadcast_address()
        self.internode_authenticator()
        self.start_native_transport()
        self.native_transport_port()
        self.native_transport_port_ssl()
        self.native_transport_max_threads()
        self.native_transport_max_frame_size_in_mb()
        self.native_transport_max_concurrent_connections()
        self.native_transport_max_concurrent_connections_per_ip()
        self.start_rpc()
        self.rpc_address()
        self.rpc_interface()
        self.rpc_interface_prefer_ipv6()
        self.rpc_port()
        self.broadcast_rpc_address()
        self.rpc_keepalive()
        self.rpc_server_type()
        self.rpc_min_threads()
        self.rpc_max_threads()
        self.rpc_send_buff_size_in_bytes()
        self.rpc_recv_buff_size_in_bytes()
        self.internode_send_buff_size_in_bytes()
        self.internode_recv_buff_size_in_bytes()
        self.thrift_framed_transport_size_in_mb()
        self.incremental_backups()
        self.snapshot_before_compaction()
        self.auto_snapshot()
        self.tombstone_warn_threshold()
        self.tombstone_failure_threshold()
        self.column_index_size_in_kb()
        self.batch_size_warn_threshold_in_kb()
        self.batch_size_fail_threshold_in_kb()
        self.unlogged_batch_across_partitions_warn_threshold()
        self.concurrent_compactors()
        self.compaction_throughput_mb_per_sec()
        self.compaction_large_partition_warning_threshold_mb()
        self.sstable_preemptive_open_interval_in_mb()
        self.stream_throughput_outbound_megabits_per_sec()
        self.inter_dc_stream_throughput_outbound_megabits_per_sec()
        self.read_request_timeout_in_ms()
        self.range_request_timeout_in_ms()
        self.write_request_timeout_in_ms()
        self.counter_write_request_timeout_in_ms()
        self.cas_contention_timeout_in_ms()
        self.truncate_request_timeout_in_ms()
        self.request_timeout_in_ms()
        self.cross_node_timeout()
        self.streaming_socket_timeout_in_ms()
        self.phi_convict_threshold()
        self.endpoint_snitch()
        self.dynamic_snitch_update_interval_in_ms()
        self.dynamic_snitch_reset_interval_in_ms()
        self.dynamic_snitch_badness_threshold()
        self.request_scheduler()
        self.request_scheduler_options()
        self.request_scheduler_id()
        self.server_encryption_options()
        self.client_encryption_options()
        self.internode_compression()
        self.inter_dc_tcp_nodelay()
        self.tracetype_query_ttl()
        self.tracetype_repair_ttl()
        self.gc_log_threshold_in_ms()
        self.gc_warn_threshold_in_ms()
        self.enable_user_defined_functions()
        self.enable_scripted_user_defined_functions()
        self.windows_timer_interval()
        self.max_value_size_in_mb()
        self.otc_coalescing_strategy()
        self.otc_coalescing_window_us()
        self.otc_coalescing_enough_coalesced_messages()
        self.otc_backlog_expiration_interval_ms()

    def cluster_name(self):
        """
        cluster_name: 'Test Cluster'
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r"^(cluster_name: ')(.*)(')\n",
            jinja_variable='cassandra_yaml.cluster_name')

    def num_tokens(self):
        """
        num_tokens: 256
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(num_tokens: )(.*)\n',
            jinja_variable='cassandra_yaml.num_tokens')

    def allocate_tokens_for_keyspace(self):
        """
        # allocate_tokens_for_keyspace: KEYSPACE
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (allocate_tokens_for_keyspace: )(.*)\n',
            jinja_variable='cassandra_yaml.allocate_tokens_for_keyspace')

    def initial_token(self):
        """
        # initial_token:
        :return:
        """
        self.add_jinja_for_commented_option_with_no_default_value(
            option_pattern=r'^# (initial_token:)\n',
            jinja_variable='cassandra_yaml.initial_token')

    def hinted_handoff_enabled(self):
        """
        hinted_handoff_enabled: true
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(hinted_handoff_enabled: )(.*)\n',
            jinja_variable='cassandra_yaml.hinted_handoff_enabled')

    def hinted_handoff_disabled_datacenters(self):
        """
        #hinted_handoff_disabled_datacenters:
        #    - DC1
        #    - DC2
        :return:
        """
        pass

    def max_hint_window_in_ms(self):
        """
        max_hint_window_in_ms: 10800000 # 3 hours
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(max_hint_window_in_ms: )(.*)( # 3 hours)\n',
            jinja_variable='cassandra_yaml.max_hint_window_in_ms')

    def hinted_handoff_throttle_in_kb(self):
        """
        hinted_handoff_throttle_in_kb: 1024
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(hinted_handoff_throttle_in_kb: )(.*)\n',
            jinja_variable='cassandra_yaml.hinted_handoff_throttle_in_kb')

    def max_hints_delivery_threads(self):
        """
        max_hints_delivery_threads: 2
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(max_hints_delivery_threads: )(.*)\n',
            jinja_variable='cassandra_yaml.max_hints_delivery_threads')

    def hints_directory(self):
        """
        # hints_directory: /var/lib/cassandra/hints
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (hints_directory: )(.*)\n',
            jinja_variable='cassandra_yaml.hints_directory')

    def hints_flush_period_in_ms(self):
        """
        hints_flush_period_in_ms: 10000
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(hints_flush_period_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.hints_flush_period_in_ms')

    def max_hints_file_size_in_mb(self):
        """
        max_hints_file_size_in_mb: 128
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(max_hints_file_size_in_mb: )(.*)\n',
            jinja_variable='cassandra_yaml.max_hints_file_size_in_mb')

    def hints_compression(self):
        """
        #hints_compression:
        #   - class_name: LZ4Compressor
        #     parameters:
        #         -
        :return:
        """
        pass

    def batchlog_replay_throttle_in_kb(self):
        """
        batchlog_replay_throttle_in_kb: 1024
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(batchlog_replay_throttle_in_kb: )(.*)\n',
            jinja_variable='cassandra_yaml.batchlog_replay_throttle_in_kb')

    def authenticator(self):
        """
        authenticator: AllowAllAuthenticator
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(authenticator: )(.*)\n',
            jinja_variable='cassandra_yaml.authenticator')

    def authorizer(self):
        """
        authorizer: AllowAllAuthorizer
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(authorizer: )(.*)\n',
            jinja_variable='cassandra_yaml.authorizer')

    def role_manager(self):
        """
        role_manager: CassandraRoleManager
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(role_manager: )(.*)\n',
            jinja_variable='cassandra_yaml.role_manager')

    def roles_validity_in_ms(self):
        """
        roles_validity_in_ms: 2000
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(roles_validity_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.roles_validity_in_ms')

    def roles_update_interval_in_ms(self):
        """
        # roles_update_interval_in_ms: 1000
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (roles_update_interval_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.roles_update_interval_in_ms')

    def permissions_validity_in_ms(self):
        """
        permissions_validity_in_ms: 2000
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(permissions_validity_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.permissions_validity_in_ms')

    def permissions_update_interval_in_ms(self):
        """
        # permissions_update_interval_in_ms: 1000
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (permissions_update_interval_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.permissions_update_interval_in_ms')

    def partitioner(self):
        """
        partitioner: org.apache.cassandra.dht.Murmur3Partitioner
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(partitioner: )(.*)\n',
            jinja_variable='cassandra_yaml.partitioner')

    def data_file_directories(self):
        """
        This method requires a custom implementation for the jinja produced because multiple data_file_directories can
        be listed.
        # data_file_directories:
        #     - /var/lib/cassandra/data
        :return:
        """
        option_pattern = r'^(# data_file_directories:\n#\s*- /var/lib/cassandra/data)\n'
        jinja_variable = 'cassandra_yaml.data_file_directories'
        compiled_pattern = re.compile(option_pattern, re.MULTILINE)
        match = compiled_pattern.search(self.content)
        if match:
            replacement = match.group(0)
            replacement += '{%- if ' + jinja_variable + ' is defined -%}\n'
            replacement += 'data_file_directories:\n'
            replacement += '{%- for dir in ' + jinja_variable + ' %}\n'
            replacement += '    - {{ dir }}\n'
            replacement += '{%- endfor -%}\n'
            replacement += '{% endif %}\n'
            self.content = compiled_pattern.sub(replacement, self.content)

    def commitlog_directory(self):
        """
        # commitlog_directory: /var/lib/cassandra/commitlog
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (commitlog_directory: )(.*)\n',
            jinja_variable='cassandra_yaml.commitlog_directory')

    def disk_failure_policy(self):
        """
        disk_failure_policy: stop
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(disk_failure_policy: )(.*)\n',
            jinja_variable='cassandra_yaml.disk_failure_policy')

    def commit_failure_policy(self):
        """
        commit_failure_policy: stop
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(commit_failure_policy: )(.*)\n',
            jinja_variable='cassandra_yaml.commit_failure_policy')

    def key_cache_size_in_mb(self):
        """
        key_cache_size_in_mb:
        :return:
        """
        self.add_jinja_for_option_with_no_default_value(
            option_pattern=r'^(key_cache_size_in_mb:)\n',
            jinja_variable='cassandra_yaml.key_cache_size_in_mb')

    def key_cache_save_period(self):
        """
        key_cache_save_period: 14400
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(key_cache_save_period: )(.*)\n',
            jinja_variable='cassandra_yaml.key_cache_save_period')

    def key_cache_keys_to_save(self):
        """
        # key_cache_keys_to_save: 100
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (key_cache_keys_to_save: )(.*)\n',
            jinja_variable='cassandra_yaml.key_cache_keys_to_save')

    def row_cache_class_name(self):
        """
        # row_cache_class_name: org.apache.cassandra.cache.OHCProvider
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (row_cache_class_name: )(.*)\n',
            jinja_variable='cassandra_yaml.row_cache_class_name')

    def row_cache_size_in_mb(self):
        """
        row_cache_size_in_mb: 0
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(row_cache_size_in_mb: )(.*)\n',
            jinja_variable='cassandra_yaml.row_cache_size_in_mb')

    def row_cache_save_period(self):
        """
        row_cache_save_period: 0
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(row_cache_save_period: )(.*)\n',
            jinja_variable='cassandra_yaml.row_cache_save_period')

    def row_cache_keys_to_save(self):
        """
        # row_cache_keys_to_save: 100
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (row_cache_keys_to_save: )(.*)\n',
            jinja_variable='cassandra_yaml.row_cache_keys_to_save')

    def counter_cache_size_in_mb(self):
        """
        counter_cache_size_in_mb:
        :return:
        """
        self.add_jinja_for_option_with_no_default_value(
            option_pattern=r'^(counter_cache_size_in_mb:)\n',
            jinja_variable='cassandra_yaml.counter_cache_size_in_mb')

    def counter_cache_save_period(self):
        """
        counter_cache_save_period: 7200
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(counter_cache_save_period: )(.*)\n',
            jinja_variable='cassandra_yaml.counter_cache_save_period')

    def counter_cache_keys_to_save(self):
        """
        # counter_cache_keys_to_save: 100
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (counter_cache_keys_to_save: )(.*)\n',
            jinja_variable='cassandra_yaml.counter_cache_keys_to_save')

    def saved_caches_directory(self):
        """
        # saved_caches_directory: /var/lib/cassandra/saved_caches
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (saved_caches_directory: )(.*)\n',
            jinja_variable='cassandra_yaml.saved_caches_directory')

    def commitlog_sync(self):
        """
        commitlog_sync: periodic
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(commitlog_sync: )(.*)\n',
            jinja_variable='cassandra_yaml.commitlog_sync')

    def commitlog_sync_period_in_ms(self):
        """
        commitlog_sync_period_in_ms: 10000
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(commitlog_sync_period_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.commitlog_sync_period_in_ms')

    def commitlog_segment_size_in_mb(self):
        """
        commitlog_segment_size_in_mb: 32
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(commitlog_segment_size_in_mb: )(.*)\n',
            jinja_variable='cassandra_yaml.commitlog_segment_size_in_mb')

    def commitlog_compression(self):
        """
        #commitlog_compression:
        #   - class_name: LZ4Compressor
        #     parameters:
        #         -
        :return:
        """
        pass

    def seeds(self):
        """
        This method requires a custom implementation for the jinja produced because seeds is a comma separated list of
        addresses.
        - seeds: "127.0.0.1"
        :return:
        """
        option_pattern = r'^(\s*- seeds: ")(.*)(")\n'
        jinja_variable = 'cassandra_yaml.seeds'
        compiled_pattern = re.compile(option_pattern, re.MULTILINE)
        match = compiled_pattern.search(self.content)
        if match:
            replacement = match.group(1) + "{{ " + jinja_variable + " | default(['" + match.group(2) \
                          + "']) | join(',') }}" + match.group(3) + '\n'
            self.content = compiled_pattern.sub(replacement, self.content)

    def concurrent_reads(self):
        """
        concurrent_reads: 32
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(concurrent_reads: )(.*)\n',
            jinja_variable='cassandra_yaml.concurrent_reads')

    def concurrent_writes(self):
        """
        concurrent_writes: 32
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(concurrent_writes: )(.*)\n',
            jinja_variable='cassandra_yaml.concurrent_writes')

    def concurrent_counter_writes(self):
        """
        concurrent_counter_writes: 32
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(concurrent_counter_writes: )(.*)\n',
            jinja_variable='cassandra_yaml.concurrent_counter_writes')

    def concurrent_materialized_view_writes(self):
        """
        concurrent_materialized_view_writes: 32
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(concurrent_materialized_view_writes: )(.*)\n',
            jinja_variable='cassandra_yaml.concurrent_materialized_view_writes')

    def file_cache_size_in_mb(self):
        """
        # file_cache_size_in_mb: 512
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (file_cache_size_in_mb: )(.*)\n',
            jinja_variable='cassandra_yaml.file_cache_size_in_mb')

    def buffer_pool_use_heap_if_exhausted(self):
        """
        # buffer_pool_use_heap_if_exhausted: true
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (buffer_pool_use_heap_if_exhausted: )(.*)\n',
            jinja_variable='cassandra_yaml.buffer_pool_use_heap_if_exhausted')

    def disk_optimization_strategy(self):
        """
        # disk_optimization_strategy: ssd
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (disk_optimization_strategy: )(.*)\n',
            jinja_variable='cassandra_yaml.disk_optimization_strategy')

    def memtable_heap_space_in_mb(self):
        """
        # memtable_heap_space_in_mb: 2048
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (memtable_heap_space_in_mb: )(.*)\n',
            jinja_variable='cassandra_yaml.memtable_heap_space_in_mb')

    def memtable_offheap_space_in_mb(self):
        """
        # memtable_offheap_space_in_mb: 2048
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (memtable_offheap_space_in_mb: )(.*)\n',
            jinja_variable='cassandra_yaml.memtable_offheap_space_in_mb')

    def memtable_cleanup_threshold(self):
        """
        # memtable_cleanup_threshold: 0.11
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (memtable_cleanup_threshold: )(.*)\n',
            jinja_variable='cassandra_yaml.memtable_cleanup_threshold')

    def memtable_allocation_type(self):
        """
        memtable_allocation_type: heap_buffers
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(memtable_allocation_type: )(.*)\n',
            jinja_variable='cassandra_yaml.memtable_allocation_type')

    def commitlog_total_space_in_mb(self):
        """
        # commitlog_total_space_in_mb: 8192
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (commitlog_total_space_in_mb: )(.*)\n',
            jinja_variable='cassandra_yaml.commitlog_total_space_in_mb')

    def memtable_flush_writers(self):
        """
        #memtable_flush_writers: 8
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^#(memtable_flush_writers: )(.*)\n',
            jinja_variable='cassandra_yaml.memtable_flush_writers')

    def index_summary_capacity_in_mb(self):
        """
        index_summary_capacity_in_mb:
        :return:
        """
        self.add_jinja_for_option_with_no_default_value(
            option_pattern=r'^(index_summary_capacity_in_mb:)\n',
            jinja_variable='cassandra_yaml.index_summary_capacity_in_mb')

    def index_summary_resize_interval_in_minutes(self):
        """
        index_summary_resize_interval_in_minutes: 60
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(index_summary_resize_interval_in_minutes: )(.*)\n',
            jinja_variable='cassandra_yaml.index_summary_resize_interval_in_minutes')

    def trickle_fsync(self):
        """
        trickle_fsync: false
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(trickle_fsync: )(.*)\n',
            jinja_variable='cassandra_yaml.trickle_fsync')

    def trickle_fsync_interval_in_kb(self):
        """
        trickle_fsync_interval_in_kb: 10240
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(trickle_fsync_interval_in_kb: )(.*)\n',
            jinja_variable='cassandra_yaml.trickle_fsync_interval_in_kb')

    def storage_port(self):
        """
        storage_port: 7000
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(storage_port: )(.*)\n',
            jinja_variable='cassandra_yaml.storage_port')

    def ssl_storage_port(self):
        """
        ssl_storage_port: 7001
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(ssl_storage_port: )(.*)\n',
            jinja_variable='cassandra_yaml.ssl_storage_port')

    def listen_address(self):
        """
        listen_address: localhost
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(listen_address: )(.*)\n',
            jinja_variable='cassandra_yaml.listen_address')

    def listen_interface(self):
        """
        # listen_interface: eth0
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (listen_interface: )(.*)\n',
            jinja_variable='cassandra_yaml.listen_interface')

    def listen_interface_prefer_ipv6(self):
        """
        # listen_interface_prefer_ipv6: false
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (listen_interface_prefer_ipv6: )(.*)\n',
            jinja_variable='cassandra_yaml.listen_interface_prefer_ipv6')

    def broadcast_address(self):
        """
        # broadcast_address: 1.2.3.4
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (broadcast_address: )(.*)\n',
            jinja_variable='cassandra_yaml.broadcast_address')

    def listen_on_broadcast_address(self):
        """
        # listen_on_broadcast_address: false
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (listen_on_broadcast_address: )(.*)\n',
            jinja_variable='cassandra_yaml.listen_on_broadcast_address')

    def internode_authenticator(self):
        """
        # internode_authenticator: org.apache.cassandra.auth.AllowAllInternodeAuthenticator
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (internode_authenticator: )(.*)\n',
            jinja_variable='cassandra_yaml.internode_authenticator')

    def start_native_transport(self):
        """
        start_native_transport: true
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(start_native_transport: )(.*)\n',
            jinja_variable='cassandra_yaml.start_native_transport')

    def native_transport_port(self):
        """
        native_transport_port: 9042
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(native_transport_port: )(.*)\n',
            jinja_variable='cassandra_yaml.native_transport_port')

    def native_transport_port_ssl(self):
        """
        # native_transport_port_ssl: 9142
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (native_transport_port_ssl: )(.*)\n',
            jinja_variable='cassandra_yaml.native_transport_port_ssl')

    def native_transport_max_threads(self):
        """
        # native_transport_max_threads: 128
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (native_transport_max_threads: )(.*)\n',
            jinja_variable='cassandra_yaml.native_transport_max_threads')

    def native_transport_max_frame_size_in_mb(self):
        """
        # native_transport_max_frame_size_in_mb: 256
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (native_transport_max_frame_size_in_mb: )(.*)\n',
            jinja_variable='cassandra_yaml.native_transport_max_frame_size_in_mb')

    def native_transport_max_concurrent_connections(self):
        """
        # native_transport_max_concurrent_connections: -1
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (native_transport_max_concurrent_connections: )(.*)\n',
            jinja_variable='cassandra_yaml.native_transport_max_concurrent_connections')

    def native_transport_max_concurrent_connections_per_ip(self):
        """
        # native_transport_max_concurrent_connections_per_ip: -1
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (native_transport_max_concurrent_connections_per_ip: )(.*)\n',
            jinja_variable='cassandra_yaml.native_transport_max_concurrent_connections_per_ip')

    def start_rpc(self):
        """
        start_rpc: false
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(start_rpc: )(.*)\n',
            jinja_variable='cassandra_yaml.start_rpc')

    def rpc_address(self):
        """
        rpc_address: localhost
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(rpc_address: )(.*)\n',
            jinja_variable='cassandra_yaml.rpc_address')

    def rpc_interface(self):
        """
        # rpc_interface: eth1
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (rpc_interface: )(.*)\n',
            jinja_variable='cassandra_yaml.rpc_interface')

    def rpc_interface_prefer_ipv6(self):
        """
        # rpc_interface_prefer_ipv6: false
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (rpc_interface_prefer_ipv6: )(.*)\n',
            jinja_variable='cassandra_yaml.rpc_interface_prefer_ipv6')

    def rpc_port(self):
        """
        rpc_port: 9160
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(rpc_port: )(.*)\n',
            jinja_variable='cassandra_yaml.rpc_port')

    def broadcast_rpc_address(self):
        """
        # broadcast_rpc_address: 1.2.3.4
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (broadcast_rpc_address: )(.*)\n',
            jinja_variable='cassandra_yaml.broadcast_rpc_address')

    def rpc_keepalive(self):
        """
        rpc_keepalive: true
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(rpc_keepalive: )(.*)\n',
            jinja_variable='cassandra_yaml.rpc_keepalive')

    def rpc_server_type(self):
        """
        rpc_server_type: sync
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(rpc_server_type: )(.*)\n',
            jinja_variable='cassandra_yaml.rpc_server_type')

    def rpc_min_threads(self):
        """
        # rpc_min_threads: 16
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (rpc_min_threads: )(.*)\n',
            jinja_variable='cassandra_yaml.rpc_min_threads')

    def rpc_max_threads(self):
        """
        # rpc_max_threads: 2048
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (rpc_max_threads: )(.*)\n',
            jinja_variable='cassandra_yaml.rpc_max_threads')

    def rpc_send_buff_size_in_bytes(self):
        """
        # rpc_send_buff_size_in_bytes:
        :return:
        """
        self.add_jinja_for_commented_option_with_no_default_value(
            option_pattern=r'^# (rpc_send_buff_size_in_bytes:)\n',
            jinja_variable='cassandra_yaml.rpc_send_buff_size_in_bytes')

    def rpc_recv_buff_size_in_bytes(self):
        """
        # rpc_recv_buff_size_in_bytes:
        :return:
        """
        self.add_jinja_for_commented_option_with_no_default_value(
            option_pattern=r'^# (rpc_recv_buff_size_in_bytes:)\n',
            jinja_variable='cassandra_yaml.pc_recv_buff_size_in_bytes')

    def internode_send_buff_size_in_bytes(self):
        """
        # internode_send_buff_size_in_bytes:
        :return:
        """
        self.add_jinja_for_commented_option_with_no_default_value(
            option_pattern=r'^# (internode_send_buff_size_in_bytes:)\n',
            jinja_variable='cassandra_yaml.internode_send_buff_size_in_bytes')

    def internode_recv_buff_size_in_bytes(self):
        """
        # internode_recv_buff_size_in_bytes:
        :return:
        """
        self.add_jinja_for_commented_option_with_no_default_value(
            option_pattern=r'^# (internode_recv_buff_size_in_bytes:)\n',
            jinja_variable='cassandra_yaml.internode_recv_buff_size_in_bytes')

    def thrift_framed_transport_size_in_mb(self):
        """
        thrift_framed_transport_size_in_mb: 15
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(thrift_framed_transport_size_in_mb: )(.*)\n',
            jinja_variable='cassandra_yaml.thrift_framed_transport_size_in_mb')

    def incremental_backups(self):
        """
        incremental_backups: false
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(incremental_backups: )(.*)\n',
            jinja_variable='cassandra_yaml.incremental_backups')

    def snapshot_before_compaction(self):
        """
        snapshot_before_compaction: false
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(snapshot_before_compaction: )(.*)\n',
            jinja_variable='cassandra_yaml.snapshot_before_compaction')

    def auto_snapshot(self):
        """
        auto_snapshot: true
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(auto_snapshot: )(.*)\n',
            jinja_variable='cassandra_yaml.auto_snapshot')

    def tombstone_warn_threshold(self):
        """
        tombstone_warn_threshold: 1000
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(tombstone_warn_threshold: )(.*)\n',
            jinja_variable='cassandra_yaml.tombstone_warn_threshold')

    def tombstone_failure_threshold(self):
        """
        tombstone_failure_threshold: 100000
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(tombstone_failure_threshold: )(.*)\n',
            jinja_variable='cassandra_yaml.tombstone_failure_threshold')

    def column_index_size_in_kb(self):
        """
        column_index_size_in_kb: 64
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(column_index_size_in_kb: )(.*)\n',
            jinja_variable='cassandra_yaml.column_index_size_in_kb')

    def batch_size_warn_threshold_in_kb(self):
        """
        batch_size_warn_threshold_in_kb: 5
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(batch_size_warn_threshold_in_kb: )(.*)\n',
            jinja_variable='cassandra_yaml.batch_size_warn_threshold_in_kb')

    def batch_size_fail_threshold_in_kb(self):
        """
        batch_size_fail_threshold_in_kb: 50
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(batch_size_fail_threshold_in_kb: )(.*)\n',
            jinja_variable='cassandra_yaml.batch_size_fail_threshold_in_kb')

    def unlogged_batch_across_partitions_warn_threshold(self):
        """
        unlogged_batch_across_partitions_warn_threshold: 10
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(unlogged_batch_across_partitions_warn_threshold: )(.*)\n',
            jinja_variable='cassandra_yaml.unlogged_batch_across_partitions_warn_threshold')

    def concurrent_compactors(self):
        """
        #concurrent_compactors: 1
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^#(concurrent_compactors: )(.*)\n',
            jinja_variable='cassandra_yaml.concurrent_compactors')

    def compaction_throughput_mb_per_sec(self):
        """
        compaction_throughput_mb_per_sec: 16
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(compaction_throughput_mb_per_sec: )(.*)\n',
            jinja_variable='cassandra_yaml.compaction_throughput_mb_per_sec')

    def compaction_large_partition_warning_threshold_mb(self):
        """
        compaction_large_partition_warning_threshold_mb: 100
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(compaction_large_partition_warning_threshold_mb: )(.*)\n',
            jinja_variable='cassandra_yaml.compaction_large_partition_warning_threshold_mb')

    def sstable_preemptive_open_interval_in_mb(self):
        """
        sstable_preemptive_open_interval_in_mb: 50
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(sstable_preemptive_open_interval_in_mb: )(.*)\n',
            jinja_variable='cassandra_yaml.sstable_preemptive_open_interval_in_mb')

    def stream_throughput_outbound_megabits_per_sec(self):
        """
        # stream_throughput_outbound_megabits_per_sec: 200
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (stream_throughput_outbound_megabits_per_sec: )(.*)\n',
            jinja_variable='cassandra_yaml.stream_throughput_outbound_megabits_per_sec')

    def inter_dc_stream_throughput_outbound_megabits_per_sec(self):
        """
        # inter_dc_stream_throughput_outbound_megabits_per_sec: 200
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (inter_dc_stream_throughput_outbound_megabits_per_sec: )(.*)\n',
            jinja_variable='cassandra_yaml.inter_dc_stream_throughput_outbound_megabits_per_sec')

    def read_request_timeout_in_ms(self):
        """
        read_request_timeout_in_ms: 5000
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(read_request_timeout_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.read_request_timeout_in_ms')

    def range_request_timeout_in_ms(self):
        """
        range_request_timeout_in_ms: 10000
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(range_request_timeout_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.range_request_timeout_in_ms')

    def write_request_timeout_in_ms(self):
        """
        write_request_timeout_in_ms: 2000
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(write_request_timeout_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.write_request_timeout_in_ms')

    def counter_write_request_timeout_in_ms(self):
        """
        counter_write_request_timeout_in_ms: 5000
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(counter_write_request_timeout_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.counter_write_request_timeout_in_ms')

    def cas_contention_timeout_in_ms(self):
        """
        cas_contention_timeout_in_ms: 1000
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(cas_contention_timeout_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.cas_contention_timeout_in_ms')

    def truncate_request_timeout_in_ms(self):
        """
        truncate_request_timeout_in_ms: 60000
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(truncate_request_timeout_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.truncate_request_timeout_in_ms')

    def request_timeout_in_ms(self):
        """
        request_timeout_in_ms: 10000
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(request_timeout_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.request_timeout_in_ms')

    def cross_node_timeout(self):
        """
        cross_node_timeout: false
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(cross_node_timeout: )(.*)\n',
            jinja_variable='cassandra_yaml.cross_node_timeout')

    def streaming_socket_timeout_in_ms(self):
        """
        # streaming_socket_timeout_in_ms: 86400000
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (streaming_socket_timeout_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.streaming_socket_timeout_in_ms')

    def phi_convict_threshold(self):
        """
        # phi_convict_threshold: 8
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (phi_convict_threshold: )(.*)\n',
            jinja_variable='cassandra_yaml.phi_convict_threshold')

    def endpoint_snitch(self):
        """
        endpoint_snitch: SimpleSnitch
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(endpoint_snitch: )(.*)\n',
            jinja_variable='cassandra_yaml.endpoint_snitch')

    def dynamic_snitch_update_interval_in_ms(self):
        """
        dynamic_snitch_update_interval_in_ms: 100
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(dynamic_snitch_update_interval_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.dynamic_snitch_update_interval_in_ms')

    def dynamic_snitch_reset_interval_in_ms(self):
        """
        dynamic_snitch_reset_interval_in_ms: 600000
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(dynamic_snitch_reset_interval_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.dynamic_snitch_reset_interval_in_ms')

    def dynamic_snitch_badness_threshold(self):
        """
        dynamic_snitch_badness_threshold: 0.1
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(dynamic_snitch_badness_threshold: )(.*)\n',
            jinja_variable='cassandra_yaml.dynamic_snitch_badness_threshold')

    def request_scheduler(self):
        """
        request_scheduler: org.apache.cassandra.scheduler.NoScheduler
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(request_scheduler: )(.*)\n',
            jinja_variable='cassandra_yaml.request_scheduler')

    def request_scheduler_options(self):
        """
        # request_scheduler_options:
        #    throttle_limit: 80
        #    default_weight: 5
        #    weights:
        #      Keyspace1: 1
        #      Keyspace2: 5
        :return:
        """
        pass

    def request_scheduler_id(self):
        """
        # request_scheduler_id: keyspace
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (request_scheduler_id: )(.*)\n',
            jinja_variable='cassandra_yaml.request_scheduler_id')

    def server_encryption_options(self):
        """
        server_encryption_options:
            internode_encryption: none
            keystore: conf/.keystore
            keystore_password: cassandra
            truststore: conf/.truststore
            truststore_password: cassandra
            # More advanced defaults below:
            # protocol: TLS
            # algorithm: SunX509
            # store_type: JKS
            # cipher_suites: [TLS_RSA_WITH_AES_128_CBC_SHA, ... ,TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA]
            # require_client_auth: false
        :return:
        """
        pass

    def client_encryption_options(self):
        """
         client_encryption_options:
            enabled: false
            # If enabled and optional is set to true encrypted and unencrypted connections are handled.
            optional: false
            keystore: conf/.keystore
            keystore_password: cassandra
            # require_client_auth: false
            # Set trustore and truststore_password if require_client_auth is true
            # truststore: conf/.truststore
            # truststore_password: cassandra
            # More advanced defaults below:
            # protocol: TLS
            # algorithm: SunX509
            # store_type: JKS
            # cipher_suites: [TLS_RSA_WITH_AES_128_CBC_SHA, ... ,TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA]
        :return:
        """
        pass

    def internode_compression(self):
        """
        internode_compression: all
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(internode_compression: )(.*)\n',
            jinja_variable='cassandra_yaml.internode_compression')

    def inter_dc_tcp_nodelay(self):
        """
        inter_dc_tcp_nodelay: false
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(inter_dc_tcp_nodelay: )(.*)\n',
            jinja_variable='cassandra_yaml.inter_dc_tcp_nodelay')

    def tracetype_query_ttl(self):
        """
        tracetype_query_ttl: 86400
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(tracetype_query_ttl: )(.*)\n',
            jinja_variable='cassandra_yaml.tracetype_query_ttl')

    def tracetype_repair_ttl(self):
        """
        tracetype_repair_ttl: 604800
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(tracetype_repair_ttl: )(.*)\n',
            jinja_variable='cassandra_yaml.tracetype_repair_ttl')

    def gc_log_threshold_in_ms(self):
        """
        # gc_log_threshold_in_ms: 200
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (gc_log_threshold_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.gc_log_threshold_in_ms')

    def gc_warn_threshold_in_ms(self):
        """
        gc_warn_threshold_in_ms: 1000
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(gc_warn_threshold_in_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.gc_warn_threshold_in_ms')

    def enable_user_defined_functions(self):
        """
        enable_user_defined_functions: false
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(enable_user_defined_functions: )(.*)\n',
            jinja_variable='cassandra_yaml.enable_user_defined_functions')

    def enable_scripted_user_defined_functions(self):
        """
        enable_scripted_user_defined_functions: false
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(enable_scripted_user_defined_functions: )(.*)\n',
            jinja_variable='cassandra_yaml.enable_scripted_user_defined_functions')

    def windows_timer_interval(self):
        """
        windows_timer_interval: 1
        :return:
        """
        self.add_jinja_for_option_with_default_value(
            option_pattern=r'^(windows_timer_interval: )(.*)\n',
            jinja_variable='cassandra_yaml.windows_timer_interval')

    def max_value_size_in_mb(self):
        """
        # max_value_size_in_mb: 256
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (max_value_size_in_mb: )(.*)\n',
            jinja_variable='cassandra_yaml.max_value_size_in_mb')

    def otc_coalescing_strategy(self):
        """
        # otc_coalescing_strategy: TIMEHORIZON
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (otc_coalescing_strategy: )(.*)\n',
            jinja_variable='cassandra_yaml.otc_coalescing_strategy')

    def otc_coalescing_window_us(self):
        """
        # otc_coalescing_window_us: 200
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (otc_coalescing_window_us: )(.*)\n',
            jinja_variable='cassandra_yaml.otc_coalescing_window_us')

    def otc_coalescing_enough_coalesced_messages(self):
        """
        # otc_coalescing_enough_coalesced_messages: 8
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (otc_coalescing_enough_coalesced_messages: )(.*)\n',
            jinja_variable='cassandra_yaml.otc_coalescing_enough_coalesced_messages')

    def otc_backlog_expiration_interval_ms(self):
        """
        # otc_backlog_expiration_interval_ms: 200
        :return:
        """
        self.add_jinja_for_commented_option_with_default_value(
            option_pattern=r'^# (otc_backlog_expiration_interval_ms: )(.*)\n',
            jinja_variable='cassandra_yaml.otc_backlog_expiration_interval_ms')
