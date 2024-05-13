import requests
import logging
import time
from colorama import init, Fore
import argparse

logging.basicConfig(level=logging.INFO, format='%(message)s')

init(autoreset=True)

def colorize_status_code(status_code):
    if status_code.startswith('2'):
        return Fore.GREEN + status_code
    elif status_code.startswith('3'):
        return Fore.YELLOW + status_code
    elif status_code.startswith('4'):
        return Fore.RED + status_code
    elif status_code.startswith('5'):
        return Fore.MAGENTA + status_code
    else:
        return status_code

def colorize_size_and_lines(size, lines):
    return Fore.BLUE + f"size [{size}]   lines [{lines}]"

def send_request(request, wordlist, ignored_headers, status_filter, size_filter, line_filter, delay, rate, print_time):
    with open(request, 'r') as req_file:
        request_data = req_file.read().splitlines()

    with open(wordlist, 'r') as wordlist_file:
        words = wordlist_file.read().splitlines()

    for word in words:
        for i, line in enumerate(request_data):
            if i == 0 or line.startswith("Host"):
                continue
            elif line.split(':', 1)[0].strip() in ignored_headers:
                continue
            else:
                modified_headers = request_data[:]
                header_name, header_value = line.split(':', 1)
                modified_header = f"{header_name.strip()}: {header_value.strip()}{word}"  # Remove space here
                modified_headers[i] = modified_header


                modified_request = '\n'.join(modified_headers)

                start_time = time.time()
                response = requests.request('GET', 'https://target.com', headers={'Content-Type': 'text/plain'}, data=modified_request)
                end_time = time.time()

                status_code = colorize_status_code(str(response.status_code))
                size_and_lines = colorize_size_and_lines(len(response.text), len(response.text.splitlines()))

                # Check if the response matches any filters
                if response.status_code in status_filter or len(response.text) in size_filter or len(response.text.splitlines()) in line_filter:
                    continue  # Skip printing the response if it's filtered
                else:
                	logging.info(modified_headers[i])

                logging.info(f"status [{status_code}]\t{size_and_lines}")
                if print_time:
                    logging.info(f"Request took {end_time - start_time:.2f} seconds")
                logging.info("\n")

                time.sleep(delay)

def main():
    des="""-r, --request <request_file>: Path to the request file.
-w, --wordlist <wordlist_file>: Path to the wordlist file.
-d, --ignored_headers <ignored_headers>: Headers to be ignored (comma-separated).
-fc, --status_filter <status_filter>: Status code filter (comma-separated).
-fs, --size_filter <size_filter>: Size filter (comma-separated).
-fl, --line_filter <line_filter>: Line number filter (comma-separated).
-delay, --delay <delay>: Delay between requests (in milliseconds).
-rate, --rate <rate>: Number of requests per second.
-time, --print_time: Print request duration."""
    parser = argparse.ArgumentParser(description='HTTP request modification script')
    parser.add_argument('-r', '--request', help='Path to the request file', required=True)
    parser.add_argument('-w', '--wordlist', help='Path to the wordlist file', required=True)
    parser.add_argument('-d', '--ignored_headers', help='Headers to be ignored (comma-separated)')
    parser.add_argument('-fc', '--status_filter', help='Status code filter (comma-separated)', default='')
    parser.add_argument('-fs', '--size_filter', help='Size filter (comma-separated)', default='')
    parser.add_argument('-fl', '--line_filter', help='Line number filter (comma-separated)', default='')
    parser.add_argument('-delay', '--delay', help='Delay between requests (in milliseconds)', type=int, default=0)
    parser.add_argument('-rate', '--rate', help='Number of requests per second', type=int, default=10)
    parser.add_argument('-time', '--print_time', help='Print request duration', action='store_true')
    parser.add_argument('-h', '--help', help=des)
    args = parser.parse_args()

    ignored_headers = args.ignored_headers.split(',')
    status_filter = [int(code) for code in args.status_filter.split(',') if code]
    size_filter = [int(size) for size in args.size_filter.split(',') if size]
    line_filter = [int(line) for line in args.line_filter.split(',') if line]

    send_request(args.request, args.wordlist, ignored_headers, status_filter, size_filter, line_filter, args.delay / 1000, 1 / args.rate, args.print_time)

if __name__ == "__main__":
    main()
