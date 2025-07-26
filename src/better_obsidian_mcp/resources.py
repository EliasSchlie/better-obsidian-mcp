def test_outer(*args, **kwargs):
    def test(name: str):
        return f"test {name}"
    return test, "file://test/{name}"

def test2_outer(*args, **kwargs):
    def test2():
        return f"test2 inner text hi"
    return test2, "file://test2/"