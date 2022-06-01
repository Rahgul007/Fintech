from Settings import *








class Category_Subcategory(db.Model):
    __tablename__ = 'category_subcategory'
    id = db.Column(db.Integer(),primary_key=True)
    category = db.Column(db.String(191),nullable=False,unique=True)
    sub_category = db.Column(db.String(191),nullable=False,unique=True)



class Income_details(db.Model):
    __tablename__ = 'income'
    id = db.Column(db.BigInteger(),primary_key=True)
    amount = db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)
    received_from = db.Column(db.String(100),nullable=True)
    ref_no = db.Column(db.String(255),nullable=True)
    description = db.Column(db.String(250),nullable=True)
    received_date = db.Column(db.Date,nullable=False)
    created_date = db.Column(db.DateTime(timezone=True),server_default=func.now())





class Expense_details(db.Model):
    __tablename__ = 'expense'
    id = db.Column(db.BigInteger(),primary_key=True)
    amount = db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=False)
    paid_to = db.Column(db.String(100),nullable=True)
    ref_no = db.Column(db.String(255),nullable=True)
    description = db.Column(db.String(250),nullable=True)
    paid_date = db.Column(db.Date,nullable=False)
    created_date = db.Column(db.DateTime(timezone=True),server_default=func.now())
