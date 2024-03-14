class IslamicModel:
    """
    A class for modelling the effect of Islamic Banking on a given business.
    The model assumes the Mudarabah model.

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

    bank_fee : float
        The percentage profit the bank expects to make on the loaned amount.
    
    bank_share : float
        The percentage of net profit given to the bank as a form of debt repayment. This is in terms of dividend 
        since the bank is in a profit/loss sharing parternship.

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
    
    def __init__(self, initial_capital: int, current_capital: int, profit_margin: float, expenses: float, bank_fee: float, bank_share: float, initial_capital_reinvestment: float, dividend_payment: float = 0.0) -> None:
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

            bank_fee : float
                The percentage profit the bank expects to make on the loaned amount.
            
            bank_share : float
                The percentage of net profit given to the bank as a form of debt repayment. This is in terms of dividend 
                since the bank is in a profit/loss sharing parternship.

            initial_capital_reinvestment : float
                The amount from the initial_capital to be reinvested into the business.
            
            dividend_payment : float = 0.0
                The percentage of dividend expected to be paid to the business owner.
        """
        self.initial_capital = initial_capital
        self.current_capital = current_capital
        self.profit_margin = profit_margin
        self.expenses = expenses
        self.bank_fee = bank_fee
        self.bank_share = bank_share
        self.initial_capital_reinvestment = initial_capital_reinvestment
        self.dividend_payment = dividend_payment
        
        self.bank_loan = initial_capital * (1 + self.bank_fee)
        self.business_loan = -initial_capital
        self.business_share = 1-bank_share

    # simulation function
    def simulate(self, time_period: int, grace_period: int, verbose: bool = False) -> tuple[int, int, float, float, float]:
        """
        Simulates the business operating over a given time_period, t, from t=0 to t=time_period.

        Parameters
        ----------
            time_period : int
                The time period (epochs) for the simulation duration

            grace_period : int
                Grace period given to the business to become operational and make actual profits.

            verbose : bool = False
                Whether to ouput simulation results for each time period (epoch)

        Returns
        -------
            (status, t, net_profit, current_capital, bank_loan) : tuple[int, int, float, float, float]\n
                status = 1 if simulation suceeded, 2 if business is a loss model (failed), 3 if maximum simulation time is reached and debt is not paid (failed)\n
                t = the time taken for simulation.\n
                net_profit = final net profit after final bank payment.\n
                current_capital = amount of capital owned entirely by the business.\n
                bank_loan = amount of loan remaining.\n
        """

        print(f"\nISLAMIC BANK SIMULATION\nBank Capital: {self.initial_capital:,.2f} | Bank Loan (@{self.bank_fee:.2%}): {self.bank_loan:,.2f}")

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

            # subtract expenses + profit amount paid to bank, to get net profit
            net_profit = profit - self.expenses

            # update loan amounts
            if self.bank_loan > 0:

                # calculate profit share for bank to be paid and update the amount
                bank_repayment = net_profit * self.bank_share
                net_profit -= bank_repayment

                # pay to the bank only what's needed and not more
                if bank_repayment <= self.bank_loan:
                    self.bank_loan -= bank_repayment
                    self.business_loan += bank_repayment
                else:
                    net_gain = bank_repayment - self.bank_loan
                    bank_repayment = self.bank_loan
                    self.bank_loan = 0

                    net_profit += net_gain

            # running total of total loan amount paid
            total_loan_paid += bank_repayment

            # calculate business's own capital
            self.current_capital += net_profit + investment

            if verbose:
                print(f"Amount invested: {investment:,.2f}")
                print(f"Profit made (@{self.profit_margin:.2%}): {profit:,.2f} | Profit paid to bank (@{self.bank_share:.2%}): {bank_repayment:,.2f} | Net profit: {net_profit:,.2f}")
                print(f"Loan Remaining: {self.bank_loan:,.2f}")
                print(f"Amount Reinvested: {self.current_capital:,.2f}\n")

            if (self.bank_loan == 0) and (net_profit>0 or self.current_capital>0):
                within_grace_period: bool = t <= grace_period
                status = 1
                break
            elif (t == grace_period) and (net_profit < 0 or self.current_capital < 0):
                within_grace_period: bool = t <= grace_period
                status = 2
                break
            else:
                within_grace_period: bool = t <= grace_period
                status = 3

        
        match status:

            case 1:
                print(f"\n---------END OF SIMULATION----------")
                print(f"Status: SUCCESS")
                print(f"Total period of payment {t = } months | {'Within' if within_grace_period else 'After'} grace period\n")
                print(f"Loan Remaining: {self.bank_loan:,.2f} | Loan Paid: {total_loan_paid:,.2f}")
                print(f"Profit made (@{self.profit_margin:.2%}): {profit:,.2f} | Final bank payment (@{self.bank_share:.2%}): {bank_repayment:,.2f} | Net profit: {net_profit:,.2f}")
                print(f"Amount Reinvested: {self.current_capital:,.2f}\n")

            case 2:
                print(f"\n---------END OF SIMULATION----------")
                print(f"Status: FAIL | Business is a LOSS MODEL")
                print(f"Total period of payment {t = } months | {'Within' if within_grace_period else 'After'} grace period\n")
                print(f"Loan Remaining: {self.bank_loan:,.2f} | Loan Paid: {total_loan_paid:,.2f}")
                print(f"Profit made (@{self.profit_margin:.2%}): {profit:,.2f} | Final bank payment (@{self.bank_share:.2%}): {bank_repayment:,.2f} | Net profit: {net_profit:,.2f}")
                print(f"Amount Reinvested: {self.current_capital:,.2f}\n")

            case 3:
                print(f"\n---------END OF SIMULATION----------")
                print(f"Status: FAIL | Maximum time period reached")
                print(f"Total period of payment {t = } months | {'Within' if within_grace_period else 'After'} grace period\n")
                print(f"Loan Remaining: {self.bank_loan:,.2f} | Loan Paid: {total_loan_paid:,.2f}")
                print(f"Profit made (@{self.profit_margin:.2%}): {profit:,.2f} | Final bank payment (@{self.bank_share:.2%}): {bank_repayment:,.2f} | Net profit: {net_profit:,.2f}")
                print(f"Amount Reinvested: {self.current_capital:,.2f}\n")

            case _:
                print(f"UNKNOWN CASE")

        return (status, t, round(net_profit, 2), round(self.current_capital, 2), round(self.bank_loan, 2))
