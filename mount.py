import re


def main():
    start_state_log = open('pre-mount.log', 'r')

    parse_state_log(start_state_log)


def parse_state_log(log_file):
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

        elif re.search(re_fstab_match, line):
            print('{} {}'.format(host, line))

        elif re.search(re_symlink_match, line):
            print('{} {}'.format(host, line))


class HostMounts:

    def __init__(self, log_data_block):
        self.log_data_block =  log_data_block

    def parse_data_block(self):
        print("Test")

if __name__ == "__main__":
    main()
