from Settings import *







class App_Users(db.Model):
    __tablename__="app_users"
    id=db.Column(db.BigInteger(),primary_key=True)
    name=db.Column(db.String(70),nullable=False)
    role=[
        (0,"user"),
        (1,"adimn"),
        (2,"finance"),
        (3,"super_admin")
    ]
    role_id=db.Column(db.Integer(),ChoiceType(role),nullable=False,default=0)
    user_name=db.Column(db.String(70),nullable=False,unique=True)
    image_path=db.Column(db.String(255),nullable=True)
    encrypted_password=db.Column(db.String(255),nullable=False)
    email=db.Column(db.String(70),nullable=False,unique=True)
    mobile=db.Column(db.Integer(),nullable=False,unique=True)
    created_on=db.Column(db.DateTime(timezone=True),nullable=False,server_default=func.now())
    status_=[
        (0,"active"),
        (1,"deactive")
        ]
    status=db.Column(db.Integer(),ChoiceType(status_),nullable=False,default=0)
    reference_no=db.Column(db.Integer(),nullable=False)

    request_details=db.relationship("Request_Details",back_populates="app_user_details",cascade="all,delete",passive_deletes=True)


    def json(self):
        return {
            "app_user_id":self.id,
            "name":self.name,
        }
    
    def __repr__(self):
        return f"<App_Users>:{self.id}"    
