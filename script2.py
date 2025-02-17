import os
import re
import json
from collections import Counter

log_patter = re.compile(
    r'(?P<ip>S+) - - [(?P<time>[^]]+)] "(?P<request>[^"]+)" (?P<status>d{3}) (?P<bytes>d+) "(?P<referer>[^"]*)"'
)

def parse_log_line(line):
    line_match = log_patter.match(line)
    if line_match:
        return line_match.groupdict()
    return None

def analyze_log_file(file_path):
    total_requests = 0
    method_count = Counter()
    ip_count = Counter()
    top_slow_requests = []

    with open(file_path, 'r') as f:
        for line in f:
            total_requests+=1
            log_data = parse_log_line(line)
            if log_data:
                method = log_data['request'].split()[0]
                method_count[method]+=1
                ip_count[log_data['ip']]+=1
                duration = int(log_data['duration'])
                if len(top_slow_requests) < 3 or duration > top_slow_requests[-1]['duration']:
                    top_slow_requests.append({
                        'ip': log_data['ip'],
                        'date': log_data['time'],
                        'method': method,
                        'url': log_data['request'].split()[1] if len(log_data['request'].split())
                    })
                    top_slow_requests.sort(key=lambda x: x['dutation'], reverse=True)
                top_slow_requests = top_slow_requests[:3]
    return {
        'total_requests': total_requests,
        'total_stat': dict(method_count),
        'top_ips': ip_count.most_common(3),
        'top_longest': top_slow_requests
    }

def save_to_json(data, output_path):
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

def process_logs(path):
    if os.path.isfile(path):
        log_files = [path]
    elif os.path.isdir(path):
        log_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.log')]
    else:
        print(f"Path {path} is not valid")
        return

    for log_file in log_files:
        print(f"Processing {log_file}...")
        stats = analyze_log_file(log_file)
        output_json = f"{os.path.splitext(log_file)[0]}_stats.json"
        save_to_json(stats, output_json)
        print(json.dumps(stats, indent=4))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Analyzde web server log files.")
    parser.add_argument("path", help='Path to log fule or directiry containing log files.')
    args = parser.parse_args()
    process_logs(args.path)


