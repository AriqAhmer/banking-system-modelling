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

    profit_margin : float
        The percentage profit margin on the goods traded.
    
    expenses : float
        The amount to be spent on expenses during operation of business.
    
    interest_rate : float
        The interest rate charged by the bank.

    loan_period : int
        The expected time for paying back the loaned amount + interest.

    initial_capital_reinvestment : float
        The amount from the initial_capital to be reinvested into the business.
    
    dividend_payment : float
        The percentage of dividend expected to be paid to the business owner.

    ...

    Methods
    -------
    simulate(time_period : int, grace_period : int, verbose : bool = False):
        Simulates the business operating over a given time_period, t, from t=0 to t=time_period and returns relevant data.
    """
    
    def __init__(self, initial_capital: int, current_capital: int, profit_margin: float, expenses: float, interest_rate: float, loan_period: int, initial_capital_reinvestment: float, dividend_payment: float = 0.0) -> None:
        """
        Constructs the business model based on the parameters

        Parameters
        ----------
            initial_capital : int
                The capital amount loaned to the business by the Bank.
            
            current_capital : int
                The capital amount the business currently has before the venture begins.

            profit_margin : float
                The percentage profit margin on the goods traded.
            
            expenses : float
                The amount to be spent on expenses during operation of business.
            
            interest_rate : float
                The interest charged by the bank.
            
            loan_period : int
                The expected time (in years) for paying back the loaned amount + interest.

            initial_capital_reinvestment : float
                The amount from the initial_capital to be reinvested into the business.
            
            dividend_payment : float = 0.0
                The percentage of dividend expected to be paid to the business owner.
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

    def simulate(self, time_period: int, grace_period: int, verbose: bool = False) -> tuple[bool, int, float, float, float]:
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
            (status, t, net_profit, current_capital, bank_loan) : tuple[bool, int, float, float, float]\n
                status = True if simulation succeeded, False otherwise.\n
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
            
            if verbose:
                print(f"At {t = } month\nStarting Capital: {self.initial_capital:,.2f} | Current Capital: {self.current_capital:,.2f}")
            
            # get some amount from initial capital
            if self.initial_capital - self.initial_capital_reinvestment >= 0:
                investment = self.initial_capital_reinvestment + self.current_capital
                self.initial_capital -= self.initial_capital_reinvestment
            else:
                investment = self.initial_capital + self.current_capital
            
            # invest that amount and make profit
            profit = investment * self.profit_margin

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
            net_profit = profit - (bank_repayment + self.expenses)
            total_loan_paid += bank_repayment

            # calculate business's own capital
            self.current_capital += net_profit + investment

            if verbose:
                print(f"Amount invested: {investment:,.2f}")
                print(f"Profit made (@{self.profit_margin:.2%}): {profit:,.2f} | Amount paid to bank (@{self.interest_rate:.2%}): {bank_repayment:,.2f} | Net profit: {net_profit:,.2f}")
                print(f"Loan Remaining: {self.bank_loan:,.2f}")
                print(f"Amount Reinvested: {self.current_capital:,.2f}\n")

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
                print(f"Profit made (@{self.profit_margin:.2%}): {profit:,.2f} | Final bank payment (@{self.interest_rate:.2%}): {bank_repayment:,.2f} | Net profit: {net_profit:,.2f}")
                print(f"Amount Reinvested: {self.current_capital:,.2f}\n")
            
            case 2:
                print(f"\n---------END OF SIMULATION----------")
                print(f"Status: FAIL | Business is a LOSS MODEL")
                print(f"Total period of payment {t = } months | {'Within' if within_grace_period else 'After'} grace period\n")
                print(f"Loan Remaining: {self.bank_loan:,.2f} | Loan Paid: {total_loan_paid:,.2f}")
                print(f"Profit made (@{self.profit_margin:.2%}): {profit:,.2f} | Final bank payment (@{self.interest_rate:.2%}): {bank_repayment:,.2f} | Net profit: {net_profit:,.2f}")
                print(f"Amount Reinvested: {self.current_capital:,.2f}\n")

            case 3:
                print(f"\n---------END OF SIMULATION----------")
                print(f"Status: FAIL | Maximum time period reached")
                print(f"Total period of payment {t = } months | {'Within' if within_grace_period else 'After'} grace period\n")
                print(f"Loan Remaining: {self.bank_loan:,.2f} | Loan Paid: {total_loan_paid:,.2f}")
                print(f"Profit made (@{self.profit_margin:.2%}): {profit:,.2f} | Final bank payment (@{self.interest_rate:.2%}): {bank_repayment:,.2f} | Net profit: {net_profit:,.2f}")
                print(f"Amount Reinvested: {self.current_capital:,.2f}\n")

            case _:
                print(f"UNKNOWN CASE")

        return (status, t, round(net_profit, 2), round(self.current_capital, 2), round(self.bank_loan, 2))
