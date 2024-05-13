# HTTP header fuzzer

This is a Python script that allows you to add a charachter to end of headers one by one and send HTTP request with modified header to a target server (kind of like fuzzing). You can customize various aspects of the request such as headers, parameters, and request rate.

## Features

- **Request Modification:** Modify HTTP headers and parameters using a wordlist.
- **Header Filtering:** Filter responses based on status codes, response size, or number of lines.
- **Colorized Output:** Response status codes, sizes, and lines are colorized for better visibility.
- **Rate Limiting:** Control the rate of requests sent per second.
- **Request Duration Logging:** Optionally log the duration of each request.

## Dependencies

- requests: For sending HTTP requests.
- colorama: For colorizing the output.
- argparse: For parsing command-line arguments.

## Installation

Clone this repository:

```bash
git clone https://github.com/mhossein1631/head-test
cd head-test
pip install -r requirements.txt
```

## Usage

```bash
python3 head-test.py -r <request_file> -w <wordlist_file> [options]
```

### Options:

- `r, --request <request_file>`: Path to the request file.
- `w, --wordlist <wordlist_file>`: Path to the wordlist file.
- `d, --ignored_headers <ignored_headers>`: Headers to be ignored (comma-separated).
- `fc, --status_filter <status_filter>`: Status code filter (comma-separated).
- `fs, --size_filter <size_filter>`: Size filter (comma-separated).
- `fl, --line_filter <line_filter>`: Line number filter (comma-separated).
- `delay, --delay <delay>`: Delay between requests (in milliseconds).
- `rate, --rate <rate>`: Number of requests per second.
- `time, --print_time`: Print request duration.

## Examples

Modify headers and send requests:

```bash
python3 head-test.py -r request.txt -w wordlist.txt
```

Modify headers, filter responses, and control request rate:

```bash
python3 head-test.py -r request.txt -w wordlist.txt -fc 200,404 -fs 1000-5000 -fl 10
```
