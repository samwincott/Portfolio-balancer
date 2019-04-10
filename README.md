# Lazy Allocator

Lazy Allocator is a Python program for allocating savings to a fixed portfolio.
For example saving £100 a month to a defined portfolio such as 60% equities and 40% bonds. If those are represented by multiple trackers, each of a different price, it may not be clear how to allocate the £100 a month to each fund; especially as the prices of each will fluctuate over time.

This program scrapes pricing data from [Morningstar](morningstar.co.uk). An example is [Vanguard emerging markets](http://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id=F000003VEA).

## Usage
```text
make run
```

The constant `VOLATILITY` is set in the portfolio class. This is because the broker I use executes all trades at 4pm. If I submit a trade at 11am at the actual price, the price increases, then the trade may not execute due to a lack of funds. If the price does not reach the upper limit that is set with the `VOLATILITY` variable, then it will execute at the best price at 4pm.

## Portfolio JSON
Example:
```json
{
    "shares":[
        {
            "Ticker":"ABC",
            "Owned":8,
            "Percentage":30,
            "MorningstarID":"0P0000YWPH"
        },
        {
            "Ticker":"MNO",
            "Owned":8,
            "Percentage":30,
            "MorningstarID":"0P0000WAHF"
        },
        {
            "Ticker":"XYZ",
            "Owned":12,
            "Percentage":40,
            "MorningstarID":"0P0000WAHG"
        }
    ]
}
```

The ticker, aim percentage of portfolio, and Morninstar ID must be included in this file.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

