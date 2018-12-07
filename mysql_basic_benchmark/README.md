# Enviroment

Host Hardware

* CPU:    2860QM 4C8T
* RAM:    12G
* DISK:   two SATA SSD
* HOST OS:    Ubuntu 16.04.5
* sysbench: 1.0.15
* use [percona benchmark script]( https://www.percona.com/blog/2018/03/05/tpcc-like-workload-sysbench-1-0/) 10 scales,10tables,64 threads

Use Virtualbox create virtual machine

* CPU:  2
* RAM:  4G
* DISK: 10G for OS,20G on second disk for mysql data,and preallocated
* OS:   Ubuntu 18.04.1
* Mariadb: 10.3.11




# TESTS


## T1 default

use ubuntu default config,use mariadb default config.use ext4 for mysql data.no tunning anything

### result

    SQL statistics:
    queries performed:
        read:                            126822
        write:                           131226
        other:                           19426
        total:                           277474
    transactions:                        9649   (31.98 per sec.)
    queries:                             277474 (919.67 per sec.)
    ignored errors:                      43     (0.14 per sec.)
    reconnects:                          0      (0.00 per sec.)

    General statistics:
        total time:                          301.7092s
        total number of events:              9649

    Latency (ms):
            min:                                    8.30
            avg:                                 1995.94
            max:                                17905.03
            95th percentile:                     6135.91
            sum:                             19258817.82

    Threads fairness:
        events (avg/stddev):           150.7656/11.59
        execution time (avg/stddev):   300.9190/0.45

## T2 optimized with percona

kernel

    vm.swappiness = 1 #ubuntu 18.04 install default no swap

disk for mysql data

    format with XFS
    mount with default options

change disk scheduler

    sudo echo noop > /sys/block/sdb/queue/scheduler

mysql config

    innodb_file_per_table=ON
    innodb_stats_on_metadata = OFF
    innodb_buffer_pool_instances = 8 # (or 1 if innodb_buffer_pool_size < 1GB)
    query_cache_type = 0
    query_cache_size = 0 # (disabling mutex)

    innodb_buffer_pool_size = 2560M # (adjust value here, 50%-70% of total RAM)
    innodb_log_file_size = 256M
    innodb_flush_log_at_trx_commit = 1 # may change to 2 or 0
    innodb_flush_method = O_DIRECT #mariadb default is O_DIRECT

### result

    SQL statistics:
    queries performed:
        read:                            694080
        write:                           719858
        other:                           106950
        total:                           1520888
    transactions:                        53411  (177.80 per sec.)
    queries:                             1520888 (5062.91 per sec.)
    ignored errors:                      260    (0.87 per sec.)
    reconnects:                          0      (0.00 per sec.)

    General statistics:
        total time:                          300.3966s
        total number of events:              53411

    Latency (ms):
            min:                                    1.62
            avg:                                  359.68
            max:                                 8907.32
            95th percentile:                      909.80
            sum:                             19210862.29

    Threads fairness:
        events (avg/stddev):           834.5469/26.60
        execution time (avg/stddev):   300.1697/0.10


## T3 same as T2 but disk format is ext4

### result

    SQL statistics:
    queries performed:
        read:                            691477
        write:                           716789
        other:                           106926
        total:                           1515192
    transactions:                        53399  (177.76 per sec.)
    queries:                             1515192 (5043.97 per sec.)
    ignored errors:                      209    (0.70 per sec.)
    reconnects:                          0      (0.00 per sec.)

    General statistics:
        total time:                          300.3952s
        total number of events:              53399

    Latency (ms):
            min:                                    1.18
            avg:                                  359.74
            max:                                 7360.77
            95th percentile:                      926.33
            sum:                             19209663.56

    Threads fairness:
        events (avg/stddev):           834.3594/22.23
        execution time (avg/stddev):   300.1510/0.09


## T4 same as T2 but change mariadb to mysql 5.7.24

### result

    SQL statistics:
    queries performed:
        read:                            776074
        write:                           805991
        other:                           119682
        total:                           1701747
    transactions:                        59777  (198.99 per sec.)
    queries:                             1701747 (5664.88 per sec.)
    ignored errors:                      280    (0.93 per sec.)
    reconnects:                          0      (0.00 per sec.)

    General statistics:
        total time:                          300.4008s
        total number of events:              59777

    Latency (ms):
            min:                                    1.06
            avg:                                  321.37
            max:                                 5131.15
            95th percentile:                      831.46
            sum:                             19210773.35

    Threads fairness:
        events (avg/stddev):           934.0156/28.04
        execution time (avg/stddev):   300.1683/0.11


### PS

mysql 5.7 faster than mariadb.I think problem is mariadb default enable bin log.mysql do not

### references
- https://www.percona.com/blog/2018/07/03/linux-os-tuning-for-mysql-database-performance/
- https://www.percona.com/blog/2016/10/12/mysql-5-7-performance-tuning-immediately-after-installation/
- http://www.monitis.com/blog/101-tips-to-mysql-tuning-and-optimization/