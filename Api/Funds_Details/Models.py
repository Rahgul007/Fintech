from Settings import *




class Santha_Payment(db.Model):
    __tablename__="santha_payment"
    id=db.Column(db.BigInteger(),primary_key=True)
    santha_for_year=db.Column(db.Integer(),nullable=False,default=0)
    santha_amount_received=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False,default=0)
    received_date=db.Column(db.Date(),nullable=True)
    
    created_on=db.Column(db.DateTime(timezone=True),server_default=func.now())
    annual_contribution=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True,default=0)
    reference_no=db.Column(db.BigInteger(),nullable=False,unique=True)
    member_profile_id=db.Column(db.BigInteger(),db.ForeignKey("member_profile.id",ondelete="CASCADE"),nullable=False)

    #connection from member profile
    member_details=db.relationship("Member_Profile",back_populates="santha_details")


    def santha_payment_json(self):
        return {
            "reference_no":self.reference_no,
            "santha_payment_id":self.id,
            "santha_year":self.santha_for_year,
            "amount_received":self.santha_amount_received,
            "received_date":str(self.received_date)
        }

    def __repr__(self):
        return f"<Santha_Payment>:{self.id}"





        

class Member_Savings(db.Model):
    __tablename__="member_savings"
    id=db.Column(db.BigInteger(),primary_key=True)
    date=db.Column(db.Date(),nullable=False)
    initial_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False,default=0)
    payment_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False,default=0)
    final_balance=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)
    created_on=db.Column(db.DateTime(timezone=True),server_default=func.now())
    reference_no=db.Column(db.BigInteger(),nullable=False,unique=True)
    member_profile_id=db.Column(db.BigInteger(),db.ForeignKey("member_profile.id",ondelete="CASCADE"),nullable=False)

    member_details=db.relationship("Member_Profile",back_populates="member_savings_details")
    
    def member_savings_payment_json(self):
        week=get_week_of_month(self.date.year,self.date.month,self.date.day)
        month=self.date.strftime("%b-%Y")
        return {
            "saving_payment_id":self.id,
            "amount":self.payment_amount,
            "initial_amount":self.initial_amount,
            "month":month,
            "week":int(week),
            "received_date":str(self.created_on)
        }
    def member_savings_withdraw_json(self):
       
        return {
            "saving_payment_id":self.id,
            "withdraw_amount":self.payment_amount, 
            "withdraw_date":str(self.created_on)
        }
    
    def __repr__(self):
        return f"<member_savings>:{self.id}"     