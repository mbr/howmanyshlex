import shlex


class SyntaxError(Exception):
    def __init__(self, reason, linenum, line):
        super(SyntaxError, self).__init__('{}: {}'.format(linenum, reason))


def parse_format(src):
    rv = []

    for n, line in enumerate(src.splitlines()):
        # skip blank lines
        if not line.strip():
            continue

        if line.startswith('  '):
            # comment line
            continue

        fields = shlex.split(line, posix=True)
        entry = {}

        if len(fields) == 1:
            raise SyntaxError('Missing password', n, line)

        if len(fields) > 3:
            # check if the extra fields are comments
            if fields[3] != '#':
                raise SyntaxError('Too many fields, expected comment')

            entry['comment'] = [' '.join(fields[4:])]

        if not fields[0].endswith(':'):
            raise SyntaxError('Key must end with colon (:)', n, line)

        entry['key'] = fields[0]

        entry['username'] = None
        if len(fields) == 2:
            entry['password'] = fields[1]

        elif len(fields) == 3:
            entry['username'] = fields[1]
            entry['username'] = fields[2]

        rv.append(entry)

    return rv


sample = r"""
.an_old_entry_that_is_ignored: foo bar

mail.google: first-user@gmail.com "*****"
  see https://mail.google.com/

mail.google: second-user@gmail.com "*****"
  John's account

ssh.my_private_server: root "*****"
  with great power comes great responsibility.

mobile.pin: 12345
"""


sample2 = r"""
.an_old_entry_that_is_ignored: foo bar
mail.google: first-user@gmail.com "*****"  # see https://mail.google.com/
mail.google: second-user@gmail.com "*****"  # John's account
ssh.my_private_server: root "*****"
  with great power comes great responsibility
  and some other crappy freeform information
mobile.pin: 12345
"""


print parse_format(sample)
print parse_format(sample2)
