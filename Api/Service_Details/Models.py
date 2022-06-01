from Settings import *
from Api.Teams_Details.Models import *
from Api.Auth.Models import *
# from Api.Services_Details.Payment.Models import *


class Request_Details(db.Model):
    __tablename__="request"
    id =db.Column(db.BigInteger(),primary_key=True)
    name=db.Column(db.String(100),nullable=True)
    loan_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True,default=0)
    number_of_emi=db.Column(db.Integer(),nullable=True)
    interest_rate=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    final_payment=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    req_type=[
        (0,"savings"),
        (1,"business"),
        (2,"education"),
        (3,"benefit"),
        (4,"pension")
    ]
    request_type=db.Column(db.Integer(),ChoiceType(req_type),nullable=False,default=0)
    applied_on=db.Column(db.Date(),nullable=False)
    status_=[
        (0,"pending"),
        (1,"approved"),
        (2,"rejected")
    ]
    status=db.Column(db.Integer(),ChoiceType(status_),nullable=False,default=0)
    approved_date=db.Column(db.Date(),nullable=True)
    comments=db.Column(db.String(100),nullable=True)
    created_on=db.Column(db.DateTime(timezone=True),server_default=func.now())
    benefit_type=db.Column(db.String(100),nullable=True)
    pension_type=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    requested_by_id = db.Column(db.BigInteger(),db.ForeignKey("member_profile.id",ondelete="CASCADE"),nullable=False)
    action_by_user_id = db.Column(db.BigInteger(),db.ForeignKey("app_users.id",ondelete="CASCADE"),nullable=False)
    reference_no=db.Column(db.BigInteger(),nullable=False)


    member_details=db.relationship("Member_Profile",back_populates="request_details")


    app_user_details=db.relationship("App_Users",back_populates="request_details")



    def request_json(self):
        status_name=""
        req_type=""
        if self.request_type==0:
            req_type="Savings_loan"
        if self.request_type==1:
            req_type="Business_loan"
        if self.request_type==2:
            req_type="Education_loan"
        if self.request_type==3:
            req_type="Benefit"
        if self.request_type==4:
            req_type="Pension"
        if self.status==0:
            status_name="pending"
        if self.status==1:
            status_name="approved"
        if self.status==2:
            status_name="rejected"

        return {
            "request_id":self.id,
            "request_type":req_type,
            "applied_date":str(self.applied_on),
            "approved_status":status_name
        }
    def json(self):
        return {

        }    
    
    
    def __repr__(self):
        return f"<Request>:{self.id}"










class Pension(db.Model):
    __tablename__="pension"
    id =db.Column(db.BigInteger(),primary_key=True)
    Status_=[
        (0,"pending"),
        (1,"active"),
        (2,"closed")
    ]
    status=db.Column(db.Integer(),ChoiceType(Status_),nullable=False,default=0)
    pension_monthly_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)
    start_date=db.Column(db.Date(),nullable=True)
    end_date=db.Column(db.Date(),nullable=True)
    remarks=db.Column(db.String(50),nullable=True)
    created_on=db.Column(db.DateTime(timezone=True),server_default=func.now())
    reference_no=db.Column(db.BigInteger(),nullable=False)
    approved_date=db.Column(db.Date(),nullable=True)
    approved_by_id=db.Column(db.BigInteger(),nullable=False)
    member_id=db.Column(db.BigInteger(),nullable=False)

    
    def __repr__(self):
        return f"<pensions>:{self.id}" 






class Benefits(db.Model):
    __tablename__="benefits"
    id =db.Column(db.BigInteger(),primary_key=True)
    status_=[
        (0,"pending"),
        (1,"active"),
        (2,"closed")
    ]
    status=db.Column(db.Integer(),ChoiceType(status_),nullable=False,default=0)
    benefit_type=db.Column(db.String(50),nullable=True)
    approved_on=db.Column(db.Date(),nullable=True)
    issued_on=db.Column(db.Date(),nullable=True)
    remarks=db.Column(db.String(150),nullable=True)
    created_on=db.Column(db.DateTime(timezone=True),server_default=func.now())
    reference_no=db.Column(db.BigInteger(),nullable=True)
    approved_by_id=db.Column(db.BigInteger(),nullable=False)
    member_id=db.Column(db.BigInteger(),nullable=False)

    
    def __repr__(self):
        return f"<benefit>:{self.id}" 



