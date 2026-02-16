# Order Routing

Order routing is the process by which a broker sends a client's order to an execution venue for execution. The goal of order routing is to find the best possible execution for the client's order, taking into account factors such as price, speed, and likelihood of execution.

## Smart Order Routers (SORs)
- **Description:** Smart Order Routers are algorithms that automate the order routing process. They use a set of rules and real-time market data to determine the best venue to which to route an order.
- **SOR Logic:** SORs typically consider the following factors:
    - **Venue fees:** The costs associated with trading on different venues.
    - **Liquidity:** The amount of trading activity on different venues.
    - **Latency:** The time it takes to send an order to a venue and receive a confirmation.
    - **Price improvement:** The potential to get a better price than the National Best Bid and Offer (NBBO).

## Common Order Routing Strategies
- **Spray:** Sending small orders to multiple venues simultaneously.
- **Sequential:** Sending an order to one venue at a time until it is filled.
- **Ping:** Sending a small order to a venue to test for liquidity before sending a larger order.

## Regulation of Order Routing
- **Regulation NMS (National Market System):** A set of rules in the United States that are designed to promote fair and efficient markets. One of the key provisions of Regulation NMS is the "Order Protection Rule," which requires brokers to route orders to the venue with the best price.
