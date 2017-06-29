import re
from deepdiff import DeepDiff
from pprint import pprint


def main():
    start_state_log = open('prod-pre-mount.log', 'r')
    end_state_log = open('prod-post-mount.log', 'r')
    host_mounts = {}

    parse_state_log(start_state_log, host_mounts, 'pre')
    parse_state_log(end_state_log, host_mounts, 'post')

    compare_state_log(host_mounts, ['pre', 'post'])


def parse_state_log(log_file, host_mounts, state):
    host = False

    for line in log_file:

        re_section = re.compile('#{34}')
        re_host = re.compile('([a-zA-Z0-9]*-[a-zA-Z0-9]*-[a-zA-Z0-9]*-.*)')
        re_fstab = re.compile('^(.*)\\t(.*)\\tcredentials=')
        re_symlink = re.compile('([a-zA-Z0-9]*)\s->\s(.*?)(?:\\n)?$')

        if re_section.search(line):
            pass

        elif re_host.search(line):
            host = re_host.search(line).group(1)
            if host not in host_mounts:
                host_mounts[host] = HostMounts(host)

        elif re_fstab.search(line):
            if host:
                fstab_data = re_fstab.search(line)
                fstab_vol = fstab_data.group(1)
                fstab_fstype = fstab_data.group(2)
                host_mounts[host].add_mount(fstab_vol, fstab_fstype, state)

        elif re_symlink.search(line):
            if host:
                symlink_data = re_symlink.search(line)
                symlink_name = symlink_data.group(1)
                symlink_target = symlink_data.group(2)
                host_mounts[host].add_symlink(symlink_name, symlink_target, state)
                pass


def compare_state_log(host_mounts, states):
    for host in host_mounts:
        host_mounts[host].compare_mounts(states)
        host_mounts[host].compare_symlinks(states)


class HostMounts(object):

    def __init__(self, host_name):
        self.host_name = host_name
        self.mounts = {
            'pre': {},
            'post': {}
        }
        self.symlinks = {
            'pre': {},
            'post': {}
        }

    def add_mount(self, volume, fstype, state):
            self.mounts[state][volume] = {'volume': volume, 'fstype': fstype}

    def compare_mounts(self, states):
        for a in range(0, len(states)):
            for b in range(a, len(states)):
                diff = self.compare_dict(self.mounts[states[a]], self.mounts[states[b]])
                if diff != {}:
                    pprint({self.host_name: diff}, indent=2)
                    print('\n')

    def add_symlink(self, name, target, state):
            self.symlinks[state][name] = {'name': name, 'target': target}

    def compare_symlinks(self, states):
        for a in range(0, len(states)):
            for b in range(a, len(states)):
                diff = self.compare_dict(self.symlinks[states[a]], self.symlinks[states[b]])
                if diff != {}:
                    pprint({self.host_name: diff}, indent=2)
                    print('\n')

    @staticmethod
    def compare_dict(dict_a, dict_b):
        return DeepDiff(dict_a, dict_b)

    @property
    def host_name(self):
        return self.__host_name

    @host_name.setter
    def host_name(self, value):
        self.__host_name = value

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
