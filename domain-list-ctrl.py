# Imports

from sqlite3 import connect
from argparse import ArgumentParser,ArgumentDefaultsHelpFormatter
from re import match,compile

# Regex argument check

arg_check = compile('(?P<active>enabled)|(?P<inactive>disabled)')

# Service Parameters

db_path = '/etc/pihole/gravity.db'

# Get Argument from CLI

def getArg():
    parser = ArgumentParser(
        description="Change blacklist/whitelist state in Gravity",
        formatter_class=ArgumentDefaultsHelpFormatter
                )
    parser.add_argument(
        "state",
        help="Select state: enabled/disabled"
                )
    parser.add_argument(
        "-c",'--comment_groups',
        default=[],
        nargs='*',
        help=(
            "Select mapped comment as a flag"
            " on the basis of which to change the status"
            )
                    )
    args = parser.parse_args()
    pair = vars(args)
    value_match = match(arg_check,pair['state'])
    if value_match:
        if value_match.group('active'):
            return str(1), pair['comment_groups']
        elif value_match.group('inactive'):
            return str(0), pair['comment_groups']
    else:
        print('Invalid argument')
        exit()

# Make changes to Gravity.DB: 'domainlist' table

def dbConnect(gravity_path,comment_flag_list,state):
    if comment_flag_list == []:
        print(
            '\nEmpty comment field, reffer to /path/domain-list-ctrl.py --help'
            '\n[-c OPTIONAL ARGUMENT]\n\nExiting programm\n')
        exit()
    db_connection = connect(gravity_path)
    db_cursor = db_connection.cursor()
    for each_comment in comment_flag_list:
        db_cursor.execute(
            "UPDATE domainlist SET enabled = "
            "{0} WHERE comment = '{1}'".format(state,each_comment))
    db_connection.commit()

# Main

if __name__ == "__main__":

    working_state,comment_group_list = getArg()
    dbConnect(db_path,comment_group_list,working_state)
