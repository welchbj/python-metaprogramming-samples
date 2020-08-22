"""A simple framework for automatically creating CLIs from functions."""

from __future__ import annotations

import inspect
import sys

from argparse import ArgumentParser
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Type


class Application:

    @classmethod
    def func_to_parser(cls: Type[Application], func: Callable) -> ArgumentParser:
        parser = ArgumentParser(
            prog=func.__name__,
            description=func.__doc__
        )

        for _, param in inspect.signature(func).parameters.items():
            cls.add_param_to_parser(param, parser)

        return parser

    @classmethod
    def add_func_to_subparser(
        cls: Type[Application], func: Callable, subparser: ArgumentParser
    ) -> None:
        for _, param in inspect.signature(func).parameters.items():
            cls.add_param_to_parser(param, subparser)

    @classmethod
    def add_param_to_parser(
        cls: Type[Application], param: inspect.Parameter, parser: ArgumentParser
    ) -> None:
        if param.kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY,):
            kwargs: Dict[str, Any] = {}

            if param.default is not inspect.Parameter.empty:
                kwargs['default'] = param.default
                kwargs['required'] = False

            if param.annotation is not inspect.Parameter.empty:
                if param.annotation is bool:
                    kwargs['action'] = 'store_true'
                else:
                    kwargs['type'] = param.annotation

            flag_name = cls.arg_to_flag_name(param.name)
            parser.add_argument(flag_name, **kwargs)
        elif param.kind == param.POSITIONAL_ONLY:
            raise ValueError('Positional-only arguments not supported')
        elif param.kind == param.VAR_POSITIONAL:
            raise ValueError('*args-like arguments not supported')
        elif param.kind == param.VAR_KEYWORD:
            raise ValueError('**kwargs-like arguments not supported')
        else:
            raise ValueError('This should be unreachable')

    @staticmethod
    def arg_to_flag_name(arg_name: str) -> str:
        flagitized_arg_name = arg_name.lstrip('-').replace('_', '-')
        return f'--{flagitized_arg_name}'

    def __init__(self) -> None:
        self.config: Dict[str, Any] = {}

        self.top_level_func: Optional[Callable] = None
        self.cmd_funcs: Dict[str, Callable] = {}

    def top_level(self, func: Callable) -> Callable:
        """Decorator to add top-level flags for the application."""

        if self.top_level_func is not None:
            raise ValueError('Tried to set multiple @top_level functions')

        self.top_level_func = func

        @wraps(func)
        def decorated(*args, **kwargs):
            return func(*args, **kwargs)

        return decorated

    def cmd(self, func: Callable) -> Callable:
        """Decorator to add a sub-command (and its flags) for the application."""

        if func.__name__ in self.cmd_funcs.keys():
            raise ValueError('Tried to register functions with the same name')
        self.cmd_funcs[func.__name__] = func

        @wraps(func)
        def decorated(*args, **kwargs):
            return func(*args, **kwargs)

        return decorated

    def run(self, args: Optional[List[str]] = None) -> None:
        if self.top_level_func is None:
            raise ValueError('Need a @top_level function')

        parser = self.__class__.func_to_parser(self.top_level_func)

        # Add sub-parsers if there are other registered commands.
        if self.cmd_funcs:
            subparsers = parser.add_subparsers(dest='__framework_func_name__')

            # Enumerate over sub-commands, making sub-parsers for each of them.
            for cmd_name, func in self.cmd_funcs.items():
                subparser = subparsers.add_parser(cmd_name)
                self.__class__.add_func_to_subparser(func, subparser)

        if args is None:
            args = sys.argv[1:]

        parsed_args = parser.parse_args(args)

        cmd_options = ', '.join(sorted(self.cmd_funcs.keys()))

        func_name = parsed_args.__framework_func_name__
        if func_name is None:
            raise ValueError(f'A sub-command is required! Pick from: {cmd_options}')

        chosen_cmd_func: Optional[Callable] = self.cmd_funcs.get(func_name, None)
        if chosen_cmd_func is None:
            raise ValueError(
                f'Invalid sub-command {func_name}! Pick from: {cmd_options}'
            )

        # Separate arguments between the @top_level function and the chosen command.
        # This is a fragile way of doing this and assumes no shared argument names
        # between the @top_level function and chosen command, and also relies on the
        # fact that no *args or positional-only arguments are permitted.
        arg_dict = vars(parsed_args)
        top_level_arg_names = inspect.signature(self.top_level_func).parameters.keys()
        top_level_kwargs = {
            k: v for k, v in arg_dict.items() if k in top_level_arg_names
        }
        cmd_func_arg_names = inspect.signature(chosen_cmd_func).parameters.keys()
        cmd_func_kwargs = {
            k: v for k, v in arg_dict.items() if k in cmd_func_arg_names
        }

        self.top_level_func(**top_level_kwargs)
        chosen_cmd_func(**cmd_func_kwargs)
