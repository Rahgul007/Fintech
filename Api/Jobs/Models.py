

from Settings import *





class Savings_Loan_Jobs(db.Model):
    __tablename__="savings_loan_jobs"
    id=db.Column(db.BigInteger(),primary_key=True)
    loan_id=db.Column(db.BigInteger())
    next_run_date=db.Column(db.Date())
    status_=[
        (0,"active"),
        (1,"inactive")
    ]
    status=db.Column(db.Integer(),ChoiceType(status_),default=0)
  
    def __repr__(self):
        return f"<Savings_loan_jobs>:{self.id}"

class Business_Loan_Jobs(db.Model):
    __tablename__="business_loan_jobs"
    id=db.Column(db.BigInteger(),primary_key=True)
    loan_id=db.Column(db.BigInteger())
    next_run_date=db.Column(db.Date())
    status_=[
        (0,"active"),
        (1,"inactive")
    ]
    status=db.Column(db.Integer(),ChoiceType(status_),default=0)
    
    
    def __repr__(self):
        return f"<Business_loan_jobs>:{self.id}"     



class Education_Loan_Jobs(db.Model):
    __tablename__="education_loan_jobs"
    id=db.Column(db.BigInteger(),primary_key=True)
    loan_id=db.Column(db.BigInteger())
    next_run_date=db.Column(db.Date())
    status_=[
        (0,"active"),
        (1,"inactive")
    ]
    status=db.Column(db.Integer(),ChoiceType(status_),default=0)
    
    
    def __repr__(self):
        return f"<Education_loan_jobs>:{self.id}"  



class Member_Savings_Jobs(db.Model):
    __tablename__="member_savings_jobs"
    id=db.Column(db.BigInteger(),primary_key=True)
    member_id=db.Column(db.BigInteger())
    next_run_date=db.Column(db.Date())
    status_=[
        (0,"active"),
        (1,"inactive")
    ]
    status=db.Column(db.Integer(),ChoiceType(status_),default=0)
   
    def __repr__(self):
        return f"<Member_savings_jobs>:{self.id}"    