import ast
import os
from pathlib import Path

"""
Goes through all the files in config/fund_loader_config/FAB and adds each round to FAB_FUND_ROUND_CONFIGS

Each file in that directory needs to be python format as per the FAB exports,
containing one property called LOADER_CONFIG
See test_fab_round_config.py for example
"""

FAB_FUND_ROUND_CONFIGS = {}

this_dir = Path("config") / "fund_loader_config" / "FAB"

for file in os.listdir(this_dir):
    if "__" in file.title():
        continue
    with open(this_dir / file, "r") as json_file:

        content = json_file.read().split("LOADER_CONFIG=")[1]
        loader_config = ast.literal_eval(content)
        if not loader_config.get("fund_config", None):
            print("No fund config found in the loader config.")
            raise ValueError(f"No fund_config found in {file}")
        if not loader_config.get("round_config", None):
            print("No round config found in the loader config.")
            raise ValueError(f"No round_config found in {file}")
        fund_short_name = loader_config["fund_config"]["short_name"]
        round_short_name = loader_config["round_config"]["short_name"]
        FAB_FUND_ROUND_CONFIGS[fund_short_name] = loader_config["fund_config"]
        if not FAB_FUND_ROUND_CONFIGS[fund_short_name].get("rounds", None):
            FAB_FUND_ROUND_CONFIGS[fund_short_name]["rounds"] = {}
        FAB_FUND_ROUND_CONFIGS[fund_short_name]["rounds"][round_short_name] = loader_config["round_config"]
        FAB_FUND_ROUND_CONFIGS[fund_short_name]["rounds"][round_short_name]["sections_config"] = loader_config[
            "sections_config"
        ]
        FAB_FUND_ROUND_CONFIGS[fund_short_name]["rounds"][round_short_name]["base_path"] = loader_config["base_path"]
