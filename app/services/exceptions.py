class InvalidAmountError(ValueError):
    """Исключение для некорректного количества товара."""

    def __init__(self, sku, amount):
        self.sku = sku
        self.amount = amount
        super().__init__("Некорректное количество '{amount}' "
                         f"для товара '{sku}'")
