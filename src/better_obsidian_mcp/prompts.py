def test_outer(*args, **kwargs):
    def test(name: str):
        """
        This is a test prompt.
        """
        return f"test {name}"
    return test, "Prompt name"
