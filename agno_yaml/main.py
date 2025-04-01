from agno_yaml.yaml_loader import load_yaml_specs
from dotenv import load_dotenv

def main():
    import argparse

    parser = argparse.ArgumentParser(
        prog='Ango YAML',
        description='A command line tool to load models, tools, agents from a YAML file')
    parser.add_argument(
        '--providers_yaml_file',
        default=None,
        help='A file containing a yaml description of providers for Ango framework.')
    parser.add_argument(
        '--yaml_file',
        default='examples/agent_with_tools.yaml',
        help='A file containing a yaml description of Ango entities.')
    parser.add_argument(
        '--example',
        default='default',
        help='The name of example to run.')
    parser.add_argument(
        '--agent',
        default=None,
        help='The name of agent.')
    parser.add_argument(
        '--team',
        default=None,
        help='The name of team.')
    parser.add_argument(
        '--query',
        default=None,
        help='A query.')
    parser.add_argument(
        '--start_playground',
        action="store_true",
        help='Will start playgroud if true.')
    args = parser.parse_args()

    load_dotenv()
    agno_yaml = load_yaml_specs(args.yaml_file, args.providers_yaml_file)

    if args.start_playground:
        from agno import playground
        # force to load all agents.
        agents = [agno_yaml.agents[k] for k in agno_yaml.agents.keys()]
        app = playground.Playground(agents=agents).get_app()
        playground.serve_playground_app(app)
    elif args.agent and args.query:
        if args.agent in agno_yaml.agents:
            agent = agno_yaml.agents[args.agent]
            agent.print_response(args.query)
        else:
            raise ValueError('Cannot find agent %s in %s' %
                             (args.agent, args.yaml_file))
    elif args.team and args.query:
        if args.team in agno_yaml.teams:
            team = agno_yaml.teams[args.team]
            team.print_response(args.query)
        else:
            raise ValueError('Cannot find team %s in %s' %
                             (args.team, args.yaml_file))
    elif args.example:
        if args.example in agno_yaml.examples:
            example = agno_yaml.examples[args.example]
            example()
        else:
            raise ValueError('Cannot find example %s in %s' %
                             (args.example, args.yaml_file))


if __name__ == '__main__':
    main()
