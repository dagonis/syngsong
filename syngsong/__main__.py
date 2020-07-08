import argparse
import logging
import os
import sys

import core

if not sys.version_info.major == 3 and sys.version_info.minor >= 6:
    print("You need to be running at least Python3.6 for this to work.")
    sys.exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("artist", help="The artist you would like to grab lyrics for.")
    parser.add_argument("--minsize", help="Minimum password length, default: 8", default=8, type=int)
    parser.add_argument("--maxsize", help="Maximum password length, default: 32", default=32, type=int)
    parser.add_argument("--mask", help="Hashcat style mask to append extra characters to the end of the passwords, Provide these in double quotes to keep your shell happy.", default="")
    parser.add_argument("--geniuskey", "-g", help="The Client Access Token from genius.com, you can also provide this with the envar GENIUSKEY")
    parser.add_argument("--topsongs", "-t", help="Pull x number of songs for an artist, based on popularity.", type=int, default=0)
    parser.add_argument("--debug", "-d", help="Set logging to DEBUG level, INFO by default", action='store_true')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    logging.info(f"Starting Syngsong - Artist: {args.artist}, Minsize: {args.minsize}, Maxsize: {args.maxsize}, Mask: {args.mask if not args.mask == '' else 'None'}")
    if args.geniuskey is None and os.getenv("GENIUSKEY") is None:
        print("You need to provide a genius Client access token either via the -g option at invocation or with the envar GENIUSKEY")
        sys.exit()
    else:
        genius_key = args.geniuskey if args.geniuskey is not None else os.getenv("GENIUSKEY")
    core.generate_passwords(args.artist, genius_key, args.mask, min_len=args.minsize, max_len=args.maxsize, top_songs=args.topsongs)
