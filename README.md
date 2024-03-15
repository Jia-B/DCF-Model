# DCF-Model
## Purpose
The goal of this Python program is to calculate the enterprise value (EV) of a company based on future cash flows discounted to their present value, also known as a discounted cash flow (DCF) model. 

The program assumes that the user already has certain projections and assumptions. 

Assumptions supplied by the user include the following: 

* **Growth rate**
* **EV/EBITDA**
* **Cost of debt**
* **Tax rate**
* **10-Year Treasury Bond return**
* **Beta**
* **Market return**
* **Equity value**
* **Debt value**

## Files
* `DCF.py` - contains the Python program
* `input_data.csv` - contains an example of what the input to the program should look like in terms of formatting

## How to Use
On lines 6-14, the user should update the assumptions. 

On line 28, the user should change the file path to their csv file with columns: EBIT, D&A, CapEx, and Change in Non-Cash Working Capital. Each row should represent a year.

The program will output the calculated weighted average cost of capital (WACC), terminal value, and enterprise value. Additionally, it will output a DataFrame containing the full DCF model, including the present value of the future free cash flows. 

## Technologies
The DCF model uses the following Python libraries `pandas` (for DataFrames) and `re` (for Regular Expressions). 
