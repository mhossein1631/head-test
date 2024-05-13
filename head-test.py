import argparse
import requests
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(message)s')

def send_request(request, wordlist, ignored_headers, status_filter, size_filter, line_filter, delay, rate):
    with open(request, 'r') as req_file:
        request_data = req_file.read().splitlines()

    with open(wordlist, 'r') as wordlist_file:
        words = wordlist_file.read().splitlines()

    for word in words:
        for i, line in enumerate(request_data):
            if i == 0:
                modified_headers = []
                for header in request_data[1:]:
                    header_name, header_value = header.split(':', 1)
                    header_name = header_name.strip()
                    header_value = header_value.strip()
                    if header_name not in ignored_headers:
                        modified_header = f"{header_name}: {header_value} {word}"
                        modified_headers.append(modified_header)
                    else:
                        modified_headers.append(header)
                
                logging.info('\n'.join(modified_headers))
                modified_request = '\n'.join([request_data[0]] + modified_headers)
                
                start_time = time.time()
                response = requests.request('GET', 'https://target.com', headers={'Content-Type': 'text/plain'}, data=modified_request)
                end_time = time.time()

                if response.status_code not in status_filter and len(response.text) not in size_filter and len(response.text.splitlines()) not in line_filter:
                    logging.info(f"status [{response.status_code}]\tsize [{len(response.text)}]\tlines [{len(response.text.splitlines())}]")
                else:
                    logging.info("Response filtered")
                logging.info(f"Request took {end_time - start_time:.2f} seconds")
                logging.info("\n")
                
                time.sleep(delay)

def main():
    parser = argparse.ArgumentParser(description='HTTP request modification script')
    parser.add_argument('-r', '--request', help='Path to the request file', required=True)
    parser.add_argument('-w', '--wordlist', help='Path to the wordlist file', required=True)
    parser.add_argument('-d', '--ignored_headers', help='Headers to be ignored (comma-separated)', required=True)
    parser.add_argument('-fc', '--status_filter', help='Status code filter (comma-separated)', default='')
    parser.add_argument('-fs', '--size_filter', help='Size filter (comma-separated)', default='')
    parser.add_argument('-fl', '--line_filter', help='Line number filter (comma-separated)', default='')
    parser.add_argument('-delay', '--delay', help='Delay between requests (in milliseconds)', type=int, default=0)
    parser.add_argument('-rate', '--rate', help='Number of requests per second', type=int, default=1)
    args = parser.parse_args()

    ignored_headers = args.ignored_headers.split(',')
    status_filter = [int(code) for code in args.status_filter.split(',') if code]
    size_filter = [int(size) for size in args.size_filter.split(',') if size]
    line_filter = [int(line) for line in args.line_filter.split(',') if line]

    send_request(args.request, args.wordlist, ignored_headers, status_filter, size_filter, line_filter, args.delay / 1000, 1 / args.rate)

if __name__ == "__main__":
    main()
