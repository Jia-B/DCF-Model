# Import relevant libraries
import pandas as pd
import re

# -------------------- INPUT ASSUMPTIONS --------------------
growth_rate = 0.017
ev_ebitda = 7.0
cost_debt = 0.05
tax_rate = 0.25
treasury_10y = 0.015
beta = 1.3
market_return = 0.1
equity_value = 17500.0
debt_value = 15000.0

"""
The next step is to import a csv file containing the following columns:
- EBIT
- D&A
- CapEx
- Change in non-cash working capital (increase should be positive/decrease should be negative)

Each row should represent a year. 
"""
# -------------------- DATA CLEANING --------------------

# Importing file
file_path = "/Users/jiabloom/Documents/DCF/input_data.csv" # CHANGE TO ACTUAL FILE PATH
input_data = pd.read_csv(file_path)
input_data = input_data.astype(str) # for data cleaning

# Change column names for standardization
column_names = ["EBIT", "D&A", "CapEx", "ChangeWC"]
input_data.columns = column_names

# Remove any commas from the data
input_data = input_data.replace(",", "", regex=True)

# Replace parentheses with negative sign
# Define a function to process each cell
def process_cell(cell):
    # Use regular expression to find numbers within parentheses
    match = re.match(r'\((-?\d+)\)', cell)
    if match:
        # If parentheses found, extract the number and add a negative sign
        number = match.group(1)
        return '-' + number
    else:
        return cell

# Apply function to input data
input_data = input_data.map(process_cell)

# Create a year column
input_data["Year"] = [i + 1 for i in range(len(input_data))]
input_data = input_data.reindex(columns = ["Year", "EBIT", "D&A", "CapEx", "ChangeWC"])

# Convert data frame to float
input_data = input_data.astype(float)

# -------------------- CALCULATIONS --------------------

# STEP 1: Calculate projected free cash flows (FCF)
FCF = input_data
FCF["Tax"] = FCF["EBIT"] * tax_rate
FCF["FCF"] = FCF["EBIT"] - FCF["Tax"] + FCF["D&A"] - FCF["CapEx"] - FCF["ChangeWC"]

# STEP 2: Calculate weighted average cost of capital (WACC)
cost_of_equity = treasury_10y + beta * (market_return - treasury_10y)
debt_percent =  debt_value / (debt_value + equity_value)
equity_percent = equity_value / (debt_value + equity_value)
WACC = (equity_percent * cost_of_equity) + (debt_percent * cost_debt * (1 - tax_rate))
print("The weighted average cost of capital (WACC) is", round(WACC*100, 2), "%")  

# STEP 3: Calculate terminal value
EBITDA_final = FCF["EBIT"].iloc[-1] + FCF["D&A"].iloc[-1] # final year EBIT + final year D&A
exit_multiple = ev_ebitda * EBITDA_final
perpetuity_growth = (FCF["FCF"].iloc[-1] * (1 + growth_rate)) / (WACC - growth_rate)
# Terminal value calculated based on the average of the exit multiple & perpetuity growth assumption
terminal_value = (exit_multiple + perpetuity_growth) / 2    
print("The terminal value is $", round(terminal_value, 2))

# STEP 4: Discount FCF & terminal value to present value
FCF["TotalCF"] = FCF["FCF"]
FCF["TotalCF"].iloc[-1] = FCF["TotalCF"].iloc[-1] + terminal_value
FCF["DiscountFactor"] = 1 / (1 + WACC) ** FCF["Year"]
FCF["PresentValue"] = FCF["TotalCF"] * FCF["DiscountFactor"]

EV = round(sum(FCF["PresentValue"]),2)
print("The enterprise value of the company is $", EV)

# Rounding the final DCF model for readability
DCF = FCF.round(2)
print(DCF)