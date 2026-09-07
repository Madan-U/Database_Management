# ==============================================================================
# File        : collectors/health_checks.py
# Location    : /data/database-management/collectors/health_checks.py
# Purpose     : Shared health-check helper routines used by the collectors.
# Author      : Madan U
# Email       : madan.u@kotak.com
# Created On  : 2026-09-07
# Last Update : 2026-09-07
# ==============================================================================

"""Central place for alert thresholds, per the requirement doc's Phase 2
alerting table. Keeping this separate from the collectors makes thresholds
easy to tune without touching SSH/Mongo connection code."""

THRESHOLDS = {
    "cpu_warning_pct": 85,
    "memory_warning_pct": 90,
    "disk_warning_pct": 80,
    "connections_warning_pct": 90,
    "replication_lag_warning_seconds": 10,
}


def evaluate_os_status(cpu_usage=None, memory_usage=None, disk_usage=None):
    if (cpu_usage and cpu_usage > THRESHOLDS["cpu_warning_pct"]) or \
       (memory_usage and memory_usage > THRESHOLDS["memory_warning_pct"]) or \
       (disk_usage and disk_usage > THRESHOLDS["disk_warning_pct"]):
        return "yellow"
    return "green"
