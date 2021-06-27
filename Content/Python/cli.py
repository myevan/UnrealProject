import pb.platforms
import click

@click.group()
def cli():
    pass

@cli.command()
def dbc_build():
    from pb.tools.dbc_tool import DBCTool
    from pb.env import Environment
    env = Environment()
    DBCTool().build(env.csv_root_path, env.dbc_root_path)

if __name__ == '__main__':
    cli.main()
