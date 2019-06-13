def implication(antecedent: bool, consequent: bool) -> bool:
    return not antecedent or consequent


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return not left_statement ^ right_statement
