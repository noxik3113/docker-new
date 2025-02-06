import heroku3

def validate_heroku_api(api_key):
    """Validate the Heroku API key by making a test request."""
    try:
        heroku_conn = heroku3.from_key(api_key)
        # Test by listing apps (or any lightweight operation)
        heroku_conn.apps()
        return True
    except Exception as e:
        print(f"Validation error: {e}")
        return False

def list_heroku_apps(api_key):
    """List Heroku apps using the provided API key."""
    try:
        heroku_conn = heroku3.from_key(api_key)
        apps = heroku_conn.apps()
        return "\n".join([f"{app.name} - {app.stack}" for app in apps])
    except Exception as e:
        return f"❌ Error fetching apps: {e}"