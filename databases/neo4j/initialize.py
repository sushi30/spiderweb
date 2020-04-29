import os

from dotenv import load_dotenv

load_dotenv()

from models.neo4j import *
from neomodel import install_all_labels, config

config.DATABASE_URL = os.environ["NEO4J_BOLT_URL"]


def main():

    install_all_labels()


if __name__ == "__main__":
    main()
