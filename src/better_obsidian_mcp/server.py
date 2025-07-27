from mcp.server.fastmcp import FastMCP
import os
import logging

import tools, resources, prompts

logging.basicConfig(level=logging.INFO)

VAULT_DIRECTORY = os.getenv("vault_directory")
MCP_RESOURCES_DIRECTORY = "mcp_resources"

mcp = FastMCP("better_obsidian_mcp")

for name, func in tools.__dict__.items():
    if name.endswith('_outer'):
        mcp.tool()(func(vault_directory=VAULT_DIRECTORY))

for name, func in resources.__dict__.items():
    if name.endswith('_outer'):
        func, uri = func(vault_directory=VAULT_DIRECTORY)
        mcp.resource(uri)(func)

# Automatically create resources for files in VAULT_DIRECTORY/MCP_RESOURCES_DIRECTORY/
resources_dir = os.path.join(VAULT_DIRECTORY, MCP_RESOURCES_DIRECTORY)
if os.path.exists(resources_dir) and os.path.isdir(resources_dir):
    for filename in os.listdir(resources_dir):
        file_path = os.path.join(resources_dir, filename)
        if os.path.isfile(file_path) and filename.lower().endswith('.md'):
            # Create a resource function for this file
            def create_resource_function(filepath, fname):
                def resource_func() -> str:
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            return f.read()
                    except FileNotFoundError:
                        return f"Resource file not found at: {filepath}"
                    except Exception as e:
                        return f"Error reading resource file {fname}: {str(e)}"
                
                resource_func.__doc__ = f"Content from '{fname}' in the '{MCP_RESOURCES_DIRECTORY}' directory."
                return resource_func
            
            # Create the resource function and register it
            resource_function = create_resource_function(file_path, filename)
            
            # Use filename (without extension) as the resource name, sanitized for URL
            resource_name = os.path.splitext(filename)[0]
            # Sanitize the resource name to be URL-safe
            import re
            sanitized_name = re.sub(r'[^a-zA-Z0-9_-]', '_', resource_name).strip('_')
            # Ensure it doesn't start with a number or underscore for better compatibility
            if sanitized_name and sanitized_name[0].isdigit():
                sanitized_name = f"file_{sanitized_name}"
            uri = f"file://{sanitized_name}/"
            
            mcp.resource(uri, name=filename, title=filename)(resource_function)

for name, func in prompts.__dict__.items():
    if name.endswith('_outer'):
        func, prompt_name = func()
        mcp.prompt(name=prompt_name)(func)

if __name__ == "__main__":
    mcp.run(transport='stdio')