from sqlalchemy import ForeignKey
from Settings import *



class Employees(db.Model):
    __tablename__="employees"
    id=db.Column(db.BigInteger(),primary_key=True)
    emp_type=[
        (0,"incharge")
    ]
    employee_type=db.Column(db.Integer(),ChoiceType(emp_type),default=0)
    name=db.Column(db.String(50),nullable=False)
    dob=db.Column(db.Date(),nullable=False)
    gen=[
        (0,"Male"),
        (1,"Female")
    ]
    gender=db.Column(db.Integer(),ChoiceType(gen),default=0)
    status_=[
        (0,"active"),
        (1,"deactive")
    ]
    status=db.Column(db.Integer(),ChoiceType(status_),nullable=False,default=0)
    image_path=db.Column(db.String(255),nullable=True)
    email=db.Column(db.String(100),unique=True)
    address=db.Column(db.String(255),nullable=True)
    city=db.Column(db.String(120),nullable=True)
    district=db.Column(db.String(120),nullable=True)
    state=db.Column(db.String(120),nullable=True)
    pincode=db.Column(db.Integer(),nullable=True)
    aadhar_no=db.Column(db.BigInteger(),nullable=True)
    mobile_no=db.Column(db.BigInteger(),nullable=True)
    join_date=db.Column(db.Date())
    salary=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    relieving_date=db.Column(db.Date(),nullable=True)
    created_on=db.Column(db.DateTime(timezone=True),nullable=True,server_default=func.now())
    reference_no=db.Column(db.BigInteger(),nullable=False,unique=True)

    member_details=db.relationship("Member_Profile",back_populates="incharge_details",cascade="all,delete",passive_deletes=True)
    
    def json(self):
        return {
            "employee_type":self.employee_type,
            "incharge_id":self.id,
            "name":self.name,
            "dob":str(self.dob),
            "gender":self.gender,
            "image_path":self.image_path,
            "address":self.address,
            "district":self.district,
            "city":self.city,
            "state":self.state,
            "status":self.status,
            "pincode":self.pincode,
            "aadhar_no":self.aadhar_no,
            "mobile_no":self.mobile_no,
            "join_date":str(self.join_date),
            "salary":self.salary,
            "relieving_date":str(self.relieving_date),
            "creadted_on":str(self.created_on),
            "reference_no":self.reference_no
        }
    def emp_json(self):
        age=0
        emp_age=Employees.query.filter_by(id=self.id).first()
        if emp_age:
            dob=date(emp_age.dob.year,emp_age.dob.month,emp_age.dob.day)
            today=datetime.today()
            age=today.year-dob.year-((today.month,today.day)<(dob.month,dob.day))
    
        return {
            "incharge_id":self.id,
            "name":self.name,
            "gender":self.gender,
            "age":age,
            "place":self.city,
            "mobile_no":self.mobile_no,
            "salary":self.salary,
            "reference_no":self.reference_no
        }

    def emp_by_json(self):
        age=0
        emp_age=Employees.query.filter_by(id=self.id).first()
        if emp_age:
            dob=date(emp_age.dob.year,emp_age.dob.month,emp_age.dob.day)
            today=datetime.today()
            age=today.year-dob.year-((today.month,today.day)<(dob.month,dob.day))

        status=""
        if self.status==0:
            status="Active"    
        if self.status==1:
            status="Deactive"    
    
        return {
            "incharge_id":self.id,
            "name":self.name,
            "gender":self.gender,
            "image":self.image_path,
            "age":age,
            "aadhar_no":self.aadhar_no,
            "place":self.city,
            "address":self.address,
            "join_date":str(self.join_date),
            "mobile_no":self.mobile_no,
            "salary":self.salary,
            "reference_no":self.reference_no,
            "relieving_date":str(self.relieving_date),
            "status":status
        }


    def employee_list_json(self):
        return {
            "employee_id":self.id,
            "name":self.name
        }
        
    
    def __repr__(self):
        return f"<Employees>:{self.id}" 









