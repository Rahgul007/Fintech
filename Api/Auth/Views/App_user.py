from operator import and_
from Settings import *
from Api.Auth.Models import *







@app.route("/app_user/<int:page>/<int:per_page>",methods=['GET'])
def get_app_user(page,per_page):
    try:
        app_user=App_Users.query.filter_by(status=0).paginate(page=page,per_page=per_page,error_out=False)
        if app_user:
            app_user_count=App_Users.query.filter(App_Users.status==0).count()
            return jsonify({
                "data":[App_Users.json(i) for i in reversed(app_user.items)],
                "total_count":app_user_count
                }),200
        else:
            return jsonify({"data":{},"message":"No data","status":False}),404    
       
    except Exception as e:
        return jsonify({"message":str(e)}),500   




@app.route("/app_user/<int:id>",methods=['GET'])
def get_app_user_by_id(id):
    try:
        
        app_user=App_Users.query.filter_by(id=id).first()
        if app_user:
            return jsonify({"data":App_Users.json(app_user),"status":True}),200
        else:
            return jsonify({"message":"No data","status":False}),404    
         
    except Exception as e:
        return jsonify({"message":str(e)}),500   




@app.route("/app_user",methods=['POST'])
def add_app_user():
    try:
        data=request.get_json()
        if data:

            user_validation=App_Users.query.all()
            if user_validation:
                for i in user_validation:
                    if i.user_name==data['user_name']:
                        return jsonify(message="Username is already exist try another user name"),406  
                    if i.email==data['email']:
                        return jsonify(message="Email is already exist try another email"),406
                    if i.mobile==data['mobile_no']:
                        return jsonify(message="Mobile number is already exist try another mobile number"),406


            app_user=App_Users(
                name=data['name'],
                role_id=data['role_id'],
                user_name=data['user_name'],
                image_path=data['image_path'],
                encrypted_password=generate_password_hash(data['encrypted_password']),
                email=data['email'],
                mobile=data['mobile_no'],
                reference_no=reference_number()
            )
            if app_user:
                db.session.add(app_user)
                db.session.commit()
                return jsonify({"data":App_Users.json(app_user),"status":True,"message":"Successfully added new data"}),201
            else:
                return jsonify({"message":"something wrong into master data","status":False}),400    
        else:
             return jsonify({"message":"something went wrong in sending data","status":False}),400  
    except Exception as e:
        return jsonify({"message":str(e)}),500




@app.route("/app_user/<int:id>",methods=['PUT'])
def update_app_user(id):
    try:
        data=request.get_json()
        if data: 
            app_user=App_Users.query.filter_by(id=id).first()
            if app_user:

                app=App_Users.query.all()
                if app:
                    for i in app:
                        if i.id!=app_user.id:
                            if i.mobile==data['mobile_no']:
                                return jsonify(message="Mobile number is already exist try another"),406
                            if i.user_name==data['user_name']:
                                return jsonify(message="user name is already exist try another"),406
                            if i.email==data['email']:
                                return jsonify(message="email is already exist try another"),406


                if not check_password_hash(app_user.encrypted_password,data['old_password']):
                    return jsonify({"message":"Old password is not matched"}),406

                if check_password_hash(app_user.encrypted_password,data['new_password']):
                    return jsonify({"message":"This password matched old password please enter new password"}),406

               

                app_user.name=data['name']
                app_user.role_id=data['role_id']
                app_user.user_name=data['user_name']
                app_user.image_path=data['image_path']
                app_user.encrypted_password=generate_password_hash(data['new_password'])
                app_user.email=data['email']
                app_user.mobile=data['mobile_no']
                
                db.session.commit()
               
                return jsonify({"data":App_Users.json(app_user),"message":"Successfully updated data"}),202
            else:
                return jsonify({"message":f"please check app user id {id}"}),400     
        else:
             return jsonify({"message":"something went wrong in sending data","status":False}),400  
    except Exception as e:
        return jsonify({"message":str(e)}),500 





@app.route("/app_user/<int:id>",methods=['DELETE'])
def delete_app_user_by_id(id):
    try:
        app_user=App_Users.query.filter_by(id=id).first()
        if app_user:
            db.session.delete(app_user)
            db.session.commit()
            return jsonify({"message":f"Successfully deleted id:{id} data","status":True}),202
        else:
            return jsonify({"message":"No data","status":False}),400    
    
    except Exception as e:
        return jsonify({"message":str(e)}),500 