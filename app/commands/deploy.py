
@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade

    # migrate database to latest revision
    upgrade()
