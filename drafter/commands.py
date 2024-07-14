
import argparse
import drafter.llm_interface as interface
from colorama import Fore, Style


def iterate_draft():
    parser = argparse.ArgumentParser(
        description='Ask for current code project change.'
    )
    parser.add_argument(
        'command',
        type=str,
        nargs='?',
        help='Command to perform the code iteration.',
        default='.'
    )
    parser.add_argument(
        '--undo',
        action='store_true',
        help='Undo the last change.'
    )
    parser.add_argument(
        '--redo',
        action='store_true',
        help='Redo the last undone change.'
    )
    args = parser.parse_args()

    if args.undo:
        interface.undo_last_change()
    elif args.redo:
        interface.redo_last_change()
    else:
        response = interface.get_iteration(args.command)
        interface.format_output('Processing your request with a pinch of magic... 🌟', style=Style.BRIGHT, color=Fore.BLUE)
        interface.execute_response(response)

