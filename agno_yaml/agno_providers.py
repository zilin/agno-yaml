AGNO_PROVIDERS = """
# Providers for Agno Framework
- type: python
  config: {}
  models:
    Gemini: 'agno.models.google.Gemini'
  tools:
    DuckDuckGoTools: 'agno.tools.duckduckgo.DuckDuckGoTools'
    YFinanceTools: 'agno.tools.yfinance.YFinanceTools'
    YouTubeTools: 'agno.tools.youtube.YouTubeTools'
    Newspaper4kTools: 'agno.tools.newspaper4k.Newspaper4kTools'
  agents:
    BasicAgent: 'agno.agent.Agent'
  teams:
    BasicTeam: 'agno.team.Team'
    CollaborateTeam: 'agno_yaml.agno_utils.CollaborateTeam'
    CoordinateTeam: 'agno_yaml.agno_utils.CoordinateTeam'
    RouteTeam: 'agno_yaml.agno_utils.RouteTeam'
  actions:
    PrintResponse: 'agno_yaml.agno_utils.print_response'
"""
