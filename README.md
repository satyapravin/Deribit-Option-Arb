# Option Arbitrage on Deribit

This tool identifies opportunities in Deribit options with various parameterizations by constructing a portfolio of options that can be delta hedged to generate P/L. It should ideally be used across three option expiries.

1. Maximize Gamma with a threshold on cost of portfolio (hopefully sometimes you can find a zero cost long gamma portfolio).
2. Minimize Theta (hopefully sometimes you can find a portfolio with positive gamma and negative theta; earn theta and long gamma).
3. Minimize Cost (hopefully sometimes you can find a portfolio with postive gamma/negative theta at zero cost!)

To use this tool, refer to screenshot below and do the following:

1. Add API key and secret to config/config.ini for TEST and PROD.
2. Select environment on screen.
3. Click on Connect button.
4. Select your criteria and Click Fetch Button.
5. Click on Compute to identify your portfolio (if exists).
6. You can choose to trade this portfolio too (note: It is not guaranteed the options will be bought/sold at the limit price)



Important: This is work in progress and use at your own risk. If you want to colloborate please extend tool to show executed trades and missing executions.

![Screenshot](screen.jpeg)


