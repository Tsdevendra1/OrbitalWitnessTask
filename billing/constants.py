from billing.dataclasses import BillingParameters, Credit

# Decision: I've hard coded this here but in a real-world scenario, this would be stored in a configuration file/database/environment variable and set at a higher level.
BASE_SERVICE_URL = "https://owpublic.blob.core.windows.net/tech-task"
# Decision: I'm using a global variable for the default billing parameters. This is a simple application and we don't need
# to worry about different customers having different parameters. If we need to support different parameters in the future,
# we can always refactor this to use a database or configuration file to store the parameters.
DEFAULT_BILLING_PARAMETERS = BillingParameters(
    BASE_CREDIT_COST=Credit.from_int(1),
    CHAR_CREDIT_COST=Credit.from_float(0.05),
    LENGTH_PENALTY_THRESHOLD=100,
    ONE_TO_THREE_WORD_LENGTH_COST=Credit.from_float(0.1),
    FOUR_TO_SEVEN_WORD_LENGTH_COST=Credit.from_float(0.2),
    EIGHT_PLUS_WORD_LENGTH_COST=Credit.from_float(0.3),
    LENGTH_PENALTY_CREDITS=Credit.from_int(5),
    UNIQUE_WORDS_BONUS=Credit.from_int(2),
    PALINDROME_MULTIPLIER=2,
    VOWEL_COST=Credit.from_float(0.3),
)
