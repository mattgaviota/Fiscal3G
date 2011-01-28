#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from ConfigParser import SafeConfigParser
from optparse import OptionParser, OptionValueError

def main():
    # == Reading the config file ==

    # Define the defaults value
    config = SafeConfigParser({
        "host":"localhost",
        "port":"4080",
        "user":None,
        "password":None,
        "maxdownload":"0",
        "maxupload":"10",
        "minupload":"1",
        "margin":"down_rate ** (1/3.)",
    })

    # Read the values on the file
    config.read(os.path.expanduser('~/.mlshell'))

    # == Reading the options of the execution ==

    def define_variable(option, opt_str, value, parser):
        """Handle the -d/--define option and populate the variables dict"""
        logging.debug(option.dest)
        logging.debug(value)
        variables = getattr(parser.values, option.dest)

        try:
            variable = re.search(r"".join(("^\s*([a-zA-Z_][a-zA-Z\d_]*)",
                "\s*=\s*(.*)\s*$")), value).groups()
        except AttributeError:
            raise OptionValueError("Declaración incorrecta: %s" % value)
        else:
            variables.update((variable,))

        logging.debug(variables)

    # Instance the parser and define the usage message
    parser = OptionParser(usage="""
    %prog [-vqd]
    %prog [-vqd] file
    %prog [-vqdc] command""", version="%prog 2")

    # Define the options and the actions of each one
    parser.add_option("-c", help="Read the comands from" +
        " the arg instead of from the standard input", action="store_true",
        dest="command")
    parser.add_option("-v", "--verbose", action="count", dest="verbose")
    parser.add_option("-q", "--quiet", action="count", dest="quiet")
    parser.add_option("-d", "--define", metavar="VAR=VALUE", action="callback",
        callback=define_variable, type="string", nargs=1, dest="variables",
        help="Define a variable VAR to VALUE")

    # Define the default options
    parser.set_defaults(verbose=2, quiet=0, variables={})

    # Process the options
    options, args = parser.parse_args()

    # == Execution ==

    # Crate the wrapper instance
    session = MLSession(
        config.get("Server", "user"),
        config.get("Server", "password")
    )

    for variable in config.options("Variables"):
        session.variables[variable] = config.get("Variables", variable)

    for variable in options.variables:
        session.variables[variable] = options.variables[variable]

    logging.debug(session.variables)

    if options.command:
        print(session.execute(" ".join(args)))
        return 0

    elif args:
        print("Leyendo comandos en %s" % args[0])

    else:
        order = None
        while order not in ("q", "kill"):
            try:
                order = raw_input(session.get_prompt()).strip()

            except EOFError:
                return

            else:
                print(session.execute(order))


if __name__ == "__main__":
    exit(main())
