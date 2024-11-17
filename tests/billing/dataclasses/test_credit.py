import pytest

from billing.dataclasses import Credit


class TestMultiply:
    def test_value_is_int__returns_credit(self) -> None:
        credit = Credit.from_int(10)
        result = credit * 2

        assert isinstance(result, Credit)
        assert result.amount == 20

    def test_value_is_float__returns_credit(self) -> None:
        credit = Credit.from_int(10)
        result = credit * 2.5

        assert isinstance(result, Credit)
        assert result.amount == 25

    def test_value_is_credit__returns_credit(self) -> None:
        credit = Credit.from_int(10)
        result = credit * Credit.from_int(2)

        assert isinstance(result, Credit)
        assert result.amount == 20

    def test_value_is_invalid__returns_not_implemented(self) -> None:
        credit = Credit.from_int(10)
        with pytest.raises(NotImplementedError):
            credit * "2"  # type: ignore


class TestAdd:
    def test_value_is_credit__returns_credit(self) -> None:
        credit = Credit.from_int(10)
        result = credit + Credit.from_int(5)

        assert isinstance(result, Credit)
        assert result.amount == 15

    @pytest.mark.parametrize("value", ["2", 2, 2.5])
    def test_value_is_invalid__returns_not_implemented(self, value: str | int | float) -> None:
        credit = Credit.from_int(10)
        with pytest.raises(NotImplementedError):
            credit + value  # type: ignore


class TestSubtract:
    def test_value_is_credit__returns_credit(self) -> None:
        credit = Credit.from_int(10)
        result = credit - Credit.from_int(5)

        assert isinstance(result, Credit)
        assert result.amount == 5

    @pytest.mark.parametrize("value", ["2", 2, 2.5])
    def test_value_is_invalid__returns_not_implemented(self, value: str | int | float) -> None:
        credit = Credit.from_int(10)
        with pytest.raises(NotImplementedError):
            credit - value  # type: ignore


class TestEquality:
    def test_value_is_credit__returns_bool(self) -> None:
        credit = Credit.from_int(10)
        result = credit == Credit.from_int(10)

        assert isinstance(result, bool)
        assert result is True

    @pytest.mark.parametrize("value", ["2", 2, 2.5])
    def test_value_is_invalid__returns_not_implemented(self, value: str | int | float) -> None:
        credit = Credit.from_int(10)
        with pytest.raises(NotImplementedError):
            result = credit == value  # noqa


class TestLessThan:
    def test_value_is_credit__returns_bool(self) -> None:
        credit = Credit.from_int(10)
        result = credit < Credit.from_int(20)

        assert isinstance(result, bool)
        assert result is True

    @pytest.mark.parametrize("value", ["2", 2, 2.5])
    def test_value_is_invalid__returns_not_implemented(self, value: str | int | float) -> None:
        credit = Credit.from_int(10)
        with pytest.raises(NotImplementedError):
            result = credit < value  # type: ignore # noqa


class TestFromInt:
    def test_value_is_int__returns_credit(self) -> None:
        result = Credit.from_int(10)

        assert isinstance(result, Credit)
        assert result.amount == 10

    def test_value_is_not_int__raises_type_error(self) -> None:
        with pytest.raises(TypeError):
            Credit.from_int(10.5)  # type: ignore


class TestFromFloat:
    def test_value_is_float__returns_credit(self) -> None:
        result = Credit.from_float(10.5)

        assert isinstance(result, Credit)
        assert result.amount == 10.5

    def test_value_is_not_float__raises_type_error(self) -> None:
        with pytest.raises(TypeError):
            Credit.from_float(10)