class Member_Profile(db.Model):
    __tablename__ = 'member_profile'
    id=db.Column(db.BigInteger(),primary_key=True)
    user_id=db.Column(db.String(10),nullable=True,unique=True)   #doubt user_id but string and this user id refer from where 
    name=db.Column(db.String(50),nullable=False)
    dob=db.Column(db.Date(),nullable=False)
    image_path=db.Column(db.String(255),nullable=True)
    gen=[
        (0,"male"),
        (1,"female")
    ]
    gender=db.Column(db.Integer(),ChoiceType(gen),default=0)
    address=db.Column(db.String(255),nullable=False)
    city=db.Column(db.String(120),nullable=False)
    state=db.Column(db.String(120),nullable=False)
    district=db.Column(db.String(120),nullable=False)
    pincode=db.Column(db.Integer(),nullable=False)
    auth_type=[
        (0,"Aadhar"),
        (1,"Driving")   
    ]
    auth_type_id=db.Column(db.Integer(),ChoiceType(auth_type),nullable=False,default=0)
    auth_data=db.Column(db.String(100),nullable=True)
    auth_path=db.Column(db.String(255),nullable=True)
    mobile_no=db.Column(db.BigInteger(),nullable=False)
    join_date=db.Column(db.Date(),nullable=False)
    santha_amount=db.Column(db.Float(precision=32,decimal_return_scale=None),nullable=True)
    Is_Leader=[
        (0,"No"),
        (1,"Yes")
    ]
    is_leader=db.Column(db.Integer(),ChoiceType(Is_Leader),nullable=False,default=0)
    leader_id=db.Column(db.BigInteger(),nullable=True)
    incharge_id=db.Column(db.BigInteger(),db.ForeignKey("employees.id",ondelete="CASCADE"),nullable=False)
    status_=[
        (0,"active"),
        (1,"closed"),
        (2,"suspended")
    ]
    status=db.Column(db.Integer(),ChoiceType(status_),nullable=False,default=0)
    last_status_change_date=db.Column(db.Date(),nullable=True)
    comments=db.Column(db.String(255),nullable=True)
    nominee_name=db.Column(db.String(255),nullable=True)
    nominee_dob=db.Column(db.Date(),nullable=True)
    nominee_relation=db.Column(db.String(255),nullable=True)
    nominee_mobile_no=db.Column(db.BigInteger(),nullable=True)
    nominee_aadhar_no=db.Column(db.BigInteger(),nullable=True)
    created_on=db.Column(db.DateTime(timezone=True),server_default=func.now())
    reference_no=db.Column(db.Integer(),nullable=False,unique=True)

    #relationship from employee table name called incharge
    incharge_details=db.relationship("Employees",back_populates="member_details")

    
    #relationship from santha_payment table name called santha details
    santha_details=db.relationship("Santha_Payment",back_populates="member_details",cascade="all,delete",passive_deletes=True)

    
    #relationship from member_savings table name called savings details
    member_savings_details=db.relationship("Member_Savings",back_populates="member_details",cascade="all,delete",passive_deletes=True)


    request_details=db.relationship("Request_Details",back_populates="member_details",cascade="all,delete",passive_deletes=True)

    
    
    def member_json(self):
       
        in_charge_name=""
        leader_name=""

        employee=Employees.query.filter_by(id=self.incharge_id).first()
        if employee:
            in_charge_name=employee.name

        member_name=Member_Profile.query.filter_by(id=self.leader_id).first()   
        if member_name:
            leader_name=member_name.name

        age=find_age(self.dob.year,self.dob.month,self.dob.day)    
        return {
            "member_profile_id":self.id,
            "name":self.name,
            "age":age,
            "image_path":self.image_path,
            "gender":self.gender,
            "address":self.address,
            "city":self.city,
            "state":self.state,
            "district":self.district,
            "pincode":self.pincode,
            "auth_type_id":self.auth_type_id,
            "auth_data":self.auth_data,
            "mobile_no":self.mobile_no,
            "join_date":str(self.join_date),
            "leader_name":leader_name,
            "incharge_name":in_charge_name,
            "status":self.status,
            "nominee_name":self.nominee_name,
            "nominee_relation":self.nominee_relation,
            "reference_no":self.reference_no
        }


    def mem_json(self):
        
        in_charge_name=""
        leader_name=""

        employee=Employees.query.filter_by(id=self.incharge_id).first()
        if employee:
            in_charge_name=employee.name

        member_name=Member_Profile.query.filter_by(id=self.leader_id).first()   
        if member_name:
            leader_name=member_name.name


        mem_age=Member_Profile.query.filter_by(id=self.id).first()
        if mem_age:
            dob=date(mem_age.dob.year,mem_age.dob.month,mem_age.dob.day)
            today=datetime.today()
            age=today.year-dob.year-((today.month,today.day)<(dob.month,dob.day))

        return {
            "member_profile_id":self.id,
            "user_id":self.user_id,
            "name":self.name,
            "age":age,
            "gender":self.gender,
            "city":self.city,
            "mobile_no":self.mobile_no,
            "leader_id":self.leader_id,
            "leader_name":leader_name,
            "incharge_id":self.incharge_id,
            "incharge_name":in_charge_name,
            "reference_no":self.reference_no
        }

    def lead_json(self):
        
        in_charge_name=""
        

        employee=Employees.query.filter_by(id=self.incharge_id).first()
        if employee:
            in_charge_name=employee.name

       


        lead_age=Member_Profile.query.filter_by(id=self.id).first()
        if lead_age:
            dob=date(lead_age.dob.year,lead_age.dob.month,lead_age.dob.day)
            today=datetime.today()
            age=today.year-dob.year-((today.month,today.day)<(dob.month,dob.day))

        return {
            "member_profile_id":self.id,
            "user_id":self.user_id,
            "name":self.name,
            "age":age,
            "gender":self.gender,
            "city":self.city,
            "mobile_no":self.mobile_no,
            "leader_id":self.leader_id,
            "incharge_id":self.incharge_id,
            "incharge_name":in_charge_name,
            "reference_no":self.reference_no
        }


    
    def __repr__(self):
        return f"<Member_Profile>:{self.name}:{self.id}"