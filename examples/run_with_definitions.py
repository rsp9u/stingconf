import stingconf
import yaml


with open('definitions.yml') as f:
    definitions = yaml.safe_load(f)
parser = stingconf.Parser('This is test module.', definitions)
parser.parse()

print(parser.TIME_WAIT)
print(parser.USER)
print(parser.PASSWORD)
print(parser.HTTP_PROXY)
print(parser.HTTPS_PROXY)
