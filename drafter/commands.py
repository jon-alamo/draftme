import argparse
import drafter.llm_interface as interface


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
    interface.execute_response(response)
