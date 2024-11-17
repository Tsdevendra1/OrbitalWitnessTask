from dataclasses import dataclass
from decimal import Decimal
from functools import total_ordering
from typing import Self


@total_ordering
@dataclass(frozen=True, slots=True)
class Credit:
    """
    Decision #1 Creating a Credit dataclass:
    I chose to create a Credit dataclass because it allows for better domain modelling. Instead of using primitives
    such as floats or ints, we can encapsulate the logic related to credits in this class. This makes the code more
    readable and maintainable. If we need to change the implementation of credits in the future, we can do it in one
    place (this class) instead of scattered throughout the code. There is a trade-off here, it does make the code a bit
    more complex for this simple task, but I think it's worth it for the benefits it provides.

    Decision #2 Using the Decimal:
    Using the Decimal instead of float to avoid floating point errors.

    Decision #3 Using frozen=True:
    I chose to make the dataclass frozen to ensure immutability. This is to avoid accidental changes to variables
    in the code.

    # Decision #4 Using slots=True:
    I chose to use slots=True to save memory by avoiding the creation of a __dict__ attribute for each instance.
    This is useful when we have a large number of instances of the dataclass. In this case, it's probably not
    necessary, but it's a good practice to use slots=True when possible.
    """

    amount: Decimal

    @classmethod
    def from_float(cls, amount: float) -> Self:
        if not isinstance(amount, float):
            raise TypeError("Credit amount must be a float")
        return cls(Decimal(str(amount)))

    @classmethod
    def from_int(cls, amount: int) -> Self:
        if not isinstance(amount, int):
            raise TypeError("Credit amount must be an integer")
        return cls(Decimal(amount))

    @classmethod
    def zero(cls) -> Self:
        return cls(Decimal(0))

    def __post_init__(self) -> None:
        # Decision: I used pure dataclasses here, I think if I spent more time a BaseModel from pydantic would
        # be a better choice as it provides more validation and flexibility. Pydantic would also provide the type
        # checks for free.
        if not isinstance(self.amount, Decimal):
            raise TypeError("Credit amount must be a Decimal")

    def __add__(self, other: Self) -> Self:
        """
        Using Self instead of just returning Credit: this allows flexibility of subclassing in the future if we have
        different types of credits. Perhaps overkill for this simple task, but allows better flexibility in the future.
        """

        # We have type hinting but still worth checking for defensive programming
        if not isinstance(other, Credit):
            raise NotImplementedError("Cannot add Credit with non-Credit type")
        amount = self.amount + other.amount
        return self.__class__(amount=amount)

    def __sub__(self, other: Self) -> Self:
        if not isinstance(other, Credit):
            raise NotImplementedError("Cannot subtract Credit with non-Credit type")
        amount = self.amount - other.amount
        return self.__class__(amount=amount)

    def __mul__(self, other: Self | int | float) -> Self:
        if isinstance(other, int | float):
            return self.__class__(amount=self.amount * Decimal(str(other)))
        if isinstance(other, Credit):
            return self.__class__(amount=self.amount * other.amount)
        raise NotImplementedError("Cannot multiply Credit with non-Credit type")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Credit):
            raise NotImplementedError("Cannot compare Credit with non-Credit type")
        return self.amount == other.amount

    def __lt__(self, other: Self) -> bool:
        if not isinstance(other, Credit):
            raise NotImplementedError("Cannot compare Credit with non-Credit type")
        return self.amount < other.amount


@dataclass(frozen=True, slots=True)
class BillingParameters:
    """
    Decision #1: Using a dataclass for BillingParameters:
    I chose to use a dataclass for BillingParameters to easily encapsulate all the required parameters for billing.
    It also has the added benefit of allowing different parameter setups for different customers in the future if required.
    """

    BASE_CREDIT_COST: Credit
    CHAR_CREDIT_COST: Credit
    LENGTH_PENALTY_THRESHOLD: int
    ONE_TO_THREE_WORD_LENGTH_COST: Credit
    FOUR_TO_SEVEN_WORD_LENGTH_COST: Credit
    EIGHT_PLUS_WORD_LENGTH_COST: Credit
    LENGTH_PENALTY_CREDITS: Credit
    UNIQUE_WORDS_BONUS: Credit
    PALINDROME_MULTIPLIER: int
    VOWEL_COST: Credit
    VOWELS = set("aeiouAEIOU")

    def __post_init__(self) -> None:
        # Decision: I used pure dataclasses here, I think if I spent more time a BaseModel from pydantic would
        # be a better choice as it provides more validation and flexibility. Pydantic would also provide the type
        # checks for free.
        if self.LENGTH_PENALTY_THRESHOLD < 0:
            raise ValueError("Length penalty threshold cannot be negative")
        if self.PALINDROME_MULTIPLIER < 0:
            raise ValueError("Palindrome multiplier cannot be negative")
        if not self.VOWELS:
            raise ValueError("Vowels set cannot be empty")
        # NOTE: Defensive programming, checking if the attributes are of the correct type. Perhaps redundant, if we went
        # with pydantic we would get this for free.
        for attr in self.__annotations__:
            if attr not in {"VOWELS", "LENGTH_PENALTY_THRESHOLD", "PALINDROME_MULTIPLIER"} and not isinstance(
                getattr(self, attr), Credit
            ):
                raise TypeError(f"{attr} must be of type Credit")
