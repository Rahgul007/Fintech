from Settings import *
from Api.Funds_Details.Models import *
from Api.Teams_Details.Models import *






@app.route("/all_member_savings/<int:page>/<int:per_page>",methods=['GET'])
def all_member_savings_list(page,per_page):
    try:
        member_profile=Member_Profile.query.all()
        
        if member_profile:
            data=[]
            for i in member_profile:
                interest=10
                total_savings=0
                total_withdraw=0
                month_name=""
                week=0
                due=0
                total_savings=0
                previous_payment=0
                received_date=""
                current_savings=0
                previous_withdraw=0
                todays=date.today()
                member_savings=Member_Savings.query.filter_by(member_profile_id=i.id).all()
                if member_savings:
                    received_date=member_savings[-1].date
                    month_name=received_date.strftime("%b-%Y")
                    current_savings=member_savings[-1].final_balance
                    total_savings=member_savings[-1].final_balance
                    total_amount=0

                    withdraw=[]
                    payment=[]
                    for j in member_savings:
                        if 0>j.payment_amount:
                            withdraw.append(j.payment_amount)
                            total_amount+=abs(j.payment_amount)
                            total_withdraw=total_amount 
                        else:
                            payment.append(j.payment_amount)

                    if withdraw:
                        previous_withdraw=withdraw[-1]
                    if payment:
                        previous_payment=payment[-1]

                    previous_savings_date = date(received_date.year,received_date.month,received_date.day)

                    current_date = date(todays.year,todays.month,todays.day)

                    days_elapsed=(current_date-previous_savings_date).days

                    week=get_week_of_month(received_date.year,received_date.month,received_date.day)

                    due=(days_elapsed//7)+1
               
                    data.append({
                        "interest":interest,
                        "name":i.name,
                        "members_profile_id":i.id,
                        "ref_no":i.reference_no,
                        "due":due,
                        "week":int(week),
                        "month":month_name,
                        "total_withdraw":total_withdraw,
                        "previous_withdraw":previous_withdraw,
                        "total_savings":total_savings+abs(total_withdraw),
                        "previous_payment":previous_payment,
                        "received_on":str(received_date),
                        "current_savings":current_savings
                    })
                              
        if data:
            paginating=get_rows(data,per_page)
            count=0
            for i in paginating:
                count+=1
            if paginating:
                return jsonify({"data":paginating[page-1],"status":True,"count":count}),200
            else:
                return jsonify({"message":"No member savings","status":False}),404    
        else:
            return jsonify({"message":"No data","status":False}),404

        
    except Exception as e:
        return jsonify({"message":str(e)}),500   










@app.route("/member_savings_payment/<int:id>/<int:page>/<int:per_page>",methods=['GET'])
def all_member_savings_payment_by_id(id,page,per_page):
    try:
        member_savings=Member_Savings.query.filter_by(member_profile_id=id).order_by(Member_Savings.id.desc()).paginate(page=page,per_page=per_page,error_out=False)
        if member_savings:
            count=0
            for j in member_savings.items:
                if 0<j.payment_amount or 0<j.initial_amount:
                    count+=1
            return jsonify({"data":[Member_Savings.member_savings_payment_json(i) for i in member_savings.items if 0<=i.payment_amount],"total_count":count}),200
        else:
            return jsonify({"message":"No payment data",}),404    
    except Exception as e:
        return jsonify({"message":str(e)}),500  





@app.route("/member_savings_withdrawal/<int:id>/<int:page>/<int:per_page>",methods=['GET'])
def all_member_savings_withdrawal_by_id(id,page,per_page):
    try:
        member_savings=Member_Savings.query.filter_by(member_profile_id=id).order_by(Member_Savings.id.desc()).paginate(page=page,per_page=per_page,error_out=False)
        if member_savings:
            count=0
            for j in member_savings.items:
                if 0>j.payment_amount:
                    count+=1
                  
            return jsonify({"data":[Member_Savings.member_savings_withdraw_json(i) for i in member_savings.items if 0>i.payment_amount],"status":True,"total_count":count}),200
        else:
            return jsonify({"message":"No withdrawal data","status":False}),404    
      
    except Exception as e:
        return jsonify({"message":str(e)}),500   






@app.route('/member_savings',methods=['POST'])
def add_member_savings():
    try:
        min_amount=100
        max_amount=500
        data=request.get_json()


        if not Member_Profile.query.filter_by(id=data['member_profile_id']).first():
            return jsonify({"message":"member data not found"}),404
        
        payment_amount=data['payment_amount']
        if data['payment_amount']=="" or data['payment_amount']==None:
            payment_amount=0
    
        if 0<payment_amount:
            savings=Member_Savings.query.filter_by(member_profile_id = data['member_profile_id']).all()
            final_balance_=payment_amount
            initial_amounts=0
            if data['initial_amount']=="" or None:
                initial_amounts=0
            else:
                initial_amounts=data['initial_amount']    

            balance=0
            new=0
            if savings:
                if savings[0].initial_amount:
                    initial_amounts=0
                    new=savings[-1].final_balance
            
            balance=final_balance_+initial_amounts+new    


            member_save = Member_Savings(
                member_profile_id = data['member_profile_id'],
                date=data['date'],
                initial_amount=initial_amounts,
                payment_amount=payment_amount,
                final_balance=balance,
                reference_no=reference_number()
                )

            if member_save:
                db.session.add(member_save)
                db.session.commit()
                return jsonify({"message":"Successfully added payment","status":True}),201
            else:
                return jsonify({"message":"something wrong in adding payment"}),404 

        elif 0>data['payment_amount']:
            print("dsds")
            total=Member_Savings.query.filter_by(member_profile_id = data['member_profile_id']).all()
            
            if (total[-1].final_balance-min_amount)>=abs(data['payment_amount']):# getting negative value and abs convert negative number to positive value
                total_amount=total[-1].final_balance+data['payment_amount']

                withdraw=Member_Savings(
                    member_profile_id=data['member_profile_id'],
                    date=data['date'],
                    payment_amount=data['payment_amount'],
                    final_balance = total_amount,
                    reference_no=reference_number()
                )

                if withdraw:
                    db.session.add(withdraw)
                    db.session.commit()
                    return jsonify({"data":"Successfully withdraw","status":True}),201
                else:
                    return jsonify({"data":"something went wrong in withdrawal","status":False}),400

            else:
                posible_amount=total[-1].final_balance-min_amount
                return jsonify({"message":f"you hove no money to withdrawal you can only withdraw {posible_amount}"}),406
        else:
            return jsonify({"message":"invalid payment"}),400        
 
    except Exception as e:
        return jsonify({"error":str(e)}),500





@app.route("/member_savings/<int:id>",methods=['DELETE'])
def delete_member_savings_by_id(id):
    try:
        member_savings=Member_Savings.query.filter_by(id=id).first()
        if member_savings:
            db.session.delete(member_savings)
            db.session.commit()
            return jsonify({"message":f"Successfully deleted id:{id} data","status":True}),202
        else:
            return jsonify({"message":"No data","status":False}),404    
    
    except Exception as e:
        return jsonify({"message":str(e)}),500  











@app.route("/member_savings_header/<int:id>",methods=["GET"])# we should pass the member id
def member_savings_header_by_id(id):
    try:
        member_profile=Member_Profile.query.filter_by(id=id).first()
        if member_profile:  
            member_savings=Member_Savings.query.filter_by(member_profile_id=member_profile.id).all()
            data=[]
            days_elapsed=0
            due=0
            total_amount=0
            if member_savings:

                todays=date.today()

                start_date=member_savings[-1].date

                savings_end_date = date(start_date.year,start_date.month,start_date.day)

                current_date = date(todays.year,todays.month,todays.day)

                days_elapsed=(current_date-savings_end_date).days
                

                week=(days_elapsed//7)+1

                total_amount=member_savings[-1].final_balance
                
            else:
                return jsonify({"message":"something went wrong in member savings "}),404         
            data.append(
                {
                    "week_elapsed":week,
                    "due":week,
                    "refer_id":member_profile.reference_no,
                    "member_name":member_profile.name,
                    "member_id":member_profile.id,
                    "total_amount":total_amount
                }
            )  
            if data:
                return jsonify({"data":data})
            else:
                return jsonify({"message":"No header data"}),404    
             
                    
        else:
            return jsonify({"message":"something went wrong in member profile "}),404            

    except Exception as e:
        return jsonify({"error_message":str(e)}),500

