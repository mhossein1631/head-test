import argparse
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

def send_request(request, wordlist, ignored_header):
    with open(request, 'r') as req_file:
        request_data = req_file.read().splitlines()

    with open(wordlist, 'r') as wordlist_file:
        words = wordlist_file.read().splitlines()

    for word in words:
        for i, line in enumerate(request_data):
            if i == 0:
                logging.info(f"{line} {word}")
            elif line.startswith(ignored_header):
                logging.info(line)
            else:
                logging.info(f"{line} {word}")

        modified_request = '\n'.join(request_data)
        response = requests.request('GET', 'https://target.com', headers={'Content-Type': 'text/plain'}, data=modified_request)
        logging.info(f"Response status code: {response.status_code}")
        logging.info(f"Response size: {len(response.text)}")
        logging.info(f"Response lines: {len(response.text.splitlines())}")
        logging.info("\n")

def main():
    parser = argparse.ArgumentParser(description='HTTP request modification script')
    parser.add_argument('-r', '--request', help='Path to the request file', required=True)
    parser.add_argument('-w', '--wordlist', help='Path to the wordlist file', required=True)
    parser.add_argument('-d', '--ignored_header', help='Header to be ignored', required=True)
    args = parser.parse_args()

    send_request(args.request, args.wordlist, args.ignored_header)

if __name__ == "__main__":
    main()
