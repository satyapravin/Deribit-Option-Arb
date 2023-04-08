# Important Notice

We are not responsible for ensuring the overall performance of Software or any related applications. Any test results or performance figures are indicative and will not reflect performance under all conditions. Software may contain components that are open sourced and subject to their own licenses; you are responsible for ensuring your compliance with those licenses.

We make no representation, warranty, guarantee or undertaking in respect of Software, whether expressed or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall we be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the Software or the use or other dealings in the Software.



# Option Arbitrage on Deribit

This tool identifies opportunities in Deribit options with various parameterizations by constructing a portfolio of options that can be delta hedged to generate P/L. It should ideally be used across three option expiries.

1. Maximize Gamma with a threshold on cost of portfolio (hopefully sometimes you can find a zero cost long gamma portfolio).
2. Minimize Theta (hopefully sometimes you can find a portfolio with positive gamma and negative theta; earn theta and long gamma).
3. Minimize Cost (hopefully sometimes you can find a portfolio with postive gamma/negative theta at zero cost!)

To use this tool, refer to screenshot below and do the following:

1. Add API key and secret to config/config.ini for TEST and PROD.
2. Run src/program.py
3. Select environment on screen.
4. Click on Connect button.
5. Select your criteria and Click Fetch Button.
6. Click on Compute to identify your portfolio (if exists).
7. You can choose to trade this portfolio too (note: It is not guaranteed the options will be bought/sold at the limit price)



Important: This is work in progress and USE AT YOUR OWN RISK. If you want to colloborate please extend tool to show executed trades and missing executions.

![Screenshot](screen.jpeg)


