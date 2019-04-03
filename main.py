import stingconf


parser = stingconf.Parser(description='This is test module.')
print(parser)
print(type(parser))
print(dir(parser))
parser.env_prefix('TEST')
parser.conf_file('config.yml')
parser.add('time-wait', short='t', type=int, default=10)
parser.order('env', 'arg', 'file', 'default')

parser.parse()
print(parser.TIME_WAIT)
print(type(parser.TIME_WAIT))
