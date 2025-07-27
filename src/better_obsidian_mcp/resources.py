import os

def example_outer(*args, **kwargs):
    VAULT_DIRECTORY = kwargs["vault_directory"]

    def example() -> str:
        """
        Read the example from the vault.
        """
        return "example"
    
    return example, "file://example/"
