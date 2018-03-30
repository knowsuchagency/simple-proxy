"""
Usage:  [OPTIONS] COMMAND [ARGS]...

  A cli for simple-proxy.

Options:
  --help  Show this message and exit.
"""
from pathlib import Path
import re
import os

import click


@click.group()
def cli():
    """A cli for simple-proxy."""
    pass


def add_dev_command(root_cmd):
    """
    Add development commands to package cli, if installed in editable mode.

    Args:
        root_cmd: the root cli command group
    """

    try:

        from run import main as development_tasks

        development_tasks.add_command(update_module_docstring)

        root_cmd.add_command(development_tasks, name='dev')

    except (ImportError, ModuleNotFoundError):
        pass


@click.command()
def update_module_docstring():
    """
    Replace cli module's docstring with the one generated from top-level cli entrypoint.

    we do this for the sake of having the module docstring reflect what the cli does
    which is useful particularly since sphinx will use the module's docstring in the
    package documentation it generates
    """

    # Return early if __doc__ is already the same as cli's docstring

    def transform_module_text(matchobj):
        """
        Return the text from the module with the docstring generated by click prepended to it.
        """
        with click.Context(cli) as ctx:
            docstring = os.linesep.join(['"""', ctx.get_help(), '"""'])

        return docstring + os.linesep + ''.join(matchobj.groups()[1:])

    patt = re.compile(r'(.*?)(from|import)(.*)', re.DOTALL | re.MULTILINE)

    original_module_text = Path(__file__).read_text()

    transformed_module_text = re.sub(
        patt,
        transform_module_text,
        original_module_text
    )

    with Path(__file__).open('w') as this_module:
        this_module.write(transformed_module_text)


def main(root_cmd=cli):
    add_dev_command(root_cmd)
    root_cmd()


if __name__ == "__main__":
    main()