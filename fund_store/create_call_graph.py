from datetime import datetime

from apis.dummy_dao import FUND_DATA
from app import create_app
from pycallgraph2 import Config
from pycallgraph2 import GlobbingFilter
from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput

todays_date = datetime.today().strftime("%Y-%m-%d")

graphviz = GraphvizOutput()
graphviz.output_file = f"call_graph-{todays_date}.png"

config = Config()
config.trace_filter = GlobbingFilter(
    include=[
        "apis.*",
        "app.*",
    ]
)

with PyCallGraph(output=graphviz, config=config):
    create_app(FUND_DATA)
