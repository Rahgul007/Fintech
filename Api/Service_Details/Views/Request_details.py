from Settings import *
from Api.Service_Details.Models import *
from Api.Teams_Details.Models import *
from Api.Funds_Details.Models import *
from Api.Auth.Models import *















@app.route("/request_detail",methods=['POST'])
def add_request():
    try:
        data=request.get_json()
        if data:

            member=Member_Profile.query.filter_by(id=data['requested_by_id']).first()
            if not member:
                return jsonify(message="There is no member detail"),404

            if not App_Users.query.filter_by(id=data['action_by_user_id']).first():
                return jsonify({"message":"There is no app user details","status":False}),404

            if data['request_type']=="" or data['request_type']==None:
                return jsonify({"message":"please select valid request type"}),400

            if data['request_type']==0 or data['request_type']==1 or data['request_type']==2:


                min_savings_amount=2000
                member_savings=Member_Savings.query.filter_by(member_profile_id=data['requested_by_id']).all()
                if  member_savings:
                    if member_savings[-1].final_balance<min_savings_amount:
                        return jsonify(message="you cannot take this loan because you do not have minium balance"),400
                else:
                    return jsonify(message="You does not have any savings"),400

                tenure_month=data['number_of_emi']*12
                interest_=data['interest_rate']/12/100
                emi_amount=data['loan_amount']*interest_*pow((1+interest_),tenure_month)/(pow((1+interest_),tenure_month)-1)
                final_payment=emi_amount*tenure_month

                loan=Request_Details(
                    name=data['name'],
                    loan_amount=data['loan_amount'],
                    interest_rate=data['interest_rate'],
                    number_of_emi=data['number_of_emi'],
                    request_type=data['request_type'],
                    comments=data['comments'],
                    final_payment=float(format(final_payment,'.2f')),
                    applied_on=datetime.strptime(data['applied_on'],"%Y-%m-%d"),
                    requested_by_id=data['requested_by_id'],
                    action_by_user_id=data['action_by_user_id'],
                    reference_no=reference_number()
                )       
                if loan:
                    db.session.add(loan)
                    db.session.commit()
                    return jsonify(message="Successfully added new loan request"),201  
                else:
                    return jsonify(message="something wrong into request data in loans"),400  
            elif data['request_type']==3:

                benefit=Request_Details(
                    name=data['name'],
                    request_type=data['request_type'],
                    benefit_type=data['benefit_type'],
                    applied_on=datetime.strptime(data['applied_on'],"%Y-%m-%d"),
                    requested_by_id=data['requested_by_id'],
                    action_by_user_id=data['action_by_user_id'],
                    comments=data['comments'],
                    reference_no=reference_number()
                )
                if benefit:
                    db.session.add(benefit)
                    db.session.commit()
                    return jsonify(message="Successfully added new benefit request"),201  
                else:
                    return jsonify(message="something wrong into request data in benefits"),400               
            elif data['request_type']==4:

                pension_age=50
                birth_date=member.dob
                today=datetime.today()
                dob=date(birth_date.year,birth_date.month,birth_date.day)
                convert_age=today.year-dob.year-((today.month,today.day)<(dob.month,dob.day))
                
                if pension_age>convert_age:
                    return jsonify(message="You are not eligible to take a pension"),406

                pension=Request_Details(
                    name=data['name'],
                    request_type=data['request_type'],
                    pension_type=data['pension_type'],
                    applied_on=datetime.strptime(data['applied_on'],"%Y-%m-%d"),
                    comments=data['comments'],
                    requested_by_id=data['requested_by_id'],
                    action_by_user_id=data['action_by_user_id'],
                    reference_no=reference_number()
                )
                if pension:
                    db.session.add(pension)
                    db.session.commit()
                    return jsonify(message="Successfully added new pension request"),201  
                else:
                    return jsonify(message="something wrong into request data in pension"),400               
        else:
           return jsonify(message="Something went wrong into send data"),400
    except Exception as e:
        return jsonify({"message":str(e)}),500





