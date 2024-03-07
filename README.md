![image](https://github.com/JustTheCoolest/StockAnalyser/assets/74148176/def4b6db-32d5-4242-a15a-6fa557e7c75b)

![image](https://github.com/JustTheCoolest/StockAnalyser/assets/74148176/1862184b-03a9-4fff-8595-26b9d6f0b417)

Each of the records present for that given stock are returned.
The first and second values in the inner array represent the selling price of the stock to achieve the target profit. 
The first value considers the exact number of years (including fractions) since the stock was purchased, while the second value rounds up the number of years.

Both results are compounded annually, with the fractional year compounding upto the fraction

In the given example, the stock price was 1000 at purchase, and it was bought about 1 year and 1 month ago. The analyser also accounts for transaction fees and capital gains tax. 

Refer the API/requester_tests.py to see how adding data via the API works
