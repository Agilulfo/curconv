import argparse
import os

from forex_python.converter import CurrencyRates

from configuration import YAMLConfigurationFileLoader

DEFAULT_CONFIGURATION_FILE_PATHS = [
    os.path.join(os.getenv('HOME'), ".curconv.yaml"),
    os.path.join(os.getcwd(), "curconv.yaml")
]

OUTPUT_FORMAT = "{amount} {currency}"


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Simple currency conversion tool :-)'
    )
    parser.add_argument('amount',
                        type=float,
                        help='amount to convert to other currency')
    parser.add_argument('from_currency',
                        type=str,
                        nargs='?',
                        default=None,
                        help='currency from which you want to convert')
    parser.add_argument('to_currencies',
                        type=str,
                        nargs='*',
                        help='currency to which you want to convert')
    parser.add_argument('--conf',
                        type=argparse.FileType('r'),
                        dest='configuration_file',
                        default=None,
                        help='configuration file')
    return parser.parse_args()


def main():
    arguments = parse_arguments()

    loader = YAMLConfigurationFileLoader(arguments.configuration_file,
                                         DEFAULT_CONFIGURATION_FILE_PATHS)
    conf = loader.load_from_file()

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
