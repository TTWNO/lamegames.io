from django.core.management.base import BaseCommand
from shutil import copytree

class Command(BaseCommand):
    help = "Add a new game to lamegames (locally)"

    def add_arguments(self, parser):
        parser.add_argument("game_name",type=str)

    def handle(self, *args, **options):
        # copy all info from skel into new directory
        copytree("skel", options["game_name"])
        # change any names including skel to options["game_name"]
        # change any mention of "skel" in files to options["game_name"]
