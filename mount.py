import re


def main():
    start_state_log = open('pre-mount.log', 'r')
    end_state_log = open('post-mount.log', 'r')
    host_mounts = {}

    parse_state_log(start_state_log, host_mounts, 'pre')
    parse_state_log(end_state_log, host_mounts, 'post')

    for host in host_mounts:
        print(host)
        print(host_mounts[host].mounts)
        print(host_mounts[host].symlinks)


def parse_state_log(log_file, host_mounts, state):
    host = False

    for line in log_file:

        re_section = re.compile('#{34}')
        re_host = re.compile('[a-zA-Z0-9]*-[a-zA-Z0-9]*-[a-zA-Z0-9]*-[a-zA-Z0-9]*-[a-zA-Z]*[0-9]*')
        re_fstab = re.compile('^.*cifs.*')
        re_symlink = re.compile('([a-zA-Z0-9]*)\s->\s(.*?)(?:\\n)?$')

        if re_section.search(line):
            pass

        elif re_host.search(line):
            host = line
            if host not in host_mounts:
                host_mounts[host] = HostMounts()

        elif re_fstab.search(line):
            if host:
                host_mounts[host].add_mount(line, state)

        elif re_symlink.search(line):
            if host:
                symlink_data = re_symlink.search(line)
                symlink_name = symlink_data.group(1)
                symlink_target = symlink_data.group(2)
                host_mounts[host].add_symlink(symlink_name, symlink_target, state)
                pass


class HostMounts(object):

    def __init__(self):
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

    def add_symlink(self, name, target, state):
            self.symlinks[state].append({'name': name, 'target': target})

    @property
    def mounts(self):
        return self.__mounts

    @mounts.setter
    def mounts(self, value):
        self.__mounts = value

    @property
    def symlinks(self):
        return self.__symlinks

    @symlinks.setter
    def symlinks(self, value):
        self.__symlinks = value


if __name__ == "__main__":
    main()
