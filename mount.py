import re


def main():
    start_state_log = open('pre-mount.log', 'r')
    host_mounts = {}

    parse_state_log(start_state_log, host_mounts)

    for host in host_mounts:
        print(host)
        host_mounts[host].print_mounts()
        host_mounts[host].print_symlinks()


def parse_state_log(log_file, host_mounts):
    host = False

    for line in log_file:

        re_section_match = '#{34}'
        re_host_match = '[a-zA-Z0-9]*-[a-zA-Z0-9]*-[a-zA-Z0-9]*-[a-zA-Z0-9]*-[a-zA-Z]*[0-9]*'
        re_fstab_match = '^.*cifs.*'
        re_symlink_match = '^lrwxrwxrwx.*->.*'

        if re.search(re_section_match, line):
            pass

        elif re.search(re_host_match, line):
            host = line
            if host not in host_mounts:
                host_mounts[host] = HostMounts(host)

        elif re.search(re_fstab_match, line):
            if host:
                host_mounts[host].add_mount(line, 'pre')

        elif re.search(re_symlink_match, line):
            if host:
                host_mounts[host].add_symlink(line, 'pre')


class HostMounts:

    def __init__(self, test_string):
        self.test_string = test_string
        self.mounts = {
            'pre': [],
            'post': []
        }
        self.symlinks = {
            'pre': [],
            'post': []
        }

    def add_mount(self, mount_data, state):
            self.mounts[state].append(mount_data)

    def print_mounts(self):
        print(self.mounts)

    def add_symlink(self, mount_data, state):
            self.symlinks[state].append(mount_data)

    def print_symlinks(self):
        print(self.symlinks)


if __name__ == "__main__":
    main()