@app.route('/all_request_list/<int:id>/<int:page>/<int:per_page>',methods=['GET'])
def get_member_request_list(id,page,per_page):
    try:
        status_id=id if id else 0
        all_member=Member_Profile.query.filter_by().all()
        if all_member:
            data=[]
            total_pending_request=0
            total_approved_request=0
            total_rejected_request=0
            total_closed_request=0
            for i in all_member:
                request_details=Request_Details.query.filter_by(requested_by_id=i.id).all()
                requet_count=Request_Details.query.filter_by(requested_by_id=i.id).count()
                if request_details:
                    request_name=""
                    status=""
                    if request_details[-1].request_type==0:
                        request_name="savings"
                    if request_details[-1].request_type==1:
                        request_name="business"
                    if request_details[-1].request_type==2:
                        request_name="education"        
                    if request_details[-1].request_type==3:
                        request_name="benefits"        
                    if request_details[-1].request_type==4:
                        request_name="pension"
                    if request_details[-1].status==0:
                        status="pending"
                    if request_details[-1].status==1:
                        status="approved"
                    if request_details[-1].status==2:
                        status="rejected"
                    request_date=date(request_details[-1].applied_on.year,request_details[-1].applied_on.month,request_details[-1].applied_on.day)
                    today=date(datetime.today().year,datetime.today().month,datetime.today().day)
                    day_elapsed=(today-request_date).days
                                
                    details={
                        "name":i.name,
                        "member_id":i.id,
                        "refer_id":i.reference_no,
                        "last_request":request_name,
                        "last_request_type":request_details[-1].request_type,
                        "last_applied_on":str(request_details[-1].applied_on),
                        "last_approval_status":request_details[-1].status,
                        "last_approval_status_name":status,
                        # "last_approved_date":str(request_details[-1].approved_date),
                        "total_request":requet_count,
                        "last_request_day_elapsed":day_elapsed
                    }
                    data.append(details)
                 
            # print(data)        
            for k in Request_Details.query.all():
                if k.status==0:
                    total_pending_request+=1
                if k.status==1:
                    total_approved_request+=1    
                if k.status==2:
                    total_rejected_request+=1    
                if k.status==3:
                    total_closed_request+=1       
        if data:
            new=[]
            
            for j in data:
                if j['last_approval_status']==status_id:
                    new.append(j)
                if status_id==4:
                    new.append(j)    
                        

            
            pag=get_rows(new,per_page)
            count = 0
            for i in pag[0]:
                count+=1
            if pag:    
                return jsonify(
                    {
                        "data":pag[page-1],"count":count,
                        "total_pending_request":total_pending_request,
                        "total_approved_request":total_approved_request,
                        "total_rejected_request":total_rejected_request,
                        "total_closed_request":total_closed_request,
                        "status":True
                    }
                ),200
            else:
                return jsonify(message="No request data"),404            
        else:
            
            return jsonify({"message":"No data"}),404    
       
    except Exception as e:
        return jsonify({"message":str(e)}),500    








@app.route("/request_detail/<int:id>/<int:page>/<int:per_page>",methods=['GET'])
def get_request_by_member_id(id,page,per_page):
    try:
        
        request_details=Request_Details.query.filter_by(requested_by_id=id).order_by(Request_Details.created_on.desc()).paginate(page=page,per_page=per_page,error_out=False)
        request_count=Request_Details.query.filter_by(requested_by_id=id).count()
        if request_details:
            member=Member_Profile.query.filter_by(id=id).first()
            return jsonify({"data":[Request_Details.request_json(i) for i in request_details.items],
                            "member_name":member.name,
                            "member_id":member.id,
                            "member_reference_no":member.reference_no,
                            "total_count":request_count
                            }),200
        else:
            return jsonify({"message":"No data","status":False}),404    
       
    except Exception as e:
        return jsonify({"message":str(e)}),500   
