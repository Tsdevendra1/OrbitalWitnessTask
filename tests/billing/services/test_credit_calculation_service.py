from decimal import Decimal

import pytest

from billing.constants import DEFAULT_BILLING_PARAMETERS
from billing.dataclasses import BillingParameters, Credit
from billing.services.credit_calculation_service import (
    CalculateCreditsService,
    character_count_rule,
    length_penalty_rule,
    palindrome_bonus_rule,
    unique_words_bonus_rule,
    vowels_bonus_rule,
    word_length_multiplier_rule,
)


@pytest.fixture
def default_parameters() -> BillingParameters:
    return DEFAULT_BILLING_PARAMETERS


class TestCharacterCountRule:
    def test_empty_string__returns_zero_credits(self, default_parameters: BillingParameters) -> None:
        assert character_count_rule("", default_parameters) == Credit.zero()

    def test_three_chars__returns_expected_credit(self, default_parameters: BillingParameters) -> None:
        assert character_count_rule("abc", default_parameters) == Credit(amount=Decimal("0.15"))

    def test_string_with_spaces__includes_spaces_in_count(self, default_parameters: BillingParameters) -> None:
        assert character_count_rule("a b c", default_parameters) == Credit(amount=Decimal("0.25"))


class TestWordLengthMultiplierRule:
    def test_short_word__returns_small_multiplier(self, default_parameters: BillingParameters) -> None:
        assert word_length_multiplier_rule("cat", default_parameters) == Credit(amount=Decimal("0.1"))

    def test_medium_word__returns_medium_multiplier(self, default_parameters: BillingParameters) -> None:
        assert word_length_multiplier_rule("hello", default_parameters) == Credit(amount=Decimal("0.2"))

    def test_long_word__returns_large_multiplier(self, default_parameters: BillingParameters) -> None:
        assert word_length_multiplier_rule("beautiful", default_parameters) == Credit(amount=Decimal("0.3"))

    def test_multiple_words__returns_sum_of_multipliers(self, default_parameters: BillingParameters) -> None:
        assert word_length_multiplier_rule("cat hello beautiful", default_parameters) == Credit(amount=Decimal("0.6"))

    def test_non_word__returns_zero(self, default_parameters: BillingParameters) -> None:
        assert word_length_multiplier_rule("123", default_parameters) == Credit.zero()


class TestLengthPenaltyRule:
    def test_short_text__returns_no_penalty(self, default_parameters: BillingParameters) -> None:
        assert length_penalty_rule("short", default_parameters) == Credit.zero()

    def test_text_exceeding_threshold__returns_penalty(self, default_parameters: BillingParameters) -> None:
        long_text = "x" * 101
        assert length_penalty_rule(long_text, default_parameters) == Credit.from_int(5)

    def test_text_at_threshold__returns_no_penalty(self, default_parameters: BillingParameters) -> None:
        threshold_text = "x" * 100
        assert length_penalty_rule(threshold_text, default_parameters) == Credit.zero()


class TestUniqueWordsBonus:
    def test_all_unique_words__returns_bonus(self, default_parameters: BillingParameters) -> None:
        assert unique_words_bonus_rule("hello world", default_parameters) == Credit.from_int(2)

    def test_repeated_words__returns_no_bonus(self, default_parameters: BillingParameters) -> None:
        assert unique_words_bonus_rule("hello hello world", default_parameters) == Credit.zero()

    def test_empty_string__returns_no_bonus(self, default_parameters: BillingParameters) -> None:
        assert unique_words_bonus_rule("", default_parameters) == Credit.zero()

    def test_case_sensitive_words__considered_unique(self, default_parameters: BillingParameters) -> None:
        assert unique_words_bonus_rule("Hello hello", default_parameters) == Credit.from_int(2)


class TestVowelsBonus:
    def test_third_position_vowels__returns_bonus_per_vowel(self, default_parameters: BillingParameters) -> None:
        assert vowels_bonus_rule("abedfI", default_parameters) == Credit(amount=Decimal("0.6"))

    def test_no_third_position_vowels__returns_zero(self, default_parameters: BillingParameters) -> None:
        assert vowels_bonus_rule("xyz", default_parameters) == Credit.zero()

    def test_mixed_case_vowels__returns_bonus(self, default_parameters: BillingParameters) -> None:
        assert vowels_bonus_rule("abE", default_parameters) == Credit(amount=Decimal("0.3"))


class TestPalindromeBonus:
    def test_simple_palindrome__returns_multiplier(self, default_parameters: BillingParameters) -> None:
        assert palindrome_bonus_rule("radar", default_parameters) == 2

    def test_complex_palindrome_with_spaces__returns_multiplier(self, default_parameters: BillingParameters) -> None:
        assert palindrome_bonus_rule("A man a plan a canal Panama", default_parameters) == 2

    def test_non_palindrome__returns_one(self, default_parameters: BillingParameters) -> None:
        assert palindrome_bonus_rule("hello world", default_parameters) == 1

    def test_non_alphanumeric_palindrome__returns_one(self, default_parameters: BillingParameters) -> None:
        assert palindrome_bonus_rule("!!!!!!", default_parameters) == 1

    def test_empty_string__returns_one(self, default_parameters: BillingParameters) -> None:
        assert palindrome_bonus_rule("", default_parameters) == 1


class TestCalculateCredits:
    def test_empty_string__returns_expected_credit(self, default_parameters: BillingParameters) -> None:
        # Base cost: 1
        # Character count: 0
        # Word length: 0
        # Vowels: 0
        # Length penalty: 0
        # Unique words: 0
        # Not Palindrome: 1
        # Total: *1 + 0 + 0 + 0 + 0 + 0) * 1 = 1
        assert CalculateCreditsService(default_parameters).calculate_credits("") == Credit.from_int(1)

    def test_less_than_one_expected_credit__always_returns_at_least_one_credit(
        self, default_parameters: BillingParameters
    ) -> None:
        # Calculation
        # Base cost: 1
        # Character count (2 chars * 0.05): 0.1
        # Word length (1 word * 0.1 for 2-letter words): 0.1
        # Vowels: 0
        # No length penalty
        # Unique words bonus: -2
        # Palindrome: 2
        # Total: (1 + 0.1 + 0.1 - 2) * 2 = 0.4
        assert CalculateCreditsService(default_parameters).calculate_credits("hi") == Credit(amount=Decimal("1"))

    def test_palindrome_text__returns_doubled_credits(self, default_parameters: BillingParameters) -> None:
        # Calculation
        # Base cost: 1
        # Character count (7 chars * 0.05): 0.35
        # Word length: 2 * 0.1 = 0.2
        # Vowels: 0.3 (position 6)
        # No length penalty: 0
        # Unique words bonus: 0
        # Palindrome: 2
        # Total: (1 + 0.35 + 0.2 + 0.3) * 2 = 3.7

        text = "wow wow"
        result = CalculateCreditsService(default_parameters).calculate_credits(text)
        assert result == Credit.from_float(3.7)
