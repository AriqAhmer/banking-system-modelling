# importing matplotlib for creating plots
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from typing import Callable

class ConventionalModel:
    """
    A class for modelling the effect of Conventional Banking on a given business.
    The model assumes the interest (compounding) based model.

    ...

    Attributes
    ----------
    initial_capital : int
        The capital amount loaned to the business by the Bank.
    
    current_capital : int
        The capital amount the business currently has before the venture begins.

    profit_margin : float | Callable
        The percentage profit margin on the goods traded. Accepts a function which is time dependent with signature foo(t: int) -> float
    
    expenses : float | Callable
        The amount to be spent on expenses during operation of business. Accepts a function which is time dependent with signature foo(t: int) -> float
    
    interest_rate : float
        The interest rate charged by the bank.

    loan_period : int
        The expected time for paying back the loaned amount + interest.

    initial_capital_reinvestment : float | Callable
        The amount from the initial_capital to be reinvested into the business. Accepts a function which is time dependent with signature foo(t: int) -> float
    
    dividend_payment : float | Callable
        The percentage of dividend expected to be paid to the business owner. Accepts a function which is time dependent with signature foo(t: int) -> float

    ...

    Methods
    -------
    simulate(time_period : int, grace_period : int, verbose : bool = False):
        Simulates the business operating over a given time_period, t, from t=0 to t=time_period and returns relevant data.
    """
    
    def __init__(
            self,
            initial_capital: int,
            current_capital: int,
            profit_margin: float | Callable,
            expenses: float | Callable,
            interest_rate: float,
            loan_period: int,
            initial_capital_reinvestment: float | Callable,
            dividend_payment: float | Callable = 0.0
        ) -> None:
        """
        Constructs the business model based on the parameters

        Parameters
        ----------
            initial_capital : int
                The capital amount loaned to the business by the Bank.
            
            current_capital : int
                The capital amount the business currently has before the venture begins.

            profit_margin : float | Callable
                The percentage profit margin on the goods traded. Accepts a function which is time dependent with signature foo(t: int) -> float
            
            expenses : float | Callable
                The amount to be spent on expenses during operation of business. Accepts a function which is time dependent with signature foo(t: int) -> float
            
            interest_rate : float
                The interest charged by the bank.
            
            loan_period : int
                The expected time (in years) for paying back the loaned amount + interest.

            initial_capital_reinvestment : float | Callable
                The amount from the initial_capital to be reinvested into the business. Accepts a function which is time dependent with signature foo(t: int) -> float
            
            dividend_payment : float | Callable = 0.0
                The percentage of dividend expected to be paid to the business owner. Accepts a function which is time dependent with signature foo(t: int) -> float
        """
        self.initial_capital = initial_capital
        self.current_capital = current_capital
        self.profit_margin = profit_margin
        self.expenses = expenses
        self.interest_rate = interest_rate
        self.loan_period = loan_period
        self.initial_capital_reinvestment = initial_capital_reinvestment
        self.dividend_payment = dividend_payment
        
        self.bank_loan = initial_capital * ((1 + interest_rate)**loan_period)
        self.business_loan = -self.bank_loan
        self.status: int = 0

        # model values for analysis purposes
        self.model: dict[str: list[float]] = {
            "time_period": [],
            "initial_capital": [],
            "current_capital": [],
            "bank_loan": [],
            "debt_payment": [],
            "net_profit": []
        }

    # simulation function
    def simulate(self, time_period: int, grace_period: int, verbose: bool = False) -> tuple[int, int, float, float, float]:
        """
        Simulates the business operating over a given time_period, t, from t=0 to t=time_period.

        Parameters
        ----------
            time_period : int
                The time period (in months) (epochs) for the simulation duration.

            grace_period : int
                Grace period given to the business to become operational and make actual profits.

            verbose : bool = False
                Whether to ouput simulation results for each time period (epoch).

        Returns
        -------
            (status, t, net_profit, current_capital, bank_loan) : tuple[int, int, float, float, float]\n
                status = 1 if simulation suceeded, 2 if business is a loss model (failed), 3 if maximum simulation time is reached and debt is not paid (failed)\n
                t = the time taken for simulation.\n
                net_profit = final net profit after final bank payment.\n
                current_capital = amount of capital owned entirely by the business.\n
                bank_loan = amount of loan remaining.\n
        """

        print(f"\nCONVENTIONAL BANK SIMULATION\nBank Capital: {self.initial_capital:,.2f} | Bank Loan (@{self.interest_rate:.2%}): {self.bank_loan:,.2f}")

        # fixed amount expecred to be paid to the bank over the loan period
        bank_repayment = self.bank_loan/(self.loan_period * 12)
        total_loan_paid: float = 0.0

        for t in range(time_period+1):
            # CHECK IF FUNCTION OR CONSTANT IS PASSED

            # check for initial_capital_reinvestment
            if isinstance(self.initial_capital_reinvestment, Callable):
                initial_capital_reinvestment = self.initial_capital_reinvestment(t)
            elif isinstance(self.initial_capital_reinvestment, float):
                initial_capital_reinvestment = self.initial_capital_reinvestment
            else:
                raise TypeError(f"parameter \"initial_capital_reinvestment\" must be of type \'float\' or \'Callable\' with independent variable t. Not type {type(self.initial_capital_reinvestment)}")
            
            # check for profit margin
            if isinstance(self.profit_margin, Callable):
                profit_margin = self.profit_margin(t)
            elif isinstance(self.profit_margin, float):
                profit_margin = self.profit_margin
            else:
                raise TypeError(f"parameter \"profit_margin\" must be of type \'float\' or \'Callable\' with independent variable t. Not type {type(self.profit_margin)}")
            
            # check for expenses
            if isinstance(self.expenses, Callable):
                expenses = self.expenses(t)
            elif isinstance(self.expenses, float):
                expenses = self.expenses
            else:
                raise TypeError(f"parameter \"expenses\" must be of type \'float\' or \'Callable\' with independent variable t. Not type {type(self.expenses)}")
            
            # check for dividend
            if isinstance(self.dividend_payment, Callable):
                dividend_payment = self.dividend_payment(t)
            elif isinstance(self.dividend_payment, float):
                dividend_payment = self.dividend_payment

                if dividend_payment > 1.0 or dividend_payment < 0.0:
                    raise ValueError(f"dividend_payment must be within interval [0, 1]. Not {dividend_payment}")
            else:
                raise TypeError(f"parameter \"dividend_payment\" must be of type \'float\' or \'Callable\' with independent variable t. Not type {type(self.dividend_payment)}")
            
            # verbose
            if verbose:
                print(f"At {t = } month\nStarting Capital: {self.initial_capital:,.2f} | Current Capital: {self.current_capital:,.2f}")
            
            # storing simulation values
            self.model["time_period"].append(float(t))
            self.model["initial_capital"].append(float(self.initial_capital))
            self.model["current_capital"].append(float(self.current_capital))
            
            # get some amount from initial capital
            if self.initial_capital - initial_capital_reinvestment >= 0:
                investment = initial_capital_reinvestment + self.current_capital
                self.initial_capital -= initial_capital_reinvestment
            else:
                investment = self.initial_capital + self.current_capital
            
            # invest that amount and make profit
            profit = investment * profit_margin

            # update loan amounts
            if self.bank_loan > 0:

                if bank_repayment <= self.bank_loan:
                    self.bank_loan -= bank_repayment
                    self.business_loan += bank_repayment
                else:
                    net_gain = bank_repayment - self.bank_loan
                    bank_repayment = self.bank_loan
                    self.bank_loan = 0

                    profit += net_gain

            # subtract expenses + profit amount paid to bank, to get net profit
            net_profit = profit - (bank_repayment + expenses)
            total_loan_paid += bank_repayment

            # calculate business's own capital
            self.current_capital += (net_profit * (1.0 - dividend_payment)) + investment

            if verbose:
                print(f"Amount invested: {investment:,.2f}")
                print(f"Profit made (@{profit_margin:.2%}): {profit:,.2f} | Amount paid to bank (@{self.interest_rate:.2%}): {bank_repayment:,.2f} | Net profit: {net_profit:,.2f}")
                print(f"Loan Remaining: {self.bank_loan:,.2f}")
                print(f"Amount Reinvested: {self.current_capital:,.2f}\n")

            # storing simulation values
            self.model["bank_loan"].append(float(self.bank_loan))
            self.model["debt_payment"].append(float(bank_repayment))
            self.model["net_profit"].append(float(net_profit))

            if (self.bank_loan == 0) and (t <= self.loan_period*12) and (net_profit>0 or self.current_capital>0):
                within_grace_period: bool = t <= grace_period
                status = 1
                break
            elif (t == grace_period) and (net_profit < 0 or self.current_capital < 0):
                within_grace_period: bool = t <= grace_period
                status = 2
                break
            elif t > self.loan_period*12:
                within_grace_period: bool = t <= grace_period
                status = 3
                break

        match status:
            case 1:
                print(f"\n---------END OF SIMULATION----------")
                print(f"Status: SUCCESS")
                print(f"Total period of payment {t = } months | {'Within' if within_grace_period else 'After'} grace period\n")
                print(f"Loan Remaining: {self.bank_loan:,.2f} | Loan Paid: {total_loan_paid:,.2f}")
                print(f"Profit made (@{profit_margin:.2%}): {profit:,.2f} | Final bank payment (@{self.interest_rate:.2%}): {bank_repayment:,.2f} | Net profit: {net_profit:,.2f}")
                print(f"Amount Reinvested: {self.current_capital:,.2f}\n")
            
            case 2:
                print(f"\n---------END OF SIMULATION----------")
                print(f"Status: FAIL | Business is a LOSS MODEL")
                print(f"Total period of payment {t = } months | {'Within' if within_grace_period else 'After'} grace period\n")
                print(f"Loan Remaining: {self.bank_loan:,.2f} | Loan Paid: {total_loan_paid:,.2f}")
                print(f"Profit made (@{profit_margin:.2%}): {profit:,.2f} | Final bank payment (@{self.interest_rate:.2%}): {bank_repayment:,.2f} | Net profit: {net_profit:,.2f}")
                print(f"Amount Reinvested: {self.current_capital:,.2f}\n")

            case 3:
                print(f"\n---------END OF SIMULATION----------")
                print(f"Status: FAIL | Maximum time period reached")
                print(f"Total period of payment {t = } months | {'Within' if within_grace_period else 'After'} grace period\n")
                print(f"Loan Remaining: {self.bank_loan:,.2f} | Loan Paid: {total_loan_paid:,.2f}")
                print(f"Profit made (@{profit_margin:.2%}): {profit:,.2f} | Final bank payment (@{self.interest_rate:.2%}): {bank_repayment:,.2f} | Net profit: {net_profit:,.2f}")
                print(f"Amount Reinvested: {self.current_capital:,.2f}\n")

            case _:
                print(f"UNKNOWN CASE")

        self.status = status

        return (status, t, round(net_profit, 2), round(self.current_capital, 2), round(self.bank_loan, 2))
    
    # function to return simulation values
    def simulation_values(self) -> dict[str: list[float]]:
        """
        Function that returns simulation values

        Parameters
        ----------
            None

        Returns
        -------
            model : dict[str : list[float]]\n
            Simulation values as a dictionary. The following keywords are supported:
                - "time_period": the time intervals (months) used for the simulation.\n
                - "initial_capital": the starting capital for the business over the simulation period.\n
                - "current_capital": business's own capital after reinvestment over the simulation period.\n
                - "bank_loan": the decrease in debt for the business over time.\n
                - "debt_payment": amount of debt paid in each interval.\n
                - "net_profit": the behaviour of net profit over the simulation period.
        """
        return self.model

    # function to return a basic matplotlib graph
    def simulation_graphs(self):
        """
        Function to return matplotlib figure and axes objects of "time_period" against the following:\n
            - "initial_capital": the starting capital for the business over the simulation period.\n
            - "current_capital": business's own capital after reinvestment over the simulation period.\n
            - "bank_loan": the decrease in debt for the business over time.\n
            - "debt_payment": amount of debt paid in each interval.\n
            - "net_profit": the behaviour of net profit over the simulation period.

        Parameters
        ----------
            None

        Returns
        -------
            (fig, ax1, ax2, ax3, ax4, ax5) : tuple[fig, Any]
        """
        t, initial_capital, current_capital, bank_loan, debt_payment, net_profit = self.model.values()
        y_formatter = lambda x, pos : f'{int(x / 1000):,}k' if (x >= 1000 or x<=-1000) else f'{x}'

        fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(10, 10))
        fig.suptitle(f"Conventional Model Simulation - {'SUCCESS' if self.status==1 else 'FAIL'}")

        ax1.plot(t, initial_capital)
        ax1.set(xlabel="time (months)", ylabel="Initial Capital")
        ax1.yaxis.set_major_formatter(FuncFormatter(y_formatter))
        ax1.grid()

        ax2.plot(t, current_capital)
        ax2.set(xlabel="time (months)", ylabel="Current Capital")
        ax2.yaxis.set_major_formatter(FuncFormatter(y_formatter))
        ax2.grid()

        ax3.plot(t, bank_loan)
        ax3.set(xlabel="time (months)", ylabel="Bank Loan")
        ax3.yaxis.set_major_formatter(FuncFormatter(y_formatter))
        ax3.grid()

        ax4.plot(t, debt_payment)
        ax4.set(xlabel="time (months)", ylabel="Debt Paid")
        ax4.yaxis.set_major_formatter(FuncFormatter(y_formatter))
        ax4.grid()

        ax5.plot(t, net_profit)
        ax5.set(xlabel="time (months)", ylabel="Net Profit")
        ax5.yaxis.set_major_formatter(FuncFormatter(y_formatter))
        ax5.grid()

        fig.delaxes(ax6)
        fig.tight_layout()

        return (fig, ax1, ax2, ax3, ax4, ax5)
