import pytest

from billing.dataclasses import BillingParameters, Credit


class TestInit:
    def test_palindrome_multiplier_is_negative__raises_value_error(self) -> None:
        with pytest.raises(ValueError):
            BillingParameters(
                BASE_CREDIT_COST=Credit.from_int(1),
                CHAR_CREDIT_COST=Credit.from_float(0.05),
                LENGTH_PENALTY_THRESHOLD=100,
                ONE_TO_THREE_WORD_LENGTH_COST=Credit.from_float(0.1),
                FOUR_TO_SEVEN_WORD_LENGTH_COST=Credit.from_float(0.2),
                EIGHT_PLUS_WORD_LENGTH_COST=Credit.from_float(0.3),
                LENGTH_PENALTY_CREDITS=Credit.from_int(5),
                UNIQUE_WORDS_BONUS=Credit.from_int(2),
                PALINDROME_MULTIPLIER=-2,
                VOWEL_COST=Credit.from_float(0.3),
            )

    def test_length_penalty_threshold_is_negative__raises_value_error(self) -> None:
        with pytest.raises(ValueError):
            BillingParameters(
                BASE_CREDIT_COST=Credit.from_int(1),
                CHAR_CREDIT_COST=Credit.from_float(0.05),
                LENGTH_PENALTY_THRESHOLD=-100,
                ONE_TO_THREE_WORD_LENGTH_COST=Credit.from_float(0.1),
                FOUR_TO_SEVEN_WORD_LENGTH_COST=Credit.from_float(0.2),
                EIGHT_PLUS_WORD_LENGTH_COST=Credit.from_float(0.3),
                LENGTH_PENALTY_CREDITS=Credit.from_int(5),
                UNIQUE_WORDS_BONUS=Credit.from_int(2),
                PALINDROME_MULTIPLIER=2,
                VOWEL_COST=Credit.from_float(0.3),
            )

    # TODO If more time, add all tests for type checks, but if we used pydantic we would get this for free.
