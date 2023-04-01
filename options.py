import argparse
import sys
import os

def getArgs():
    """
    Parse the command line options and return the result
    You can get args like that :
    args.verbose # True or False
    args.recursive # True or False

    You can also get the help message like that :
    python mrsync.py -h
    """
    parser = argparse.ArgumentParser(description='A program to sync files using rsync')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase verbosity')
    parser.add_argument('-q', '--quiet', action='store_true', help='Suppress non-error messages')
    parser.add_argument('-a', '--archive', action='store_true', help='Archive mode; same as -rpt (no -H)')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recurse into directories')
    parser.add_argument('-u', '--update', action='store_true', help='Skip files that are newer on the receiver')
    parser.add_argument('-d', '--dirs', action='store_true', help='Transfer directories without recursing')
    parser.add_argument('-H', '--hard-links', action='store_true', help='Preserve hard links')
    parser.add_argument('-p', '--perms', action='store_true', help='Preserve permissions')
    parser.add_argument('-t', '--times', action='store_true', help='Preserve times')
    parser.add_argument('--existing', action='store_true', help='Skip creating new files on receiver')
    parser.add_argument('--ignore-existing', action='store_true', help='Skip updating files that exist on receiver')
    parser.add_argument('--delete', action='store_true', help='Delete extraneous files from dest dirs')
    parser.add_argument('--force', action='store_true', help='Force deletion of dirs even if not empty')
    parser.add_argument('--timeout', type=int, help='Set I/O timeout in seconds')
    parser.add_argument('--blocking-io', action='store_true', help='Use blocking I/O for the remote shell')
    parser.add_argument('-I', '--ignore-times', action='store_true', help="Don't skip files that match size and time")
    parser.add_argument('--size-only', action='store_true', help='Skip files that match in size')
    parser.add_argument('--address', help='Bind address for outgoing socket to daemon')
    parser.add_argument('--port', type=int, help='Specify double-colon alternate port number')
    parser.add_argument('--list-only', action='store_true', help='List the files instead of copying them')
    parser.add_argument('src', nargs='+', help='Sources files to sync')
    parser.add_argument('dest', nargs='?', help='Destination folder to sync (optional if --list-only is used)')

    args = parser.parse_args() # Parse the command line options and return the result
    if not args.src:
        parser.print_help()
        sys.exit(1)
    if not args.dest and not args.list_only:
        parser.print_help()
        sys.exit(1)
    return args


def getSrcs(sync):
    """
    Return the list of sources to sync
    """
    args = sync.args
    srcs = []
    if args.recursive:
        #get the absolute path of the base folder and add all files into srcs recursively
        for base_folder in args.src:
            base_folder = os.path.abspath(base_folder)
            if os.path.isdir(base_folder):
                for root, dirs, files in os.walk(base_folder):
                    for file in files:
                        srcs.append(os.path.join(root, file))
                        #print("Adding file %s to the list of files to sync" % os.path.join(root, file))
            else:
                print("Error: %s is not a directory" % base_folder)
    else:
        #get the absolute path of the base folder and add all files into srcs
        for base_folder in args.src:
            base_folder = os.path.abspath(base_folder)
            if os.path.isdir(base_folder):
                for file in os.listdir(base_folder):
                    srcs.append(os.path.join(base_folder, file))
                    #print("Adding file %s to the list of files to sync" % os.path.join(base_folder, file))
            elif os.path.isfile(base_folder): # if it's a file, just add it to the list case of * pass in parameter of SRC
                srcs.append(base_folder)
                #print("Adding file %s to the list of files to sync" % base_folder)
            else:
                print("Error: %s is not a directory" % base_folder)
    return srcs