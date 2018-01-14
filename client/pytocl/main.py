"""Application entry point."""
import argparse
import logging

import sys

from client.my_driver import MyDriver
from client.pytocl.protocol import Client


def main():
    """Main entry point of application."""
    parser = argparse.ArgumentParser(
        description='Client for TORCS racing car simulation with SCRC network'
                    ' server.'
    )
    parser.add_argument(
        '--hostname',
        help='Racing server host name.',
        default='localhost'
    )
    parser.add_argument(
        '-p',
        '--port',
        help='Port to connect, 3001 - 3010 for clients 1 - 10.',
        type=int,
        default=3001
    )
    parser.add_argument(
        '-b',
        '--base',
        help='Fuzzy system rule base file.',
        type=str,
    )
    parser.add_argument(
        '-a',
        '--AKCELERACIJA',
        help='Default value for acceleration.',
        type=float,
        default=1.0
    )
    parser.add_argument(
        '-k',
        '--KOCNICA',
        help='Default value for break.',
        type=float,
        default=0.0
    )
    parser.add_argument(
        '-m',
        '--MJENJAC',
        help='Default value for gear.',
        type=int,
        default=1
    )
    parser.add_argument(
        '-vl',
        '--VOLAN',
        help='Default value for steering.',
        type=float,
        default=0.0
    )
    parser.add_argument(
        '-f',
        '--FOKUS',
        help='Default value for focus degree.',
        type=float,
        default=0.0
    )
    parser.add_argument('-v', help='Debug log level.', action='store_true')
    args = parser.parse_args()

    # switch log level:
    if args.v:
        level = logging.DEBUG
    else:
        level = logging.INFO
    del args.v
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)7s %(name)s %(message)s"
    )

    if args.base is None:
        print("Rule base file must be specified!", file=sys.stderr)
        sys.exit(-1)

    driver = MyDriver(rule_base_path=args.base, args=args, logdata=False)
    del args.base
    del args.AKCELERACIJA
    del args.KOCNICA
    del args.MJENJAC
    del args.VOLAN
    del args.FOKUS
    # start client loop:
    client = Client(driver=driver, **args.__dict__)
    client.run()


if __name__ == '__main__':
    main()
