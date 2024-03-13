# Modelling Banking Systems - Islamic vs Conventional
Author: [@AriqAhmer](https://github.com/AriqAhmer/)

## Introduction
I have started this repository to investigate the two major banking systems and observe their performance on many factors (to be listed).
The two banking systems differ in their fundamentals:

## Definitions
- **Islamic System:** It is based on basic profit and loss sharing system. The most widely used concept is that of _Mudarabah_ and _Musharaka_. However, in this study, I have chosen to use the _Mudarabah_ model. For further reading, you may consult the wikipedia page [here.](https://en.wikipedia.org/wiki/Profit_and_loss_sharing)
- **Conventional System:** This is the system that is widely used around the world. It an interest based system. Under general circumstances, compund interest is mostly used when calculating payment on loan. Hence for this study, I have chosen the _compound interest_ model.

## Preliminary Assumptions
For the sake of simplicity (and to get this research going), I have made the following assumtions:
1. The business takes a loan from the bank to start its operations.
2. The business had no initial capital. So the borrowed amount is its initial starting capital.
3. The owner invests a fixed amount from the starting capital each month.
4. The business makes a profit from the investments with a fixed profit margin.
5. The only fixed-expense that the business incurrs is the fixed salary of the business owner i.e. the expense/salary is constant every month. (very rudimentary and loose assumption)
   5.1 **Islamic Bank -** The net profit is calculated and distributed according to the bank's share in the in the business.
   5.2 **Conventional Bank -** A fixed amount, that is to be paid over the loan payment period, is further deducted fromt the profit amount i.e `net_profit = profit - (expense + debt_payment).`
7. The remaining amount (net profit) is reinvested into the business for the next month.

## Methodology
Using the above assumptions as a premise, the model simulates the business's transactions every month until either:

1. the simulation period ends. or,
2. the business has successfully repaid all the debt. or,
3. the business fails to make profit within the grace period given. In this case, it is assumed that the business is a loss model and is not viable to operate further.

The simulations are run in the `finance_modelling.ipynb` Jupyter Notebook and the main codes for the respective models are put as classes in the file `islamic_bank.py` and `conventional_bank.py`

## Improvements
As time progresses, I intend to make the following improvements:
- [ ] Refactor the code to accept functions instead of simple constants for the expenses, profit margin, repayment, reinvestment, and so on.
- [ ] Include case studies using real world data.
- [ ] Maybe make the logic work with given data in an array??? Though I don't know how that will work.
- [ ] Come up with better documentation.
