from subprocess import call

def check(ticker: str):
    investoBot = "Rscript --vanilla InvestoBot_All\ Stocks.R"
    output = call(f"{investoBot} {ticker}",shell=True)
    return output

if __name__ == '__main__':
    ticker = "ALB"