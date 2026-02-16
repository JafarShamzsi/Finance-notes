```python
import numpy as np

def monte_carlo_option_pricer(S, K, T, r, sigma, option_type='call', n_simulations=10000):
    """
    Prices an option using a Monte Carlo simulation.

    Parameters
    ----------
    S : float
        The current price of the underlying asset.
    K : float
        The strike price of the option.
    T : float
        The time to maturity of the option (in years).
    r : float
        The risk-free interest rate.
    sigma : float
        The volatility of the underlying asset.
    option_type : str, optional
        The type of option, by default 'call'. Can be 'call' or 'put'.
    n_simulations : int, optional
        The number of simulations to run, by default 10000.

    Returns
    -------
    float
        The price of the option.
    """

    # Generate random price paths
    z = np.random.standard_normal(n_simulations)
    ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z)

    # Calculate the payoff of the option
    if option_type == 'call':
        payoff = np.maximum(ST - K, 0)
    elif option_type == 'put':
        payoff = np.maximum(K - ST, 0)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    # Discount the payoff to the present value
    option_price = np.exp(-r * T) * np.mean(payoff)

    return option_price

if __name__ == '__main__':
    # Parameters
    S = 100
    K = 100
    T = 1
    r = 0.05
    sigma = 0.2

    # Price a call option
    call_price = monte_carlo_option_pricer(S, K, T, r, sigma, option_type='call')
    print(f'The price of the call option is: {call_price:.2f}')

    # Price a put option
    put_price = monte_carlo_option_pricer(S, K, T, r, sigma, option_type='put')
    print(f'The price of the put option is: {put_price:.2f}')
```
