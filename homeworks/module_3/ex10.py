def test_phrase():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, "Your phrase is 15 symbols or longer"


