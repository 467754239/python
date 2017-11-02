# optparse

```python
import optparse

# https://github.com/ansible/ansible/blob/devel/hacking/test-module

def parse():
    """parse command line
    :return : (options, args)"""
    parser = optparse.OptionParser()

    parser.usage = "%prog -[options] (-h for help)"

    parser.add_option('-m', '--module-path', dest='module_path',
        help="REQUIRED: full path of module source to execute")
    parser.add_option('-a', '--args', dest='module_args', default="",
        help="module argument string")
    parser.add_option('-D', '--debugger', dest='debugger', 
        help="path to python debugger (e.g. /usr/bin/pdb)")
    parser.add_option('-I', '--interpreter', dest='interpreter',
        help="path to interpreter to use for this module (e.g. ansible_python_interpreter=/usr/bin/python)",
        metavar='INTERPRETER_TYPE=INTERPRETER_PATH',
        default='python={0}'.format(sys.executable))
    parser.add_option('-c', '--check', dest='check', action='store_true',
        help="run the module in check mode")
    parser.add_option('-n', '--noexecute', dest='execute', action='store_false',
        default=True, help="do not run the resulting module")
    parser.add_option('-o', '--output', dest='filename',
        help="Filename for resulting module",
        default="~/.ansible_module_generated")
    options, args = parser.parse_args()
    if not options.module_path:
        parser.print_help()
        sys.exit(1)
    else:
        return options, args
        
        
def main():

    options, args = parse()
```
