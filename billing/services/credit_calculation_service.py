from billing.dataclasses import BillingParameters, Credit
from billing.utils import get_valid_words


def character_count_rule(text: str, parameters: BillingParameters) -> Credit:
    """
    Assumption: It says each "character", so I'm assuming it's counting spaces and punctuation as well. Same applies
    to the other rules that count characters.
    """
    return parameters.CHAR_CREDIT_COST * len(text)


def word_length_multiplier_rule(text: str, parameters: BillingParameters) -> Credit:
    credits = Credit.zero()
    for word in get_valid_words(text):
        if 1 <= len(word) <= 3:
            credits += parameters.ONE_TO_THREE_WORD_LENGTH_COST
        elif 4 <= len(word) <= 7:
            credits += parameters.FOUR_TO_SEVEN_WORD_LENGTH_COST
        else:
            credits += parameters.EIGHT_PLUS_WORD_LENGTH_COST

    return credits


def length_penalty_rule(text: str, parameters: BillingParameters) -> Credit:
    if len(text) > parameters.LENGTH_PENALTY_THRESHOLD:
        return parameters.LENGTH_PENALTY_CREDITS
    return Credit.zero()


def unique_words_bonus_rule(text: str, parameters: BillingParameters) -> Credit:
    # Assumption: Only consider valid words when checking for uniqueness, not the entire text.
    words = get_valid_words(text)
    if len(words) > 0 and len(words) == len(set(words)):
        return parameters.UNIQUE_WORDS_BONUS
    return Credit.zero()


def vowels_bonus_rule(text: str, parameters: BillingParameters) -> Credit:
    credits = Credit.zero()
    for i, char in enumerate(text):
        if char in parameters.VOWELS and (i + 1) % 3 == 0:
            credits += parameters.VOWEL_COST
    return credits


def palindrome_bonus_rule(text: str, parameters: BillingParameters) -> int:
    # Assumption: empty string are not considered palindromes
    cleaned_text = "".join(c for c in text if c.isalnum()).lower()
    if cleaned_text and cleaned_text == cleaned_text[::-1]:
        return parameters.PALINDROME_MULTIPLIER
    return 1


class CalculateCreditsService:
    def __init__(self, parameters: BillingParameters) -> None:
        """
        Decision #1: pass billing parameters as an argument instead of using a global variable. This makes the code more
        flexible and easier to test. As well as allowing different parameters for different customers.

        Decision #2: function vs class. I chose a class in the end. I think perhaps it might be overkill here. The benefit
        of going with a class is that in the UsageService we could inject a mock version of this class for testing and
        also have different versions of calculating credits. There is trade-off here in terms of complexity and
        simplicity. I think either solution would work and would depend on what the team thinks in a real-world scenario.

        Decision #3: Keeping the rules as their own functions vs private methods on the class. I think this is a good
        separation of concerns. It makes the rules easier to test and also easier to understand. If the rules were private
        methods on the class, it would be harder to test them individually. Again something I think the team would need to
        decide on in a real-world scenario.
        """
        self.parameters = parameters

    def calculate_credits(self, text: str) -> Credit:
        credits = self.parameters.BASE_CREDIT_COST
        credits += character_count_rule(text, self.parameters)
        credits += word_length_multiplier_rule(text, self.parameters)
        credits += vowels_bonus_rule(text, self.parameters)
        credits += length_penalty_rule(text, self.parameters)
        credits -= unique_words_bonus_rule(text, self.parameters)
        credits *= palindrome_bonus_rule(text, self.parameters)

        # Remember to always return at least 1 credit
        return max(credits, Credit.from_int(1))
