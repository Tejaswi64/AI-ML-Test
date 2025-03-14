from manage_tables import db_connection

#member count is global variable
member_count = 20

class Account:
    def __init__(self, member_id, branch_id, balance, account_type):
        self.id = None  # Assigned by the DB
        self.member_id = member_id
        self.branch_id = branch_id
        self.balance = balance
        self.account_type = account_type
        self.connection = db_connection()

    def create_account(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO account (member_id, branch_id, balance, type, created_date)
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP);
        """, (self.member_id, self.branch_id, self.balance, self.account_type))
        self.connection.commit()
        self.id = cursor.fetchone()[0]
        print("Account created successfully!")
        #return self.id

    def add_money_to_account(self, amount):
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE account SET balance = balance + %s WHERE id = %s;
        """, (amount, self.id))
        self.connection.commit()
        print("Amount credited", amount)
    
    def withdraw_money(self, amount):
        if self.balance >= amount:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE account SET balance = balance - %s WHERE id = %s;
            """, (amount, self.id))
            self.connection.commit()
            print(f"Withdrew {amount}. Remaining balance updated.")
        else:
            print("Insufficient balance.")
    


class CheckingAccount(BaseAccount):

    def __init__(self, id, od, mi, ba, ty="Checking"):    
        super.__init__(id, od, mi, ba)
        self.type = ty

    def withdraw_money(self, amount, member_id):
        #check balance to be above ZERO
        """
        self.member_id = #instance variable
        BaseAccount.variable_name = #class variable
        member_id = 20 #local variable within this method"""

    def retrieve_account_details_with_type():

        return "member_id"
    

#multi level inheritance
class PremimumCheckingAccount(CheckingAccount):

    def __init__(self):
        super.__reduce_ex__

    def add_secondary_account_holder(self):

        return None

#multiple inheritance
class CheckingAccountMultiple(BaseAccount, BaseCountry):

    def __init__(self):
        pass

class SavingsAccount(BaseAccount):
    def __init__(self, id, od, mi, ba, ty, md):    
        super.__init__(id, od, mi, ba)
        self.type = ty
        self.monthly_deposit = md

    def withdraw_money(self, amount):
        #check balance to be above 500 and only 1 withdraw in a day.
        return True


    def retrieve_account_details_with_type():

        return "member_id"


checking1 = CheckingAccount()
baseAccount1 = BaseAccount()
baseAccount1.add_money_to_account()


checking1.add_money_to_account() #defined in base or inherited class
checking1.withdraw_money()
checking1.retrieve_account_details_with_type()