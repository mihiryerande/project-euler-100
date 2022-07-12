# Problem 100:
#     Arranged Probability
#
# Description:
#     If a box contains twenty-one coloured discs,
#       composed of fifteen blue discs and six red discs,
#       and two discs were taken at random,
#       it can be seen that the probability of taking two blue discs,
#         P[BB] = (15/21) * (14/20) = 1/2.
#
#     The next such arrangement,
#       for which there is exactly 50% chance of taking two blue discs at random,
#       is a box containing eighty-five blue discs and thirty-five red discs.
#
#     By finding the first arrangement to contain over 10^12 = 1,000,000,000,000 discs in total,
#       determine the number of blue discs that the box would contain.

from math import sqrt
from typing import Tuple


def main(n_min: int) -> Tuple[int, int]:
    """
    Returns the red/blue disc arrangement (as counts of red+blue and blue-only)
      in the first arrangement having more than `n_min` total discs,
      where the probability of drawing two blue discs (without replacement) is P[BB] = 1/2 exactly.

    Args:
        n_min (int): Natural number

    Returns:
        (Tuple[int, int]):
            Tuple of ...
              * Total disc count of arrangement (red+blue)
              * Blue disc count

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(n_min) == int and n_min > 0

    # Idea 1:
    #     Let `n` denote the total number of discs in a disc set.
    #     Let `x` denote the number of blue discs in a disc set.
    #
    #     Suppose we have a set of some fixed number of total discs `n`.
    #     What number of blue discs, `x`, would make the set an arrangement?
    #     We use the probability requirement to deduce `x`, given `n`:
    #         P[BB] = (x / n) * ((x-1) / (n-1))
    #         1/2 = (x / n) * ((x-1) / (n-1))
    #         1/2 = x*(x-1) / (n((n-1))
    #         (n*(n-1))/2 = x*(x-1)
    #         (n*(n-1))/2 = x^2 - x
    #         x^2 - x - (n*(n-1))/2 = 0
    #
    #     Solve for `x` using the quadratic formula:
    #         x = (-b ± sqrt(b^2 - 4ac) / (2a)
    #         x = (-(-1) ± sqrt((-1)^2 - 4(1)(-(n*(n-1))/2)) / (2(1))  (substituting coefficients from equation)
    #         x = (1 ± sqrt(1 + 2*n*(n-1))) / 2                        (simplifying)
    #         x = (1 + sqrt(1 + 2*n*(n-1))) / 2                         (`x` must be non-negative)
    #
    #     Now we have an exact formula for `x`, but `x` must be an integer.
    #     This means we need two things:
    #       * Radicand [1 + 2*n*(n-1)] must be a perfect square
    #       * sqrt(...) must be odd
    #
    #     Suppose we know that the radicand is a perfect square.
    #     We also know that it must be odd, since it equals 2*y+1, for some y.
    #     Thus, the sqrt(...) expression is odd as well.
    #     This verifies that x is an integer as we get
    #         x = (1 + <odd>) / 2 = <even> / 2 = <int>

    # Idea 2:
    #     From the previous reasoning, we see `n` must be such that the radicand is a perfect square.
    #     Let `z` be such that the radicand is equal to z^2.
    #     Manipulating the radicand:
    #         z^2 = 1 + 2*n*(n-1)
    #         z^2 = 2*n^2 - 2*n + 1
    #         z^2 = n^2 + n^2 - 2*n + 1
    #         z^2 = n^2 + (n-1)^2
    #
    #     We see now that we are looking for such `n` where `n` is part of a pythagorean triple (n-1, n, k)
    #     Also, such a triple would be `primitive` (i.e. co-prime), as (n-1) and n must be co-prime.
    #     Knowing this, we can use Euclid's formula for generating primitive pythagorean triples.
    #
    #     For some arbitrary ints p, q (where 0 < q < p),
    #       all primitive triples (a, b, c) can be generated with the following expressions:
    #         a = p^2 - q^2
    #         b = 2*p*q
    #         c = p^2 + q^2
    #     We thus want p and q which generate side lengths `a` and `b` differing by exactly 1,
    #       i.e. abs(a-b) = 1, and `n` would be the greater of these two.

    # Idea 3:
    #     Suppose we only consider `n` to be even.
    #     Then we have:
    #         n     = b = 2*p*q
    #         n-1   = a = p^2 - q^2
    #
    #     Combining these:
    #         2*p*q = p^2 - q^2 + 1
    #         0 = p^2 - 2*p*q - q^2 + 1
    #         p^2 - 2*p*q - q^2 = -1
    #         p^2 - 2*p*q +q^2 - 2*q^2 = -1
    #         (p-q)^2 - 2*q^2 = -1
    #     Leave this for now.
    #
    # ------------------------------------------------------
    #
    #     Now suppose we only consider `n` to be odd.
    #     Then we have:
    #         n     = a = p^2 - q^2
    #         n-1   = b = 2*p*q
    #
    #     Combining these:
    #         p^2 - q^2 = 2*p*q + 1
    #         p^2 - 2*p*q - q^2 = 1
    #         p^2 - 2*p*q + q^2 - 2*q^2 = 1
    #         (p-q)^2 - 2*q^2 = 1
    #
    # ------------------------------------------------------
    #
    #     Simplify a bit by letting ...
    #       * r = p - q
    #       * s = q
    #
    #     Combining the previous two constraints,
    #       it turns out we are looking for p and q satisfying the following:
    #         (p-q)^2 - 2*q^2 = ± 1
    #     Rephrased as:
    #         r^2 - 2*s^2 = ± 1
    #
    #     This is Pell's equation (x^2 - D*y^2 = 1) where D = 2.
    #     So we are looking for integer solutions `r` and `s` to this Diophantine equation.

    # Idea 4:
    #     The solutions of this equation are known to be the convergents of the
    #       continued-fraction representation of sqrt(D), which is sqrt(2) in this case.
    #
    #     The first convergent is c{0} = r{0} / s{0} = 1 / 1
    #     Subsequent convergents can be calculated with a recurrence relation:
    #        Base case:
    #            r{0} = 1
    #            s{0} = 1
    #        Recurrence relation:
    #            r{i+1} = r{i} + 2 * s{i}
    #            s{i+1} = r{i} + s{i}
    #
    #     Given r{i} and s{i}, we can determine the corresponding p{i} and q{i}:
    #         p{i} = r{i} + s{i}
    #         q{i} = s{i}
    #
    #     Then the two legs of the primitive pythagorean triple constructed using p{i} and q{i} will be:
    #         a{i} = p{i}^2 - q{i}^2
    #         b{i} = 2 * p{i} * q{i}
    #
    #     We know that `a` and `b` differ by exactly 1, but do not know which is greater.
    #     So we let n{i} = max(a{i}, b{i}).
    #
    #     This lets us iterate until n{i} surpasses the desired limit.
    #     Then x{i}, the number of blue discs, can be determined with the expression found previously.
    #     Dropping the subscripts for readability:
    #         x = (1 + sqrt(1 + 2*n*(n-1))) / 2
    #         x = (1 + sqrt(1 + 2*a*b)) / 2
    #         x = (1 + sqrt(1 + 2*a*b)) / 2

    # Convergent c{0} of sqrt(2) = r{0} / s{0} = 1 / 1
    r = 1
    s = 1

    while True:
        # Arbitrary ints used to generate primitive pythagorean triple
        p = r + s
        q = s

        # Legs of generated pythagorean triple
        a = (p-q)*(p+q)
        b = 2*p*q

        # n is the greater of the two legs
        n = max(a, b)
        if n > n_min:
            x = int((1 + sqrt(1 + 2*a*b)) / 2)
            return n, x
        else:
            r, s = r + 2*s, r + s
            continue


if __name__ == '__main__':
    disc_lower_bound = int(input('Enter a natural number: '))
    total_disc_count, blue_disc_count = main(disc_lower_bound)
    print('First arrangement (of > {} discs) s.t. probability of two blues is exactly 1/2:'.format(disc_lower_bound))
    print('  Total = {}'.format(total_disc_count))
    print('  Blue  = {}'.format(blue_disc_count))
