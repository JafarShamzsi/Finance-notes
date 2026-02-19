import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    Calculate Black-Scholes option price.
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return price

def binomial_tree_pricing(S, K, T, r, sigma, N, option_type='call'):
    """
    Price a European option using a multi-period binomial tree.
    """
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)

    # Initialize asset prices at maturity
    prices = np.zeros(N + 1)
    for i in range(N + 1):
        prices[i] = S * (u ** (N - i)) * (d ** i)

    # Payoffs at maturity
    if option_type == 'call':
        payoffs = np.maximum(prices - K, 0)
    else:
        payoffs = np.maximum(K - prices, 0)

    # Backward induction
    for j in range(N - 1, -1, -1):
        for i in range(j + 1):
            payoffs[i] = np.exp(-r * dt) * (p * payoffs[i] + (1 - p) * payoffs[i+1])

    return payoffs[0]

# Testing and Comparison
if __name__ == "__main__":
    S = 100
    K = 100
    T = 1
    r = 0.05
    sigma = 0.2
    N = 100

    bs_price = black_scholes(S, K, T, r, sigma)
    bt_price = binomial_tree_pricing(S, K, T, r, sigma, N)

    print(f"S={S}, K={K}, T={T}, r={r}, sigma={sigma}")
    print(f"Black-Scholes Price: {bs_price:.4f}")
    print(f"Binomial Tree Price (N={N}): {bt_price:.4f}")
    print(f"Difference: {abs(bs_price - bt_price):.6f}")
