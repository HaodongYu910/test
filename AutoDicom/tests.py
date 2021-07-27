# from django.test import TestCase
#
# # Create your tests here.
#
#
# groups:
#     - name: example
#       rules:
#       - alert: cpu使用率大于80%
#         expr: rate(process_cpu_seconds_total{job=~"biomind_node-exporter"}[1m]) * 100 > 80
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}组件的cpu使用率超过80%"
#       - alert:  cpu使用率大于90%
#         expr: rate(process_cpu_seconds_total{job=~"biomind_node-exporter"}[1m]) * 100 > 90
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}组件的cpu使用率超过90%"
#       - alert: scheduler的cpu使用率大于80%
#         expr: rate(process_cpu_seconds_total{job=~"biomind_cadvisor"}[1m]) * 100 > 80
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}组件的cpu使用率超过80%"
#       - alert:  scheduler的cpu使用率大于90%
#         expr: rate(process_cpu_seconds_total{job=~"biomind_cadvisor"}[1m]) * 100 > 90
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}组件的cpu使用率超过90%"
#       - alert: controller-manager的cpu使用率大于80%
#         expr: rate(process_cpu_seconds_total{job=~"kubernetes-controller-manager"}[1m]) * 100 > 80
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}组件的cpu使用率超过80%"
#       - alert:  controller-manager的cpu使用率大于90%
#         expr: rate(process_cpu_seconds_total{job=~"kubernetes-controller-manager"}[1m]) * 100 > 0
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}组件的cpu使用率超过90%"
#       - alert: apiserver的cpu使用率大于80%
#         expr: rate(process_cpu_seconds_total{job=~"kubernetes-apiserver"}[1m]) * 100 > 80
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}组件的cpu使用率超过80%"
#       - alert:  apiserver的cpu使用率大于90%
#         expr: rate(process_cpu_seconds_total{job=~"kubernetes-apiserver"}[1m]) * 100 > 90
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}组件的cpu使用率超过90%"
#       - alert: etcd的cpu使用率大于80%
#         expr: rate(process_cpu_seconds_total{job=~"kubernetes-etcd"}[1m]) * 100 > 80
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}组件的cpu使用率超过80%"
#       - alert:  etcd的cpu使用率大于90%
#         expr: rate(process_cpu_seconds_total{job=~"kubernetes-etcd"}[1m]) * 100 > 90
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}组件的cpu使用率超过90%"
#       - alert: kube-state-metrics的cpu使用率大于80%
#         expr: rate(process_cpu_seconds_total{k8s_app=~"kube-state-metrics"}[1m]) * 100 > 80
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.k8s_app}}组件的cpu使用率超过80%"
#           value: "{{ $value }}%"
#           threshold: "80%"
#       - alert: kube-state-metrics的cpu使用率大于90%
#         expr: rate(process_cpu_seconds_total{k8s_app=~"kube-state-metrics"}[1m]) * 100 > 0
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.k8s_app}}组件的cpu使用率超过90%"
#           value: "{{ $value }}%"
#           threshold: "90%"
#       - alert: coredns的cpu使用率大于80%
#         expr: rate(process_cpu_seconds_total{k8s_app=~"kube-dns"}[1m]) * 100 > 80
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.k8s_app}}组件的cpu使用率超过80%"
#           value: "{{ $value }}%"
#           threshold: "80%"
#       - alert: coredns的cpu使用率大于90%
#         expr: rate(process_cpu_seconds_total{k8s_app=~"kube-dns"}[1m]) * 100 > 90
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.k8s_app}}组件的cpu使用率超过90%"
#           value: "{{ $value }}%"
#           threshold: "90%"
#       - alert: kube-proxy打开句柄数>600
#         expr: process_open_fds{job=~"biomind_node-exporter"}  > 600
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}打开句柄数>600"
#           value: "{{ $value }}"
#       - alert: kube-proxy打开句柄数>1000
#         expr: process_open_fds{job=~"biomind_node-exporter"}  > 1000
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}打开句柄数>1000"
#           value: "{{ $value }}"
#       - alert: biomind_cadvisor打开句柄数>600
#         expr: process_open_fds{job=~"biomind_cadvisor"}  > 600
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}打开句柄数>600"
#           value: "{{ $value }}"
#       - alert: biomind_cadvisor打开句柄数>1000
#         expr: process_open_fds{job=~"biomind_cadvisor"}  > 1000
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}打开句柄数>1000"
#           value: "{{ $value }}"
#       - alert: kubernetes-controller-manager打开句柄数>600
#         expr: process_open_fds{job=~"kubernetes-controller-manager"}  > 600
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}打开句柄数>600"
#           value: "{{ $value }}"
#       - alert: kubernetes-controller-manager打开句柄数>1000
#         expr: process_open_fds{job=~"kubernetes-controller-manager"}  > 1000
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}打开句柄数>1000"
#           value: "{{ $value }}"
#       - alert: kubernetes-apiserver打开句柄数>600
#         expr: process_open_fds{job=~"kubernetes-apiserver"}  > 600
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}打开句柄数>600"
#           value: "{{ $value }}"
#       - alert: kubernetes-apiserver打开句柄数>1000
#         expr: process_open_fds{job=~"kubernetes-apiserver"}  > 1000
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}打开句柄数>1000"
#           value: "{{ $value }}"
#       - alert: kubernetes-etcd打开句柄数>600
#         expr: process_open_fds{job=~"kubernetes-etcd"}  > 600
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}打开句柄数>600"
#           value: "{{ $value }}"
#       - alert: kubernetes-etcd打开句柄数>1000
#         expr: process_open_fds{job=~"kubernetes-etcd"}  > 1000
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           description: "{{$labels.instance}}的{{$labels.job}}打开句柄数>1000"
#           value: "{{ $value }}"
#       - alert: coredns
#         expr: process_open_fds{k8s_app=~"kube-dns"}  > 600
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "插件{{$labels.k8s_app}}({{$labels.instance}}): 打开句柄数超过600"
#           value: "{{ $value }}"
#       - alert: coredns
#         expr: process_open_fds{k8s_app=~"kube-dns"}  > 1000
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           description: "插件{{$labels.k8s_app}}({{$labels.instance}}): 打开句柄数超过1000"
#           value: "{{ $value }}"
#       - alert: kube-proxy
#         expr: process_virtual_memory_bytes{job=~"biomind_node-exporter"}  > 2000000000
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "组件{{$labels.job}}({{$labels.instance}}): 使用虚拟内存超过2G"
#           value: "{{ $value }}"
#       - alert: scheduler
#         expr: process_virtual_memory_bytes{job=~"biomind_cadvisor"}  > 2000000000
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "组件{{$labels.job}}({{$labels.instance}}): 使用虚拟内存超过2G"
#           value: "{{ $value }}"
#       - alert: kubernetes-controller-manager
#         expr: process_virtual_memory_bytes{job=~"kubernetes-controller-manager"}  > 2000000000
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "组件{{$labels.job}}({{$labels.instance}}): 使用虚拟内存超过2G"
#           value: "{{ $value }}"
#       - alert: kubernetes-apiserver
#         expr: process_virtual_memory_bytes{job=~"kubernetes-apiserver"}  > 2000000000
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "组件{{$labels.job}}({{$labels.instance}}): 使用虚拟内存超过2G"
#           value: "{{ $value }}"
#       - alert: kubernetes-etcd
#         expr: process_virtual_memory_bytes{job=~"kubernetes-etcd"}  > 2000000000
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "组件{{$labels.job}}({{$labels.instance}}): 使用虚拟内存超过2G"
#           value: "{{ $value }}"
#       - alert: kube-dns
#         expr: process_virtual_memory_bytes{k8s_app=~"kube-dns"}  > 2000000000
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "插件{{$labels.k8s_app}}({{$labels.instance}}): 使用虚拟内存超过2G"
#           value: "{{ $value }}"
#       - alert: HttpRequestsAvg
#         expr: sum(rate(rest_client_requests_total{job=~"biomind_node-exporter|kubernetes-kubelet|biomind_cadvisor|kubernetes-control-manager|kubernetes-apiservers"}[1m]))  > 1000
#         for: 2s
#         labels:
#           team: admin
#         annotations:
#           description: "组件{{$labels.job}}({{$labels.instance}}): TPS超过1000"
#           value: "{{ $value }}"
#           threshold: "1000"
#       - alert: Pod_restarts
#         expr: kube_pod_container_status_restarts_total{namespace=~"kube-system|default|monitor-sa"} > 0
#         for: 2s
#         labels:
#           severity: warnning
#         annotations:
#           description: "在{{$labels.namespace}}名称空间下发现{{$labels.pod}}这个pod下的容器{{$labels.container}}被重启,这个监控指标是由{{$labels.instance}}采集的"
#           value: "{{ $value }}"
#           threshold: "0"
#       - alert: Pod_waiting
#         expr: kube_pod_container_status_waiting_reason{namespace=~"kube-system|default"} == 1
#         for: 2s
#         labels:
#           team: admin
#         annotations:
#           description: "空间{{$labels.namespace}}({{$labels.instance}}): 发现{{$labels.pod}}下的{{$labels.container}}启动异常等待中"
#           value: "{{ $value }}"
#           threshold: "1"
#       - alert: Pod_terminated
#         expr: kube_pod_container_status_terminated_reason{namespace=~"kube-system|default|monitor-sa"} == 1
#         for: 2s
#         labels:
#           team: admin
#         annotations:
#           description: "空间{{$labels.namespace}}({{$labels.instance}}): 发现{{$labels.pod}}下的{{$labels.container}}被删除"
#           value: "{{ $value }}"
#           threshold: "1"
#       - alert: Etcd_leader
#         expr: etcd_server_has_leader{job="kubernetes-etcd"} == 0
#         for: 2s
#         labels:
#           team: admin
#         annotations:
#           description: "组件{{$labels.job}}({{$labels.instance}}): 当前没有leader"
#           value: "{{ $value }}"
#           threshold: "0"
#       - alert: Etcd_leader_changes
#         expr: rate(etcd_server_leader_changes_seen_total{job="kubernetes-etcd"}[1m]) > 0
#         for: 2s
#         labels:
#           team: admin
#         annotations:
#           description: "组件{{$labels.job}}({{$labels.instance}}): 当前leader已发生改变"
#           value: "{{ $value }}"
#           threshold: "0"
#       - alert: Etcd_failed
#         expr: rate(etcd_server_proposals_failed_total{job="kubernetes-etcd"}[1m]) > 0
#         for: 2s
#         labels:
#           team: admin
#         annotations:
#           description: "组件{{$labels.job}}({{$labels.instance}}): 服务失败"
#           value: "{{ $value }}"
#           threshold: "0"
#       - alert: Etcd_db_total_size
#         expr: etcd_debugging_mvcc_db_total_size_in_bytes{job="kubernetes-etcd"} > 10000000000
#         for: 2s
#         labels:
#           team: admin
#         annotations:
#           description: "组件{{$labels.job}}({{$labels.instance}})：db空间超过10G"
#           value: "{{ $value }}"
#           threshold: "10G"
#       - alert: Endpoint_ready
#         expr: kube_endpoint_address_not_ready{namespace=~"kube-system|default"} == 1
#         for: 2s
#         labels:
#           team: admin
#         annotations:
#           description: "空间{{$labels.namespace}}({{$labels.instance}}): 发现{{$labels.endpoint}}不可用"
#           value: "{{ $value }}"
#           threshold: "1"
#     - name: 物理节点状态-监控告警
#       rules:
#       - alert: 物理节点cpu使用率
#         expr: 100-avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) by(instance)*100 > 90
#         for: 2s
#         labels:
#           severity: ccritical
#         annotations:
#           summary: "{{ $labels.instance }}cpu使用率过高"
#           description: "{{ $labels.instance }}的cpu使用率超过90%,当前使用率[{{ $value }}],需要排查处理"
#       - alert: 物理节点内存使用率
#         expr: (node_memory_MemTotal_bytes - (node_memory_MemFree_bytes + node_memory_Buffers_bytes + node_memory_Cached_bytes)) / node_memory_MemTotal_bytes * 100 > 90
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           summary: "{{ $labels.instance }}内存使用率过高"
#           description: "{{ $labels.instance }}的内存使用率超过90%,当前使用率[{{ $value }}],需要排查处理"
#       - alert: InstanceDown
#         expr: up == 0
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           summary: "{{ $labels.instance }}: 服务器宕机"
#           description: "{{ $labels.instance }}: 服务器延时超过2分钟"
#       - alert: 物理节点磁盘的IO性能
#         expr: 100-(avg(irate(node_disk_io_time_seconds_total[1m])) by(instance)* 100) < 60
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           summary: "{{$labels.mountpoint}} 流入磁盘IO使用率过高！"
#           description: "{{$labels.mountpoint }} 流入磁盘IO大于60%(目前使用:{{$value}})"
#       - alert: 入网流量带宽
#         expr: ((sum(rate (node_network_receive_bytes_total{device!~'tap.*|veth.*|br.*|docker.*|virbr*|lo*'}[5m])) by (instance)) / 100) > 102400
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           summary: "{{$labels.mountpoint}} 流入网络带宽过高！"
#           description: "{{$labels.mountpoint }}流入网络带宽持续5分钟高于100M. RX带宽使用率{{$value}}"
#       - alert: 出网流量带宽
#         expr: ((sum(rate (node_network_transmit_bytes_total{device!~'tap.*|veth.*|br.*|docker.*|virbr*|lo*'}[5m])) by (instance)) / 100) > 102400
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           summary: "{{$labels.mountpoint}} 流出网络带宽过高！"
#           description: "{{$labels.mountpoint }}流出网络带宽持续5分钟高于100M. RX带宽使用率{{$value}}"
#       - alert: TCP会话
#         expr: node_netstat_Tcp_CurrEstab > 1000
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           summary: "{{$labels.mountpoint}} TCP_ESTABLISHED过高！"
#           description: "{{$labels.mountpoint }} TCP_ESTABLISHED大于1000%(目前使用:{{$value}}%)"
#       - alert: 磁盘容量
#         expr: 100-(node_filesystem_free_bytes{fstype=~"ext4|xfs"}/node_filesystem_size_bytes {fstype=~"ext4|xfs"}*100) > 80
#         for: 2s
#         labels:
#           severity: critical
#         annotations:
#           summary: "{{$labels.mountpoint}} 磁盘分区使用率过高！"
#           description: "{{$labels.mountpoint }} 磁盘分区使用大于80%(目前使用:{{$value}}%)"
