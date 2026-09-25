import socket  # standard library module for low-level network connections
import time  # standard library module for timing and delays
import concurrent.futures  # standard library module for running scans in parallel


def resolve_host(target):  # define a function that turns a hostname into an IP address
    """Return the IPv4 address for `target`, or None if it cannot be resolved."""
    try:
        return socket.gethostbyname(target)  # ask the OS resolver for the IPv4 address
    except socket.gaierror:  # the hostname could not be resolved
        return None  # signal failure to the caller


def scan_port(host, port, timeout=1.0):  # define a function that tests a single TCP port
    """Return (port, is_open, banner) for one host:port combination."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a TCP socket
    sock.settimeout(timeout)  # don't block forever on unresponsive hosts
    try:
        result = sock.connect_ex((host, port))  # attempt a TCP handshake; 0 means open
        if result != 0:  # non-zero return code means connection failed
            return (port, False, "")  # report the port as closed/filtered
        banner = ""  # default banner if the service doesn't greet us
        try:
            sock.settimeout(0.5)  # short window for grabbing a banner
            banner = sock.recv(1024).decode(errors="ignore").strip()  # read up to 1 KB
        except (socket.timeout, UnicodeDecodeError):  # no banner or binary junk
            pass  # leave banner empty
        return (port, True, banner)  # report the port as open, with any banner
    except (socket.timeout, ConnectionRefusedError, OSError):  # connection problems
        return (port, False, "")  # treat all of them as "not open"
    finally:
        sock.close()  # always release the socket


def parse_ports(spec):  # define a function that turns a string like "22,80,100-110" into a list
    """Return a sorted list of ints from a comma/range port spec."""
    ports = set()  # use a set so duplicates collapse automatically
    for chunk in spec.split(","):  # split on commas
        chunk = chunk.strip()  # remove surrounding whitespace
        if not chunk:  # skip empty fragments (e.g. trailing comma)
            continue  # move to the next chunk
        if "-" in chunk:  # a range like "100-110"
            lo, hi = chunk.split("-", 1)  # split once on the dash
            ports.update(range(int(lo), int(hi) + 1))  # add every port in the range
        else:  # a single port like "80"
            ports.add(int(chunk))  # add the parsed integer
    return sorted(ports)  # return a deterministic, sorted list


def scan_host(host, ports, timeout=1.0, workers=100):  # define a function that scans many ports in parallel
    """Return a list of (port, banner) tuples for every open port on `host`."""
    open_ports = []  # accumulator list of (port, banner) tuples
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:  # spin up a worker pool
        futures = {pool.submit(scan_port, host, p, timeout): p for p in ports}  # queue one job per port
        for fut in concurrent.futures.as_completed(futures):  # consume results as they finish
            port, is_open, banner = fut.result()  # unpack the scan result
            if is_open:  # only care about ports that answered
                open_ports.append((port, banner))  # record the open port and any banner
    return sorted(open_ports)  # return results in ascending port order


def grab_banner(host, port, timeout=1.0):  # define a function that fetches a service banner on demand
    """Return a one-line banner string for `host:port`, or '' if none."""
    _, is_open, banner = scan_port(host, port, timeout)  # reuse the single-port scan
    return banner if is_open else ""  # only return banners for open ports


def timed_scan(host, ports, timeout=1.0):  # define a function that measures how long a scan takes
    """Run scan_host and return (results, elapsed_seconds)."""
    start = time.time()  # capture the start time
    results = scan_host(host, ports, timeout)  # perform the scan
    return results, time.time() - start  # return results plus duration