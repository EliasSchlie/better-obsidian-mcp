from mcp.server.fastmcp import FastMCP
import os
import logging

import tools, resources, prompts

logging.basicConfig(level=logging.INFO)

VAULT_DIRECTORY = os.getenv("vault_directory")

mcp = FastMCP("better_obsidian_mcp")

for name, func in tools.__dict__.items():
    if name.endswith('_outer'):
        mcp.tool()(func(directory=VAULT_DIRECTORY))

for name, func in resources.__dict__.items():
    if name.endswith('_outer'):
        func, uri = func()
        mcp.resource(uri)(func)

for name, func in prompts.__dict__.items():
    if name.endswith('_outer'):
        func, prompt_name = func()
        mcp.prompt(name=prompt_name)(func)

if __name__ == "__main__":
    mcp.run(transport='stdio')