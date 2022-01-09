from django.core.management.base import BaseCommand
from shutil import copytree
import os

def join(*args):
    return os.path.join(*args)

def rename(old_name, new_name):
    os.rename(old_name, new_name)

def sed(to_replace, replace_with, fname):
    text = ""
    with open(fname) as file:
        text = file.read().replace(to_replace, replace_with)
    with open(fname + ".new", "w") as new_file:
        new_file.write(text)
    rename(fname + ".new", fname)

class Command(BaseCommand):
    help = "Add a new game to lamegames (locally)"

    def add_arguments(self, parser):
        parser.add_argument("game_name",type=str)

    def handle(self, *args, **options):
        # copy all info from skel into new directory
        copytree("skel", options["game_name"])
        # change any names including skel to options["game_name"]
        rename(
          join(options["game_name"], "static", "games", "skel.js"),
          join(options["game_name"], "static", "games", options["game_name"] + ".js")
        )
        rename(
          join(options["game_name"], "templates", "games", "skel.html"),
          join(options["game_name"], "templates", "games", options["game_name"] + ".html")
        )
        # change any mention of "skel" in files to options["game_name"]
        sed("skel.html", options["game_name"] + ".html", join(options["game_name"], "views.py"))
        sed("SkelConsumer", options["game_name"].capitalize() + "Consumer", join(options["game_name"], "consumers.py"))
        sed("skel", options["game_name"], join(options["game_name"], "urls.py"))
        sed("Skel", options["game_name"].capitalize(), join(options["game_name"], "urls.py"))
        sed("skel", options["game_name"], join(options["game_name"], "apps.py"))
        sed("SkelConfig", options["game_name"].capitalize() + "Config", join(options["game_name"], "apps.py"))
        self.stdout.write(self.style.SUCCESS("Started new game \"" + options["game_name"] + "\""))
