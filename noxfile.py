from __future__ import annotations

import shutil
from pathlib import Path

import nox

DIR = Path(__file__).parent.resolve()

nox.options.sessions = ["lint", "pylint", "tests", "build"]


@nox.session
def lint(session: nox.Session) -> None:
    """
    Run the linter.
    """
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session
def pylint(session: nox.Session) -> None:
    """
    Run PyLint.
    """
    # This needs to be installed into the package environment, and is slower
    # than a pre-commit check
    session.install(".", "pylint")
    session.run("pylint", "src", *session.posargs)


@nox.session
def tests(session: nox.Session) -> None:
    """
    Run the unit and regular tests. Use --cov to activate coverage.
    """
    session.install(".[dev]")
    session.run("pytest", *session.posargs)


@nox.session
def build(session: nox.Session) -> None:
    """
    Build an SDist and wheel.
    """

    build_p = DIR.joinpath("build")
    if build_p.exists():
        shutil.rmtree(build_p)

    session.install("build")
    session.run("python", "-m", "build")
