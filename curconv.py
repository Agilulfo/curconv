import argparse
import os
import sys

from forex_python.converter import CurrencyRates
from yaml import YAMLError, load

DEFAULT_CONFIGURATION_FILE_PATH = [
    os.getenv('HOME') + "/.curconv.yaml",
    "./curconv.yaml"
]

OUTPUT_FORMAT = "{amount} {currency}"


def load_configuration_from_file(file):
    """
    Attempt to load configuration from a given file or from known file paths.
    """
    try:
        if file:
            return load(file)
        else:
            for path in DEFAULT_CONFIGURATION_FILE_PATH:
                try:
                    return load(open(path, 'r'))
                except FileNotFoundError:
                    pass
        return None
    except YAMLError:
        sys.exit('Malformed configuration file!')


def main():
    parser = argparse.ArgumentParser(
        description='Simple currency conversion tool :-)'
    )
    parser.add_argument('amount', type=float,
                        help='amount to convert to other currency')
    parser.add_argument('from_currency', type=str, nargs='?', default=None,
                        help='currency from which you want to convert')
    parser.add_argument('to_currencies', type=str, nargs='*',
                        help='currency to which you want to convert')
    parser.add_argument('--conf', dest='configuration_file',
                        type=argparse.FileType('r'),
                        default=None, help='configuration file')

    arguments = parser.parse_args()
    conf = load_configuration_from_file(arguments.configuration_file)

    amount = arguments.amount

    if conf:
        arguments.from_currency = (arguments.from_currency
                                   or conf['from_currency'])
        arguments.to_currencies = (arguments.to_currencies
                                   or conf['to_currencies'])

    from_currency = arguments.from_currency.upper()
    to_currencies = [currency.upper()for currency in arguments.to_currencies]

    converter = CurrencyRates()

    results = [(converter.convert(from_currency, dest, amount), dest)
               for dest in to_currencies if dest != from_currency]

    print(OUTPUT_FORMAT.format(amount=amount, currency=from_currency))
    for amount, currency in results:
        print(OUTPUT_FORMAT.format(amount=amount, currency=currency))


if __name__ == '__main__':
    main()
