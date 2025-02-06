import docker
import zipfile
import os
from telegram import InputFile

client = docker.from_env()

def download_and_run_container(app_name, api_key):
    """Download the Heroku registry image and run it as a container."""
    try:
        # Authenticate with Heroku Docker registry
        client.login(
            username="ignored",  # Heroku Docker registry doesn't use a username
            password=api_key,
            registry="registry.heroku.com"
        )

        # Pull the image
        image_name = f"registry.heroku.com/{app_name}/worker"
        client.images.pull(image_name)

        # Run the container
        container = client.containers.run(image_name, detach=True)
        return container.id
    except Exception as e:
        print("Error running container: {}".format(e))
        return None

def zip_and_send_files(update, context, app_name):
    """Zip files in /app folder and send them to the user."""
    try:
        zip_filename = f"{app_name}_files.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for root, _, files in os.walk("/app"):
                for file in files:
                    zipf.write(os.path.join(root, file))

        # Send the zip file to the user
        with open(zip_filename, 'rb') as file:
            context.bot.send_document(chat_id=update.message.chat_id, document=InputFile(file))
    except Exception as e:
        print("Error zipping and sending files: {}".format(e))
