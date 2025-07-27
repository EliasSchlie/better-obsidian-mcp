import os

def example_outer_(*args, **kwargs): # Remove the last _ to make it be picked up by the server

    def example() -> str:
        """
        Read the example from the vault.
        """
        return "example"
    
    return example, "file://example/"
