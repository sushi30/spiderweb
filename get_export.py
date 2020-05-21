import click
import boto3

cloudformation = boto3.client("cloudformation")

@click.command()
@click.argument("export_name")
def main(export_name):
    print(
        [
            e
            for e in cloudformation.list_exports()["Exports"]
            if e["Name"] == export_name
        ][0]["Value"]
    )


if __name__ == "__main__":
    main()