class Savings_Loan(db.Model):
    __tablename__="savings_loan"
    id= db.Column(db.BigInteger(),primary_key=True)
    status_=[
        (0,"active"),
        (1,"closed"),
        (2,"defaulted")
    ]
    status= db.Column(db.Integer(),ChoiceType(status_),default=0,nullable=True)
    loan_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    emi_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    interest_rate= db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    final_payment_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    monthly_penalty_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    penalty_interest_percentage=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    months_to_charge_penalty_interest= db.Column(db.Integer(),nullable=True)
    number_of_emi= db.Column(db.Integer(),nullable=True)
    emi_start_date= db.Column(db.Date(),nullable=True)
    loan_end_date= db.Column(db.Date(),nullable=True)
    emi_on_date= db.Column(db.Integer(),nullable=True) #'last day to pay emi every month',
    comments= db.Column(db.String(100),nullable=True)
    loan_approved_by= db.Column(db.Integer(),default=True)
    member_id= db.Column(db.Integer(),default=True)
    created_on= db.Column(db.DateTime(timezone=True),server_default=func.now())
    issued_date=db.Column(db.Date(),nullable=True)
    req_approved_date=db.Column(db.Date(),nullable=True)
    reference_no=db.Column(db.BigInteger(),nullable=False)
  

   
    def __repr__(self):
        return f"<savings_loan>:{self.id}"


class Education_Loan(db.Model):
    __tablename__="education_loan"
    id= db.Column(db.BigInteger(),primary_key=True)
    status_=[
        (0,"active"),
        (1,"closed"),
        (2,"defaulted")
    ]
    status= db.Column(db.Integer(),ChoiceType(status_),default=0,nullable=True)
    loan_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    emi_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    interest_rate= db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    final_payment_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    monthly_penalty_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    penalty_interest_percentage=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    months_to_charge_penalty_interest= db.Column(db.Integer(),nullable=True)
    number_of_emi= db.Column(db.Integer(),nullable=True)
    emi_start_date= db.Column(db.Date(),nullable=True)
    loan_end_date= db.Column(db.Date(),nullable=True)
    emi_on_date= db.Column(db.Integer(),nullable=True) #'last day to pay emi every month',
    comments= db.Column(db.String(100),nullable=True)
    loan_approved_by= db.Column(db.Integer(),default=True)
    member_id= db.Column(db.Integer(),default=True)
    created_on= db.Column(db.DateTime(timezone=True),server_default=func.now())
    issued_date=db.Column(db.Date(),nullable=True)
    req_approved_date=db.Column(db.Date(),nullable=True)
    reference_no=db.Column(db.BigInteger(),nullable=False)


    
    def __repr__(self):
        return f"<education_loan>:{self.id}"




class Business_Loan(db.Model):
    __tablename__="business_loan"
    id= db.Column(db.BigInteger(),primary_key=True)
    status_=[
        (0,"active"),
        (1,"closed"),
        (2,"defaulted")
    ]
    status= db.Column(db.Integer(),ChoiceType(status_),default=0,nullable=True)
    loan_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    emi_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    interest_rate= db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    final_payment_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    monthly_penalty_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    penalty_interest_percentage=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    months_to_charge_penalty_interest= db.Column(db.Integer(),nullable=True)
    number_of_emi= db.Column(db.Integer(),nullable=True)
    emi_start_date= db.Column(db.Date(),nullable=True)
    loan_end_date= db.Column(db.Date(),nullable=True)
    emi_on_date= db.Column(db.Integer(),nullable=True) #'last day to pay emi every month',
    comments= db.Column(db.String(100),nullable=True)
    loan_approved_by= db.Column(db.Integer(),default=True)
    member_id= db.Column(db.Integer(),default=True)
    created_on= db.Column(db.DateTime(timezone=True),server_default=func.now())
    issued_date=db.Column(db.Date(),nullable=True)
    req_approved_date=db.Column(db.Date(),nullable=True)
    reference_no=db.Column(db.BigInteger(),nullable=False)



    
    def __repr__(self):
        return f"<business_loan>:{self.id}"




