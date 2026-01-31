class InvalidRuleset(ValueError):
    pass


class Rules:
    def __init__(
        self,
        soft17: str = "H17",
        decks: int = 4,
        das: str = "DAS",
        peek: str = "peek",
    ):
        if soft17 in ["S17", "H17"]:
            self.soft17 = soft17
        else:
            raise InvalidRuleset(f"Unknown H17/S17 parameter: {soft17}")
        if decks in [2, 4]:
            self.decks = decks
        else:
            raise InvalidRuleset(f"Unknown number of decks: {decks}")
        if das in ["DAS", "noDAS"]:
            self.das = das
        else:
            raise InvalidRuleset(f"Unknown DAS rule: {das}")
        if peek in ["peek", "nopeek"]:
            self.peek = peek
        else:
            raise InvalidRuleset(f"Unknown peek rule: {peek}")

    @classmethod
    def from_ruleset(cls, ruleset: str):
        rules = ruleset.split("_")
        if len(rules) != 4:
            raise InvalidRuleset(
                f"Incorrect amount of arguments in ruleset: {len(rules)}"
            )

        soft17 = None
        decks = None
        das = None
        peek = None

        for rule in rules:
            if rule in ["S17", "H17"]:
                soft17 = rule
            elif rule in ["2", "4"]:
                decks = int(rule)
            elif rule in ["DAS", "noDAS"]:
                das = rule
            elif rule in ["peek", "nopeek"]:
                peek = rule
            else:
                raise InvalidRuleset(f"Unknown rule: {rule}")

        if soft17 is None:
            raise InvalidRuleset("Missing H17/S17")
        if decks is None:
            raise InvalidRuleset("Missing the number of decks")
        if das is None:
            raise InvalidRuleset("Missing the DAS rule")
        if peek is None:
            raise InvalidRuleset("Missing the peek rule")

        return cls(soft17=soft17, decks=decks, das=das, peek=peek)

    def ruleset_id(self):
        return f"{self.soft17}_{self.decks}_{self.das}_{self.peek}"
