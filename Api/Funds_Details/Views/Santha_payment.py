from Settings import *
from Api.Funds_Details.Models import *
from Api.Teams_Details.Models import *





@app.route('/santha_details/<int:page>/<int:per_page>',methods=['GET'])
def get_santha_details(page,per_page):
    try:
        data=[]
        member=Member_Profile.query.all()
        
        for i in member:
            if i:
                terms=0
                day_elapsed=0
                due_amount=0
                received_amount=0
                is_due="No"
                total_amount_received=0
                total_due_amount=0

                today=datetime.today()
                join_date=i.join_date
                terms=today.year - join_date.year-((today.month, today.day) < (join_date.month, join_date.day))
                santha_payment=Santha_Payment.query.filter_by(member_profile_id=i.id).all()
                for j in santha_payment:
                    last_santha_year=date(j.santha_for_year,join_date.month,join_date.day)
                    current_santha_year=date(today.year,today.month,today.day)
                    received_amount+=j.santha_amount_received
                    day_elapsed=(current_santha_year-last_santha_year).days

                due_amount=((terms+1)*i.santha_amount)-received_amount
                if ((terms+1)*i.santha_amount)==received_amount:
                    is_due="No"
                    day_elapsed=0
                elif ((terms+1)*i.santha_amount)>received_amount:
                    is_due="Yes"
                else:
                    is_due="No"
                    day_elapsed=0 
                    amount_balance=received_amount-((terms+1)*i.santha_amount)
                    due_amount=0
                   
            data.append(
                    {
                        "reference_no":i.reference_no,
                        "member_name":i.name,
                        "member_profile_id":i.id,
                        "join_date":str(i.join_date),
                        "santha_amount":float(i.santha_amount*(terms+1)),
                        "terms":terms+1,
                        "day_elapsed":day_elapsed,
                        "due_amount":float(due_amount),
                        "received_amount":received_amount,
                        "is_due":is_due
                    }
                )
        if data:
            for k in data:
                total_amount_received+=k['received_amount']
                total_due_amount+=k['due_amount']
            pag=get_rows(data,per_page)
            if pag:
                return jsonify(data=pag[page-1],total_amount=total_amount_received,total_due_amount=total_due_amount),200     
            else:
                return jsonify(message="Something wrong in pagination details"),404     
        else:
            return jsonify(message="No data in santha details"),404
       
    except Exception as e:
        return jsonify({"message":str(e)}),500






@app.route("/santha_payment/<int:id>/<int:page>/<int:per_page>",methods=['GET'])
def get_santha_payment_by_member_id(id,page,per_page):
    try:
        santha_payment=Santha_Payment.query.filter_by(member_profile_id=id).order_by(Santha_Payment.created_on.desc()).paginate(page=page,per_page=per_page,error_out=False)
        santha_payment_count=Santha_Payment.query.filter_by(member_profile_id=id).count()
        if santha_payment:
            return jsonify({"data":[Santha_Payment.santha_payment_json(i) for i in santha_payment.items],"total_count":santha_payment_count}),200
        else:
            return jsonify({"message":"No santha data","status":False}),404    
    
    except Exception as e:
        return jsonify({"message":str(e)}),500   



@app.route("/santha_payment",methods=['POST'])
def add_santha_payment():
    try:
        data=request.get_json()
        if data:

            member_profile=Member_Profile.query.filter_by(id=data['member_profile_id']).first()
            if not member_profile:
                return jsonify({"message":"Member details not found"}),404
            
            santha_payment=Santha_Payment(
                member_profile_id=data['member_profile_id'],
                santha_for_year=data['santha_for_year'],
                annual_contribution=0 if data['annual_contribution']=="" or None else data['annual_contribution'],
                santha_amount_received=data['santha_amount_received'],
                received_date=datetime.today().date(),
                reference_no=reference_number()
            )

            if santha_payment:
                db.session.add(santha_payment)
                db.session.commit()
                return jsonify({"message":"Successfully added new data"}),201
            else:
                return jsonify({"message":"something wrong into santha payment data","status":False}),400    
        else:
             return jsonify({"message":"something went wrong in sending data","status":False}),400  
    except Exception as e:
        return jsonify({"message":str(e)}),500







@app.route("/santha_payment/<int:id>",methods=['DELETE'])
def delete_santha_payment_by_id(id):
    try:
        santha_payment=Santha_Payment.query.filter_by(id=id).first()
        if santha_payment:
            db.session.delete(santha_payment)
            db.session.commit()
            return jsonify({"message":f"Successfully deleted id {id} data","status":True}),202
        else:
            return jsonify({"message":"No santha data","status":False}),404    
    
    except Exception as e:
        return jsonify({"message":str(e)}),500   