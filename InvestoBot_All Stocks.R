# Load required packages
if (!require("quantmod")) install.packages("quantmod")
if (!require("dplyr")) install.packages("dplyr")
if (!require("ggplot2")) install.packages("ggplot2")
if (!require("jsonlite")) install.packages("jsonlite")  # For JSON output
if (!require("knitr")) install.packages("knitr")        # For kable
if (!require("devtools")) install.packages("devtools")
if (!require("psymonitor")) devtools::install_github("itamarcaspi/psymonitor")

require("quantmod")
require("dplyr")
require("psymonitor")
require("ggplot2")
require("jsonlite")  # For JSON output
require("knitr")     # For kable

# Define the vector of stock tickers
tickers <- c("PLTR", "TSLA", "NVDA", "AAPL", "MSFT", "INTC", "VOW3.DE", "CCJ")

# Loop through each ticker
for (s in tickers) {
  cat("\n\nProcessing:", s, "\n")
  tryCatch({
    # Get closing prices from Yahoo Finance
    p <- getSymbols(s, src = 'yahoo', auto.assign = FALSE, from = '2023-01-01', to = Sys.Date())
    
    # Extract closing prices
    closing_price_column <- paste0(s, ".Close")  # Dynamically generate the column name
    p_close <- p[, closing_price_column]  # Extract the dynamically referenced column
    
    # Prepare the data for the PSY test
    Stat <- data.frame(
      date = index(p), 
      closing_price = as.numeric(p[, closing_price_column])  # Rename to 'closing_price'
    )
    Stat <- na.omit(Stat)  # Remove any rows with NA values in closing_price
    
    if (nrow(Stat) == 0) {
      stop("Error: Stat dataframe is empty after processing.")
    }
    
    y <- Stat$closing_price  # Use the renamed 'closing_price' column
    
    # PSY Test Setup
    obs      <- length(y)
    r0       <- 0.01 + 1.8 / sqrt(obs)
    swindow0 <- floor(r0 * obs)
    dim      <- obs - swindow0 + 1
    IC       <- 2
    adflag   <- 6
    yr       <- 2
    Tb       <- 12 * yr + swindow0 - 1
    nboot    <- 99
    
    # Run the PSY test and simulate critical values via bootstrap
    bsadf          <- PSY(y, swindow0, IC, adflag)
    quantilesBsadf <- cvPSYwmboot(y, swindow0, IC, adflag, Tb, nboot, nCores = 2)
    
    monitorDates <- Stat$date[swindow0:obs]
    quantile95   <- quantilesBsadf %*% matrix(1, nrow = 1, ncol = dim)
    ind95        <- (bsadf > t(quantile95[2, ])) * 1
    bubble_detected <- ind95[length(ind95)] == 1  # Check if the last period is in a bubble
    
    # Modify bubbleDates to include start and end prices
    bubbleDates <- disp(locate(ind95, monitorDates), obs) %>%
      mutate(
        start_price = sapply(start, function(date) Stat$closing_price[which(Stat$date == date)]),
        end_price = sapply(end, function(date) Stat$closing_price[which(Stat$date == date)]),
        period_length = as.numeric(difftime(end, start, units = "days")) + 1,
        type = ifelse(start_price < end_price, "Bubble", "Crisis")  # Classify as Bubble or Crisis
      )
    
    # Get the last closing price
    last_closing_price <- tail(Stat$closing_price, 1)
    last_date <- tail(Stat$date, 1)
    
    # Extract the starting price from the last bubble or crisis
    if (nrow(bubbleDates) > 0) {
      last_bubble_crisis <- tail(bubbleDates, 1)  # Get the last bubble or crisis period
      last_bubble_start_price <- last_bubble_crisis$start_price
      profit <- last_closing_price - (last_bubble_start_price + 0.03 * last_bubble_start_price)
      profit_percentage <- (profit / last_bubble_start_price) * 100
    } else {
      last_bubble_start_price <- NA
      profit <- NA
      profit_percentage <- NA
    }
    
    # Recommendation based on bubble detection
    previous_day_bubble_status <- if (length(ind95) > 1) ind95[length(ind95) - 1] else 0
    today_bubble_status <- ind95[length(ind95)]
    
    if (previous_day_bubble_status == 1 && today_bubble_status == 1) {
      recommendation <- "Hold"
    } else if (previous_day_bubble_status == 1 && today_bubble_status == 0) {
      recommendation <- "Sell"
    } else if (previous_day_bubble_status == 0 && today_bubble_status == 1) {
      recommendation <- "Buy"
    } else {
      recommendation <- "Do Not Buy/Sell Stock"
    }
    
    # Calculate the stop price as the starting price of the last bubble/crisis + 1
    if (!is.na(last_bubble_start_price)) {
      stop_price <- last_bubble_start_price + 1
    } else {
      stop_price <- NA
    }
    
    # Define the result object
    result <- list(
      ticker = s,
      starting_price = last_bubble_start_price,
      closing_price = last_closing_price,
      profit = profit,
      profit_percentage = profit_percentage,
      stop = stop_price,
      message = recommendation
    )
    
    # Output JSON
    cat(toJSON(result, pretty = TRUE), "\n")
    
    # Print kable for long bubble or crisis periods
    long_bubbleDates <- bubbleDates %>% filter(period_length > 1)  # Filter for periods longer than one day
    if (nrow(long_bubbleDates) > 0) {
      print(kable(long_bubbleDates, caption = paste0("Long Bubble and Crisis Periods in ", s, " (more than one day)")))
    } else {
      cat("No long bubble or crisis periods detected for", s, "\n")
    }
    
  }, error = function(e) {
    cat("Error processing", s, ":", e$message, "\n")
  })

  if (length(result) == 0) {
    cat("No valid results were generated. JSON file will not be created.\n")
  } else {
    output_file <- paste0("D:\\Git\\StockBot\\public\\", s, ".json")  # Adjusted file path
    write_json(result, output_file, pretty = TRUE)
    cat("\nAll result have been saved to:", output_file, "\n")
    result <- NULL
  }
}