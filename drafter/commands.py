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
        help='Command to perform the code iteration.',
        default='.'
    )
    args = parser.parse_args()
    response = interface.get_iteration(args.command)
    interface.format_output('Processing response with a pinch of magic... 🌟', style=Style.BRIGHT, color=Fore.BLUE)
    interface.execute_response(response)

