"""
CLI for the CPU Scheduling Simulator.

Run:
    python src/main.py

Edit the PROCESSES list below (or extend main() to read from a CSV/JSON
file) to try your own workload.
"""

from scheduler import (
    Process,
    fcfs,
    sjf,
    srtf,
    round_robin,
    priority_scheduling,
    averages,
)


def print_report(name, procs, gantt):
    print(f"\n{'=' * 50}")
    print(f" {name}")
    print(f"{'=' * 50}")

    print(f"{'PID':<6}{'Arrival':<10}{'Burst':<8}{'Completion':<12}{'Turnaround':<12}{'Waiting':<8}")
    for p in sorted(procs, key=lambda x: x.pid):
        print(f"{p.pid:<6}{p.arrival_time:<10}{p.burst_time:<8}"
              f"{p.completion_time:<12}{p.turnaround_time:<12}{p.waiting_time:<8}")

    avg_wt, avg_tat = averages(procs)
    print(f"\nAverage Waiting Time:    {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")

    print("\nGantt Chart:")
    chart = "|"
    labels = ""
    for pid, start, end in gantt:
        width = max(end - start, 1) * 4
        chart += f" {pid} " + "-" * (width - len(pid) - 2) + "|"
    print(chart)
    timeline = str(gantt[0][1]) if gantt else "0"
    for _, _, end in gantt:
        timeline += " " * 6 + str(end)
    print(timeline)


def build_sample_processes():
    return [
        Process(pid="P1", arrival_time=0, burst_time=5, priority=2),
        Process(pid="P2", arrival_time=1, burst_time=3, priority=1),
        Process(pid="P3", arrival_time=2, burst_time=8, priority=4),
        Process(pid="P4", arrival_time=3, burst_time=6, priority=3),
    ]


def main():
    processes = build_sample_processes()

    procs, gantt = fcfs(processes)
    print_report("First Come First Serve (FCFS)", procs, gantt)

    procs, gantt = sjf(processes)
    print_report("Shortest Job First (SJF, non-preemptive)", procs, gantt)

    procs, gantt = srtf(processes)
    print_report("Shortest Remaining Time First (SRTF, preemptive)", procs, gantt)

    procs, gantt = round_robin(processes, quantum=2)
    print_report("Round Robin (quantum=2)", procs, gantt)

    procs, gantt = priority_scheduling(processes)
    print_report("Priority Scheduling (lower = higher priority)", procs, gantt)


if __name__ == "__main__":
    main()
