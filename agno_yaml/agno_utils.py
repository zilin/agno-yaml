from agno.agent import Agent
from agno.media import Image, Audio, Video
from agno.team.team import Team


def print_response(message: str, agent: Agent = None, team: Team = None, **kwargs) -> None:
    """Wrap agent.print_response as a lambda function."""

    # replace image/audio by Image/Video objects
    if 'images' in kwargs:
        kwargs['images'] = [Image(**image) for image in kwargs['images']]
    if 'audio' in kwargs:
        kwargs['audio'] = [Audio(**audio) for audio in kwargs['audio']]
    if 'videos' in kwargs:
        kwargs['videos'] = [Video(**video) for video in kwargs['videos']]
    if agent:
        return lambda: agent.print_response(message, **kwargs)
    elif team:
        return lambda: team.print_response(message, **kwargs)
    else:
        raise ValueError(
            'You need to specific "agent" or "team" in the example.')


def CollaborateTeam(**kwags):
    return Team(mode="collaborate", **kwags)


def CoordinateTeam(**kwags):
    return Team(mode="coordinate", **kwags)


def RouteTeam(**kwags):
    return Team(mode="route", **kwags)
