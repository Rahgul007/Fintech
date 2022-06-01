from Settings import *



class Pension_Payment(db.Model):
    __tablename__="pension_payment"
    id =db.Column(db.BigInteger(),primary_key=True)
    month=db.Column(db.Integer(),nullable=False)
    year=db.Column(db.Integer(),nullable=False)
    paid_date=db.Column(db.Date(),nullable=True)
    amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)
    created_on=db.Column(db.DateTime(timezone=True),server_default=func.now())
    pension_id=db.Column(db.BigInteger(),nullable=False)
    
  
    
    def __repr__(self):
        return f"<Pension_payment>:{self.id}"


class Benefits_Type(db.Model):
    __tablename__="benefits_type"
    id =db.Column(db.BigInteger(),primary_key=True)
 
    benefit_type=db.Column(db.String(50),nullable=True)
    issued_on=db.Column(db.Date(),nullable=True)
    remarks=db.Column(db.String(150),nullable=True)
    created_on=db.Column(db.DateTime(timezone=True),server_default=func.now()) 




class Savings_Loan_Payment(db.Model):
    __tablename__ = 'savings_loan_payment'
    id = db.Column(db.BigInteger(),primary_key=True)

    month = db.Column(db.Integer(),nullable=True)
    year = db.Column(db.Integer(),nullable=True)
    emi_count = db.Column(db.Integer(),nullable=False)
    emi_amount= db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    paid_date = db.Column(db.Date,nullable=False)
    paid_status_=[
        (0,"No"),
        (1,"Yes")
    ]
    status=db.Column(db.Integer(),ChoiceType(paid_status_),default=0)
    # total_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    amount = db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    created_on = db.Column(db.DateTime(timezone=True),server_default=func.now())
    penalty_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True,default=0)
    savings_loan_id = db.Column(db.BigInteger())

   
    
    def __repr__(self):
        return f"<Savings_loan_payment>:{self.id}"



class Business_Loan_Payment(db.Model):
    __tablename__ = 'business_loan_payment'
    id = db.Column(db.BigInteger(),primary_key=True)

    month = db.Column(db.Integer(),nullable=True)
    year = db.Column(db.Integer(),nullable=True)
    emi_count = db.Column(db.Integer(),nullable=False)
    emi_amount= db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    paid_date = db.Column(db.Date,nullable=False)
    paid_status_=[
        (0,"No"),
        (1,"Yes")
    ]
    status=db.Column(db.Integer(),ChoiceType(paid_status_),default=0)
    # total_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    amount = db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    created_on = db.Column(db.DateTime(timezone=True),server_default=func.now())
    penalty_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True,default=0)
    business_loan_id = db.Column(db.BigInteger())

    def json(self):
        return {
            "business-loan_payment_id":self.id,
            "buiness_loan_id":self.business_loan_id,
            "penalty_amount":self.penalty_amount,
            "month":self.month,
            "year":self.year,
            "emi_count":self.emi_count,
            "paid_date":str(self.paid_date),
            "amount":self.amount,
            "created_on":str(self.created_on),
            "status":self.status
        }
    
    def __repr__(self):
        return f"<Business_loan_payment>:{self.id}"

 
class Education_Loan_Payment(db.Model):
    __tablename__ = 'education_loan_payment'
    id = db.Column(db.BigInteger(),primary_key=True)

    month = db.Column(db.Integer(),nullable=True)
    year = db.Column(db.Integer(),nullable=True)
    emi_count = db.Column(db.Integer(),nullable=False)
    emi_amount= db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    paid_date = db.Column(db.Date,nullable=False)
    paid_status_=[
        (0,"No"),
        (1,"Yes")
    ]
    status=db.Column(db.Integer(),ChoiceType(paid_status_),default=0)
    # total_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    amount = db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    created_on = db.Column(db.DateTime(timezone=True),server_default=func.now())
    penalty_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True,default=0)
    education_loan_id = db.Column(db.BigInteger())
    
    def __repr__(self):
        return f"<Savings_loan_payment>:{self.id}"