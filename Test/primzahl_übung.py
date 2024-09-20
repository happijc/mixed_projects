def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def decompose_prime_factors(n):
    factors = []
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def primzahl_check(number):
    if isinstance(number, int) and number > 1:
        if number % 2 == 0:
            if number == 2:
                return True, [2]
            else:
                return False, decompose_prime_factors(number)
        else:
            is_prime_number = is_prime(number)
            if is_prime_number:
                return True, [number]
            else:
                return False, decompose_prime_factors(number)
    else:
        return False, []

number = 50
is_prime, factors = primzahl_check(number)
if is_prime:
    print(f"{number} est un nombre premier.")
else:
    print(f"{number} n'est pas un nombre premier. Facteurs premiers : {factors}")