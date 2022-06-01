
from Settings import *
from Api.Teams_Details.Models import *


@app.route("/employee_list",methods=['GET'])
def get_employee_list():
    try:
       
        employee=Employees.query.filter_by(status=0).order_by(Employees.id.desc()).all()
        if employee:
            return jsonify({"data":[Employees.employee_list_json(i) for i in employee]}),200
        else:
            return jsonify({"message":"No data"}),404    
        
    except Exception as e:
        return jsonify({"message":str(e)}),500  






@app.route("/employee/<int:page>/<int:per_page>",methods=['GET'])
def get_employee(page,per_page):
    try:
        employee=Employees.query.filter_by(status=0).order_by(Employees.id.desc()).paginate(page=page,per_page=per_page,error_out=False)
        employee_count=Employees.query.filter_by(status=0).count()
        if employee:
            return jsonify({"data":[Employees.emp_json(i) for i in employee.items],"total_count":employee_count}),200
        else:
            return jsonify({"message":"No data"}),404    
        
    except Exception as e:
        return jsonify({"message":str(e)}),500   






@app.route("/employee/<int:id>",methods=['GET'])
def get_employee_by_id(id):
    try:
        employee=Employees.query.filter_by(id=id).first()
        if employee:
            return jsonify({"data":Employees.emp_by_json(employee)}),200
        else:
            return jsonify({"message":"No data from employee"}),404    
      
    except Exception as e:
        return jsonify({"message":str(e)}),500  






@app.route("/employee",methods=['POST'])
def add_employee():
    try:
        data=request.get_json()
        if data:

            
            if Employees.query.filter_by(mobile_no=data['mobile_no']).first():
                return jsonify(message="Mobile number is already exist"),401
            if Employees.query.filter_by(email=data['email']).first():
                return jsonify(message="email is already exist"),401
            if Employees.query.filter_by(aadhar_no=data['aadhar_no']).first():
                return jsonify(message="aadhar_no is already exist"),401
              

            employee=Employees(
                employee_type=data['employee_type'],
                name=data['name'],
                dob=datetime.strptime(data['dob'],'%Y-%m-%d'),
                gender=data['gender'],
                image_path=data['image_path'],
                address=data['address'],
                city=data['city'],
                district=data['district'],
                state=data['state'],
                email=data['email'],
                pincode=data['pincode'],
                aadhar_no=data['aadhar_no'],
                mobile_no=data['mobile_no'],
                join_date=datetime.strptime(data['join_date'],"%Y-%m-%d"),
                salary=data['salary'],
                reference_no=reference_number()
            )
            if employee:
                db.session.add(employee)
                db.session.commit()
                return jsonify({"message":"Successfully added new employee data"}),201
            else:
                return jsonify({"message":"something wrong into addings new employee data","status":False}),404    
        else:
            return jsonify({"message":"something went wrong in sending data","status":False}),404  
    except Exception as e:
        return jsonify({"message":str(e)}),500






@app.route("/employee/<int:id>",methods=['PUT'])
def update_employee(id):
    try:
        data=request.get_json()
        if data: 
            employee=Employees.query.filter_by(id=id).first()
            if employee:

                emp=Employees.query.all()
                if emp:
                    for i in emp:
                        if i.id!=employee.id:
                            if i.mobile_no==data['mobile_no']:
                                return jsonify(message="Mobile number is already exist"),401
                            if i.aadhar_no==data['aadhar_no']:
                                return jsonify(message="Aadhar number is already exist"),401
                            if i.email==data['email']:
                                return jsonify(message="Email id is already exist"),401

                
                employee.employee_type=data['employee_type'],
                employee.name=data['name'],
                employee.dob=datetime.strptime(data['dob'],"%Y-%m-%d"),
                employee.gender=data['gender'],
                employee.image_path=data['image_path'],
                employee.address=data['address'],
                employee.city=data['city'],
                employee.email=data['email'],
                employee.state=data['state'],
                employee.pincode=data['pincode'],
                employee.aadhar_no=data['aadhar_no'],
                employee.mobile_no=data['mobile_no'],
                employee.join_date=datetime.strptime(data['join_date'],"%Y-%m-%d"),
                employee.salary=data['salary'],
                employee.relieving_date=datetime.strptime(data['relieving_date'],"%Y-%m-%d") if data['relieving_date']!="" or None else None,
                
                db.session.commit()
                return jsonify({"message":"Successfully updated employee data"}),202
            else:
                return jsonify({"message":"something wrong into employee data"}),400    
        else:
             return jsonify({"message":"something went wrong in sending data"}),400  
    except Exception as e:
        return jsonify({"message":str(e)}),500





@app.route("/employee/<int:id>",methods=['DELETE'])
def delete_employee_by_id(id):
    try:
        employee=Employees.query.filter_by(id=id).first()
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return jsonify({"message":f"Successfully deleted id:{id} data","status":True}),202
        else:
            return jsonify({"message":"No data","status":False}),404    
    
    except Exception as e:
        return jsonify({"message":str(e)}),500   