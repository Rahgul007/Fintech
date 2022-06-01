from  Settings import *
from Api.Teams_Details.Models import *



@app.route("/member/<int:page>/<int:per_page>",methods=['GET'])
def get_member(page,per_page):
    try:
        member=Member_Profile.query.filter_by(status=0).filter_by(is_leader=0).paginate(page=page,per_page=per_page,error_out=False)
        member_count=Member_Profile.query.filter_by(status=0).filter_by(is_leader=0).count()
        if member:
            return jsonify({"data":[Member_Profile.mem_json(i) for i in reversed(member.items)],"total_count":member_count}),200
        else:
            return jsonify({"message":"No data"}),404    
        
    except Exception as e:
        return jsonify({"message":str(e)}),500   






@app.route("/member/<int:id>",methods=['GET'])
def get_member_by_id(id):
    try:
       
        member=Member_Profile.query.filter_by(id=id).first()
        if member:
            pension_amount=0
            total_request=0
            pending=0
            approved=0
            rejected=0
            benefits=[]
            savings_loan_=0
            business_loan_=0
            education_loan_=0
            withdraw=0
            balance_in_account=0
            total_savings=0
            pension_amount=0
            # pension=Pension.query.filter_by(member_id=member.id).first()
            # if pension:
            #     pension_amount=pension.pension_monthly_amount

            # request=Request_Details.query.filter_by(requested_by_id=member.id).all()
           
            # if request:
            #     pending=0
            #     approved=0
            #     rejected=0
            
            #     for i in request:
            #         if i.status==0:
            #             pending+=1
            #         if i.status==1:
            #             approved+=1
            #         if i.status==2:
            #             rejected+=1
            #     request_detail.append({"pending":pending,"approved":approved,"rejected":rejected})

            # savings=Member_Savings.query.filter_by(member_profile_id=member.id).all() 
              
            # if savings:
                
            #     withdraw=0
            #     balance_in_account=savings[-1].final_balance
                
            #     for j in savings:
            #         if 0>j.payment_amount:
            #             withdraw+=j.payment_amount
            #     total_savings=withdraw+balance_in_account  
            #     funds.append({"withdraw":withdraw,"balance_in_account":balance_in_account,"total_savings":total_savings}) 

            
            # benefit_details=Benefits.query.filter_by(member_id=member.id).all()
            # if benefit_details:
            #     for k in benefit_details:
            #         benefits.append(k.benefit_type)
            
            # savings_loan=Savings_Loan.query.filter_by(member_id=member.id).first()
            # savings_loan_=0
            # if savings_loan:
            #     savings_loan_=business_loan.final_payment_amount
            # business_loan=Business_Loan.query.filter_by(member_id=member.id).first()
            # business_loan_=0
            # if business_loan:
            #     business_loan_=business_loan.final_payment_amount
            # education_loan=Education_Loan.query.filter_by(member_id=member.id).first()
            # education_loan_=0
            # if education_loan:
            #     education_loan_=education_loan.final_payment_amount
            # loan.append({"savings_loan":savings_loan_,"business_loan":business_loan_,"education_loan":education_loan_})




            return jsonify({"data":Member_Profile.member_json(member),
                            "funds":{"withdraw":withdraw,"balance_in_account":balance_in_account,"total_savings":total_savings},
                            "loan(open)":{"savings_loan":savings_loan_,"business_loan":business_loan_,"education_loan":education_loan_},
                            "repayment":[],
                            "pension":pension_amount,
                            "request":{"pending":pending,"approved":approved,"rejected":rejected,"request":total_request},
                            "benfit":benefits,
                        }),200
        else:
            return jsonify({"message":"No data","status":False}),404    
    
    except Exception as e:
        return jsonify({"message":str(e)}),500   





