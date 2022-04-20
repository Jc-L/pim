import os

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import HTML

# local modules
from pimdata import *


class PimCompleter(Completer):
    def get_completions(self, document, complete_event):
        # print(document)
        yield Completion(
            'completion0', start_position=0,
            display=HTML('completion<ansired>0</ansired>'))
        yield Completion('new', start_position=0)
        yield Completion('delete', start_position=0)
        yield Completion('completion3', start_position=0)


class PimCli:

    def __init__(self):
        print('# PIM command line interface')
        while True:
            # TODO #1 Manage autocompletion
            # u = input("> ")
            # u = prompt('> ', completer=PimCompleter())
            u = prompt('> ')

            print(f'you type {u}')
