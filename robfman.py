import argparse
import httpx
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
TIMEOUT = 60

def print_banner():

    print(r"""
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓   ░░░ R O B F M A N ░░░   ▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
""")






def get_snapshots(domain, path):
    url = f"https://web.archive.org/cdx/search/cdx?url=https://{domain}/{path}&output=json&filter=statuscode:200&fl=timestamp,original&collapse=digest"
    try:
        with httpx.Client(verify=False, timeout=TIMEOUT) as client:
            r = client.get(url)
        if r.status_code != 200:
            return []
        data = r.json()
        return [row[0] for row in data[1:]]
    except Exception:
        return []

def fetch_snapshot(domain, path, timestamp):
    snapshot_url = f"https://web.archive.org/web/{timestamp}if_/https://{domain}/{path}"
    try:
        with httpx.Client(verify=False, timeout=TIMEOUT) as client:
            r = client.get(snapshot_url)
        if r.status_code == 200:
            return r.text
        return None
    except Exception:
        return None

def load_list_from_file(filename):
    items = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            item = line.strip()
            if item:
                items.append(item)
    return items

def main():
    print_banner()  # Print banner at start

    parser = argparse.ArgumentParser(description='roBFMan - Archive.org page content finder (multi-domain & multi-path)')
    parser.add_argument('-t', '--target', help='Single target domain')
    parser.add_argument('-ft', '--file_targets', help='File containing list of domains (one per line)')
    parser.add_argument('-p', '--path', default='robots.txt', help='Single path (default: robots.txt)')
    parser.add_argument('-fp', '--file_paths', help='File containing list of paths (one per line)')
    parser.add_argument('-d', '--delay', type=float, default=0.5, help='Delay (seconds) between each request [default: 0.5]')
    parser.add_argument('-o', '--output', help='Output file for saving results')
    args = parser.parse_args()

    # Prepare targets
    targets = []
    if args.file_targets:
        targets = load_list_from_file(args.file_targets)
    elif args.target:
        targets = [args.target]
    else:
        print("You must specify either --target/-t or --file_targets/-ft")
        return

    # Prepare paths
    paths = []
    if args.file_paths:
        paths = load_list_from_file(args.file_paths)
    elif args.path:
        paths = [args.path]
    else:
        print("You must specify either --path/-p or --file_paths/-fp")
        return

    delay = args.delay
    output_lines = []

    for domain in targets:
        domain = domain.strip().rstrip('/')
        for path in paths:
            path = path.lstrip('/')
            snapshots = get_snapshots(domain, path)
            if not snapshots:
                output_lines.append(f"\n----- {domain}/{path} -----\nNo snapshots found for this path.\n")
                continue
            for idx, ts in enumerate(snapshots, 1):
                content = fetch_snapshot(domain, path, ts)
                header = f"\n----- {domain}/{path} @ {ts} -----\n"
                if content:
                    output_lines.append(header + content)
                else:
                    output_lines.append(header + "[Content not available]")
                time.sleep(delay)

    # Write to file or print
    if args.output:
        Path(args.output).write_text('\n'.join(output_lines), encoding='utf-8')
        print(f"Results written to: {args.output}")
    else:
        for line in output_lines:
            print(line)

if __name__ == "__main__":
    main()
