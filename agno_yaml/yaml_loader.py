import os.path
from typing import NamedTuple
import importlib
import yaml
from agno_yaml.agno_providers import AGNO_PROVIDERS


class Providers(NamedTuple):
    """Data model to hold provider spec."""
    models: dict
    tools: dict
    agents: dict
    teams: dict
    actions: dict


def parse_providers(provider_specs, providers=None):
    """Parse providers spec from a YAML file."""
    if providers is None:
        providers = Providers(models={}, tools={},
                              agents={}, teams={}, actions={})
    for provider_spec in provider_specs:
        if 'models' in provider_spec:
            for name, constructor in provider_spec['models'].items():
                providers.models[name] = constructor
        if 'tools' in provider_spec:
            for name, constructor in provider_spec['tools'].items():
                providers.tools[name] = constructor
        if 'agents' in provider_spec:
            for name, constructor in provider_spec['agents'].items():
                providers.agents[name] = constructor
        if 'teams' in provider_spec:
            for name, constructor in provider_spec['teams'].items():
                providers.teams[name] = constructor
        if 'actions' in provider_spec:
            for name, constructor in provider_spec['actions'].items():
                providers.actions[name] = constructor
    return providers


def parse_models(model_specs, providers):
    """Parse model specs."""
    for model_spec in model_specs:
        name = model_spec['name']
        typ = model_spec['type']
        constructor = providers.models[typ]
        config = model_spec['config']
        yield name, (constructor, config)


def parse_tools(tool_specs, providers):
    """Parse tool specs."""
    for tool_spec in tool_specs:
        name = tool_spec['name']
        typ = tool_spec['type']
        constructor = providers.tools[typ]
        config = tool_spec['config']
        yield name, (constructor, config)


def parse_agents(agent_specs, providers, provided_models, provided_tools):
    """Parse agent specs."""
    for agent_spec in agent_specs:
        name = agent_spec['name']
        typ = agent_spec['type']
        constructor = providers.agents[typ]
        config = agent_spec['config']
        config['name'] = name
        # load model
        if 'model' in config:
            model_name = config['model']
            if model_name in provided_models:
                config['model'] = provided_models[model_name]
            else:
                raise ValueError("Unknown model %s" % model_name)
        else:
            raise ValueError("Agent %s has no model configured." % name)
        # load tools
        if 'tools' in config:
            tools = []
            for tool_name in config['tools']:
                if tool_name in provided_tools:
                    tool_instance = provided_tools[tool_name]
                    tools.append(tool_instance)
                else:
                    raise ValueError("Unknow tool '%s'" % tool_name)
            config['tools'] = tools
        yield name, (constructor, config)


def parse_teams(team_specs, providers, provided_models, provided_agents):
    """Parse team specs."""
    for team_spec in team_specs:
        name = team_spec['name']
        typ = team_spec['type']
        constructor = providers.teams[typ]
        config = team_spec['config']
        config['name'] = name
        # load model
        if 'model' in config:
            model_name = config['model']
            if model_name in provided_models:
                config['model'] = provided_models[model_name]
            else:
                raise ValueError("Unknown model %s" % model_name)
        else:
            raise ValueError("Agent %s has no model configured." % name)
        # load agent
        if "members" in config:
            members = []
            for agent_name in config['members']:
                if agent_name in provided_agents:
                    members.append(provided_agents[agent_name])
                else:
                    raise ValueError("Unknow agent '%s'" % agent_name)
            config['members'] = members
        yield name, (constructor, config)


def parse_examples(example_specs, providers, provided_agents, provided_teams):
    """Parse example specs."""
    for example_spec in example_specs:
        name = example_spec['name']
        typ = example_spec['type']
        constructor = providers.actions[typ]
        config = example_spec['config']
        if 'agent' in config and 'team' in config:
            raise ValueError(
                'You cannot specify both "agent" and "team" in example %s' % name)
        if 'agent' not in config and 'team' not in config:
            raise ValueError(
                'You need specify "agent" or "team" in example %s' % name)
        if 'agent' in config:
            agent_name = config['agent']
            if agent_name in provided_agents:
                config['agent'] = provided_agents[agent_name]
            else:
                raise ValueError('Cannot find agent %s' % agent_name)
        elif 'team' in config:
            team_name = config['team']
            if team_name in provided_teams:
                config['team'] = provided_teams[team_name]
            else:
                raise ValueError('Cannot find team %s' % team_name)
        yield name, (constructor, config)


def _load_from_fully_qualified_name(fully_qualified_name):
    """Load a python object from a fully qualified name."""
    o = None
    path = ''
    for segment in fully_qualified_name.split('.'):
        path = '.'.join([path, segment]) if path else segment
        if o is not None and hasattr(o, segment):
            o = getattr(o, segment)
        else:
            o = importlib.import_module(path)
    return o


class LazyDict(dict):
    """A dictionary will be lazy to constructor a python object only when first load."""

    def __getitem__(self, key):
        val = dict.__getitem__(self, key)
        if isinstance(val, tuple):
            constructor, config = val
            factory_fn = _load_from_fully_qualified_name(constructor)
            dict.__setitem__(self, key, factory_fn(**config))
            return dict.__getitem__(self, key)
        else:
            return val


class AgnoYaml(NamedTuple):
    """Data model to hold entities defined in Argno YAML file."""
    models: LazyDict
    tools: LazyDict
    agents: LazyDict
    teams: LazyDict
    examples: LazyDict


def load_yaml_spec(yaml_spec, yaml_path='', providers=None):
    """Load entities from a YAML spec file."""
    providers = parse_providers(yaml_spec.get('providers', []), providers)
    models = LazyDict()
    for name, instance in parse_models(yaml_spec.get('models', []), providers):
        models[name] = instance
    tools = LazyDict()
    for name, instance in parse_tools(yaml_spec.get('tools', []), providers):
        tools[name] = instance
    agents = LazyDict()
    for name, instance in parse_agents(yaml_spec.get('agents', []), providers, models, tools):
        agents[name] = instance
    teams = LazyDict()
    for name, instance in parse_teams(yaml_spec.get('teams', []), providers, models, agents):
        teams[name] = instance
    examples = LazyDict()
    for name, instance in parse_examples(yaml_spec.get('examples', []), providers, agents, teams):
        examples[name] = instance
    return AgnoYaml(models=models, tools=tools, agents=agents, teams=teams, examples=examples)


def load_yaml_file(yaml_file: str):
    """Parses the YAML file into a dictionary."""
    with open(yaml_file, 'r') as f:
        yaml_str = f.read()
        try:
            return yaml.safe_load(yaml_str)
        except yaml.YAMLError as e:
            raise ValueError(f'Error parsing YAML: {e}') from e


def load_yaml_specs(yaml_file, providers_yaml_file=None):
    """Load yaml file and providers yaml file."""
    if providers_yaml_file:
        providers_yaml_spec = load_yaml_file(providers_yaml_file)
    else:
        providers_yaml_spec = yaml.safe_load(AGNO_PROVIDERS)
    providers = parse_providers(providers_yaml_spec)
    yaml_path = os.path.dirname(yaml_file)
    yaml_spec = load_yaml_file(yaml_file)
    return load_yaml_spec(yaml_spec, yaml_path, providers)
