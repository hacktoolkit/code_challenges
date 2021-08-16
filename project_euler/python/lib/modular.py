"""modular.py

Modular arithmetic helpers
"""

def modular_multiply(A, B, C):
    """Finds `(A * B) mod C`

    This is equivalent to:

    `(A mod C * B mod C) mod C`

    https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/modular-multiplication
    https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/the-quotient-remainder-theorem
    """
    a_mod_c = A % C
    b_mod_c = B % C
    result = (a_mod_c * b_mod_c) % C
    return result