@app.route("/member",methods=['POST'])
def add_member():
    try:
        data=request.get_json()
        if data:

            leader_id=0
            if data['is_leader']==1:
                leader_id=0
            elif data['is_leader']==0:
                if data['leader_id']=="" or data['leader_id']==None:
                    return jsonify(message="please enter leader id"),404
                leader_id=data['leader_id']
                leader=Member_Profile.query.filter_by(id=leader_id).filter_by(is_leader=1).first()
                if leader==None:
                    return jsonify(message="Leader id does not valid"),404
            else:    
                return jsonify(message="Invalid is_leader choice"),401 

        
            if Member_Profile.query.filter_by(status=0).filter_by(mobile_no=data['mobile_no']).first():
                return jsonify(message="Mobile number is already exist"),401
            if Member_Profile.query.filter_by(status=0).filter_by(auth_data=data['auth_data']).first():
                return jsonify(message="Aadhar number is already exist"),401
            
           
          
            if not Employees.query.filter_by(id=data['incharge_id']).first():
                return jsonify({"message":"incharge does not exist"}),404

            member=Member_Profile(
                name=data['name'],
                dob=datetime.strptime(data['dob'],"%Y-%m-%d"),
                gender=data['gender'],
                image_path=data['image_path'],
                address=data['address'],
                city=data['city'],
                state=data['state'],
                district=data['district'],
                pincode=data['pincode'],
                auth_data=data['auth_data'],
                auth_path=data['auth_path'],
                auth_type_id=data['auth_type_id'],
                mobile_no=data['mobile_no'],
                join_date=datetime.strptime(data['join_date'],"%Y-%m-%d"),
                santha_amount=format(1000,".2f"),
                is_leader=data['is_leader'],
                leader_id=leader_id,
                incharge_id=data['incharge_id'],
                comments=data['comments'],
                nominee_name=data['nominee_name'],
                nominee_relation=data['nominee_relation'],
                nominee_dob=datetime.strptime(data['nominee_dob'],"%Y-%m-%d"),
                nominee_mobile_no=data['nominee_mobile_no'],
                nominee_aadhar_no=data['nominee_aadhar_no'],
                reference_no=reference_number()
            )
            if member:
                db.session.add(member)
                db.session.commit()
                return jsonify({"message":"Successfully added new data"}),201
            else:
                return jsonify({"message":"something wrong into employee data","status":False}),404    
        else:
             return jsonify({"message":"something went wrong in sending data","status":False}),404  
    except Exception as e:
        return jsonify({"message":str(e)}),500







@app.route("/member/<int:id>",methods=['PUT'])
def update_member(id):
    try:
        data=request.get_json()
        if data: 
            member=Member_Profile.query.filter_by(id=id).first()
            if member:

                if not Employees.query.filter_by(id=data['incharge_id']).first():
                    return jsonify({"message":"incharge does not exist"}),401

                leader_id=0
                if data['is_leader']==1:
                    leader_id=0
                elif data['is_leader']==0:
                    if data['leader_id']=="" or data['leader_id']==None:
                        return jsonify(message="please enter leader id"),401

                    leader_id=data['leader_id']
                    leader=Member_Profile.query.filter_by(id=leader_id).filter_by(is_leader=1).first()
                    if leader==None:
                        return jsonify(message="Leader id does not valid"),404
                else:    
                    return jsonify(message="Invalid is_leader choice"),401 

                mem=Member_Profile.query.all()
                if mem:
                    for i in mem:
                        if i.id!=member.id:
                            if i.mobile_no==data['mobile_no']:
                                return jsonify(message="Mobile number is already exist"),401
                            if i.auth_data==data['auth_data']:
                                return jsonify(message="Aadhar number is already exist"),401
                            # if i.email==data['email']:
                            #     return jsonify(message="Email id is already exist"),401
            
                member.name=data['name'],
                member.dob=datetime.strptime(data['dob'],"%Y-%m-%d"),
                member.gender=data['gender'],
                member.image_path=data['image_path'],
                member.address=data['address'],
                member.city=data['city'],
                member.state=data['state'],
                member.district=data['district'],
                member.pincode=data['pincode'],
                member.auth_data=data['auth_data'],
                member.auth_path=data['auth_path'],
                member.auth_type_id=data['auth_type_id'],
                member.mobile_no=data['mobile_no'],
                member.join_date=datetime.strptime(data['join_date'],"%Y-%m-%d"),
                member.is_leader=data['is_leader'],
                member.leader_id=leader_id,
                member.comments=data['comments'],
                member.nominee_name=data['nominee_name'],
                member.nominee_relation=data['nominee_relation'],
                member.nominee_dob=data['nominee_dob'],
                member.nominee_mobile_no=data['nominee_mobile_no'],
                member.nominee_aadhar_no=data['nominee_aadhar_no'],
                member.status=data['status']
                member.last_status_change_date=datetime.now()

                
                db.session.commit()
                return jsonify({"message":"Successfully updated data"}),202
            else:
                return jsonify({"message":"something wrong into member data",}),401    
        else:
             return jsonify({"message":"something went wrong in sending data",}),404  
    except Exception as e:
        return jsonify({"message":str(e)}),500





@app.route("/member/<int:id>",methods=['DELETE'])
def delete_member_by_id(id):
    try:
        member=Member_Profile.query.filter_by(id=id).first()
        if member:
            check=Member_Profile.query.filter_by(leader_id=member.id).first()
            if check:
                return jsonify(message="You are the leader of the some members so you can not delete this account")
            db.session.delete(member)
            db.session.commit()
            return jsonify({"message":f"Successfully deleted id:{id} data"}),202
        else:
            return jsonify({"message":"No data"}),404    
    
    except Exception as e:
        return jsonify({"message":str(e)}),500     