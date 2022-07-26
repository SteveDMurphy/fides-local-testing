import nox

nox.options.sessions = []


@nox.session()
def fides_db(session: nox.Session) -> None:
    """Spin up the local database for fidesctl"""
    session.run(
        "docker",
        "compose",
        "up",
        "-d",
        "fidesctl-db",
        external=True,
    )


@nox.session()
def teardown(session: nox.Session) -> None:
    """Spin up the local database for fidesctl"""
    session.run(
        "docker",
        "compose",
        "down",
        external=True,
    )
