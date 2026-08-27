"""
CPU Scheduling Algorithms Simulator
------------------------------------
Implements classic CPU scheduling algorithms used in Operating Systems /
Computer Engineering coursework:

    - FCFS  (First Come First Serve)
    - SJF   (Shortest Job First, non-preemptive)
    - SRTF  (Shortest Remaining Time First, preemptive)
    - Round Robin
    - Priority Scheduling (non-preemptive)

Each function takes a list of Process objects and returns a list of the
same processes annotated with completion_time, turnaround_time and
waiting_time, plus a Gantt chart (list of (pid, start, end) tuples).
"""

from dataclasses import dataclass, field
from typing import List, Tuple
import copy


@dataclass
class Process:
    pid: str
    arrival_time: int
    burst_time: int
    priority: int = 0

    # Filled in after scheduling
    remaining_time: int = field(default=None)
    completion_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0

    def __post_init__(self):
        if self.remaining_time is None:
            self.remaining_time = self.burst_time


GanttEntry = Tuple[str, int, int]  # (pid, start_time, end_time)


def _finalize(processes: List[Process]) -> List[Process]:
    for p in processes:
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
    return processes


def fcfs(processes: List[Process]) -> Tuple[List[Process], List[GanttEntry]]:
    procs = copy.deepcopy(processes)
    procs.sort(key=lambda p: p.arrival_time)
    time = 0
    gantt = []
    for p in procs:
        if time < p.arrival_time:
            time = p.arrival_time
        start = time
        time += p.burst_time
        p.completion_time = time
        gantt.append((p.pid, start, time))
    return _finalize(procs), gantt


def sjf(processes: List[Process]) -> Tuple[List[Process], List[GanttEntry]]:
    """Non-preemptive Shortest Job First."""
    procs = copy.deepcopy(processes)
    n = len(procs)
    completed = 0
    time = 0
    done = [False] * n
    gantt = []

    while completed < n:
        idx = -1
        best_burst = float("inf")
        for i, p in enumerate(procs):
            if not done[i] and p.arrival_time <= time and p.burst_time < best_burst:
                best_burst = p.burst_time
                idx = i
        if idx == -1:
            # No process has arrived yet; jump to next arrival
            time = min(p.arrival_time for i, p in enumerate(procs) if not done[i])
            continue
        p = procs[idx]
        start = time
        time += p.burst_time
        p.completion_time = time
        gantt.append((p.pid, start, time))
        done[idx] = True
        completed += 1
    return _finalize(procs), gantt


def srtf(processes: List[Process]) -> Tuple[List[Process], List[GanttEntry]]:
    """Preemptive Shortest Remaining Time First."""
    procs = copy.deepcopy(processes)
    n = len(procs)
    time = 0
    completed = 0
    gantt = []
    last_pid = None
    segment_start = 0

    max_time = sum(p.burst_time for p in procs) + max(p.arrival_time for p in procs) + 1

    while completed < n and time <= max_time:
        idx = -1
        best_remaining = float("inf")
        for i, p in enumerate(procs):
            if p.arrival_time <= time and p.remaining_time > 0 and p.remaining_time < best_remaining:
                best_remaining = p.remaining_time
                idx = i

        if idx == -1:
            time += 1
            continue

        current_pid = procs[idx].pid
        if current_pid != last_pid:
            if last_pid is not None:
                gantt.append((last_pid, segment_start, time))
            segment_start = time
            last_pid = current_pid

        procs[idx].remaining_time -= 1
        time += 1

        if procs[idx].remaining_time == 0:
            procs[idx].completion_time = time
            completed += 1
            gantt.append((last_pid, segment_start, time))
            last_pid = None

    return _finalize(procs), gantt


def round_robin(processes: List[Process], quantum: int) -> Tuple[List[Process], List[GanttEntry]]:
    procs = copy.deepcopy(processes)
    procs.sort(key=lambda p: p.arrival_time)
    n = len(procs)
    time = 0
    queue = []
    gantt = []
    completed = 0
    in_queue = [False] * n
    i = 0  # pointer into arrival-sorted procs for adding new arrivals

    # seed queue with anything arriving at time 0
    while i < n and procs[i].arrival_time <= time:
        queue.append(i)
        in_queue[i] = True
        i += 1

    if not queue and n > 0:
        time = procs[0].arrival_time
        while i < n and procs[i].arrival_time <= time:
            queue.append(i)
            in_queue[i] = True
            i += 1

    while completed < n:
        if not queue:
            time = procs[i].arrival_time
            while i < n and procs[i].arrival_time <= time:
                queue.append(i)
                in_queue[i] = True
                i += 1
            continue

        idx = queue.pop(0)
        p = procs[idx]
        run_time = min(quantum, p.remaining_time)
        start = time
        time += run_time
        p.remaining_time -= run_time
        gantt.append((p.pid, start, time))

        # enqueue any processes that arrived during this slice
        while i < n and procs[i].arrival_time <= time:
            queue.append(i)
            in_queue[i] = True
            i += 1

        if p.remaining_time > 0:
            queue.append(idx)
        else:
            p.completion_time = time
            completed += 1

    return _finalize(procs), gantt


def priority_scheduling(processes: List[Process]) -> Tuple[List[Process], List[GanttEntry]]:
    """Non-preemptive priority scheduling. Lower number = higher priority."""
    procs = copy.deepcopy(processes)
    n = len(procs)
    completed = 0
    time = 0
    done = [False] * n
    gantt = []

    while completed < n:
        idx = -1
        best_priority = float("inf")
        for i, p in enumerate(procs):
            if not done[i] and p.arrival_time <= time and p.priority < best_priority:
                best_priority = p.priority
                idx = i
        if idx == -1:
            time = min(p.arrival_time for i, p in enumerate(procs) if not done[i])
            continue
        p = procs[idx]
        start = time
        time += p.burst_time
        p.completion_time = time
        gantt.append((p.pid, start, time))
        done[idx] = True
        completed += 1
    return _finalize(procs), gantt


def averages(processes: List[Process]) -> Tuple[float, float]:
    n = len(processes)
    avg_wt = sum(p.waiting_time for p in processes) / n
    avg_tat = sum(p.turnaround_time for p in processes) / n
    return avg_wt, avg_tat
