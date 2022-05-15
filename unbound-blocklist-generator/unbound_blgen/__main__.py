import argparse

DOMAIN_FORBID_CHARS = set("\"'\0\n\r\t ")


def is_valid_domain_name(domain):
    # This is a very crude check to filter out forbidden chars in the
    # domain name. A few chars must be filtered out to prevent syntax
    # errors in the unbound configuration. The current approach is
    # however not fool-proof..
    #
    # A regular expression would be the better option, but I couldn't quickly
    # find a regular expression that works for all domains in the StevenBlack
    # hosts file.
    return not any((c in DOMAIN_FORBID_CHARS) for c in domain)


def parse_line(line):
    # Ignore empty and commented lines.
    line = line.strip()
    if (not line) or line[0] == "#":
        return None

    # Strip comments after content.
    line = line.split("#", 1)[0].strip()
    parts = line.split(" ")
    host = parts[1 if len(parts) > 1 else 0].strip()
    if host == "0.0.0.0" or not is_valid_domain_name(host):
        return None

    return host


def parse(filename):
    with open(filename) as f:
        for line in f:
            host = parse_line(line)
            if host is not None:
                yield host


def format_block_rule(host):
    return 'local-zone: "{0}" static'.format(host)


def expand_host(host):
    parts = host.split(".")
    for i in range(2, len(parts)):
        yield ".".join(parts[-i:])
    yield host


def contains_subdomain(blocklist, host):
    for subdomain in reversed(list(expand_host(host))):
        if subdomain in blocklist:
            return True
    return False


def load_blocklists(files):
    if not files:
        return set()

    hostlist = list()
    for filename in files:
        hostlist.extend(parse(filename))

    blocklist = set()
    for host in sorted(hostlist, key=len):
        if not contains_subdomain(blocklist, host):
            blocklist.add(host)

    return blocklist


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--blacklist", action="append")
    parser.add_argument("-w", "--whitelist", action="append")

    args = parser.parse_args()
    whitelist = load_blocklists(args.whitelist)
    blacklist = [
        host
        for host in load_blocklists(args.blacklist)
        if not contains_subdomain(whitelist, host)
    ]

    for line in sorted(blacklist):
        print(format_block_rule(line))


if __name__ == "__main__":
    main()
