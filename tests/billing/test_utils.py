from billing.utils import is_word


class TestIsWord:
    def test_all_lowercase__returns_true(self) -> None:
        assert is_word("test")

    def test_mixed_case__returns_true(self) -> None:
        assert is_word("TeSt")

    def test_all_uppercase__returns_true(self) -> None:
        assert is_word("TEST")

    def test_empty_string__returns_false(self) -> None:
        assert not is_word("")

    def test_whitespace_only__returns_false(self) -> None:
        assert not is_word("   ")

    def test_leading_whitespace__returns_false(self) -> None:
        assert not is_word(" test")

    def test_trailing_whitespace__returns_false(self) -> None:
        assert not is_word("test ")

    def test_special_characters__returns_false(self) -> None:
        assert not is_word("test!")

    def test_hypenated_word__returns_true(self) -> None:
        assert is_word("test-test")

    def test_multiple_hyphenated_words__returns_true(self) -> None:
        assert is_word("test-test-test")

    def test_apostrophe_word__returns_true(self) -> None:
        assert is_word("test's")

    def test_unicode_letters__returns_true(self) -> None:
        assert is_word("résumé")

    # TODO: I'm sure there are many other tests I could do but I'll leave at this for now.
