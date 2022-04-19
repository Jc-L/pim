import os

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import HTML

# local modules
from pimdata import *


class MyCustomCompleter(Completer):
    def get_completions(self, document, complete_event):
        print(document)
        yield Completion(
            'completion0', start_position=0,
            display=HTML('<b>completion</b><ansired>0</ansired>'),
            style='bg:ansiyellow')

        # Display this completion, black on yellow.
        yield Completion('completion1', start_position=0,
                         style='bg:ansiyellow fg:ansiblack')

        # Underline completion.
        yield Completion('completion2', start_position=0,
                         style='underline')

        # Specify class name, which will be looked up in the style sheet.
        yield Completion('completion3', start_position=0,
                         style='class:special-completion')

class PimCli:

    def __init__(self):
        print('# PIM command line interface')
        while True:
            # TODO #1 Manage autocompletion
            # u = input("> ")
            u = prompt('> ', completer=MyCustomCompleter())

            print(f'you type {u}')
