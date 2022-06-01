from Settings import *
from Api.Auth.Models import *




@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        if not data or not data['email']:
            return jsonify(message="Enter valid email id"),404

        if not data['password']:
            return jsonify(message="Enter valid password"),401


        filter_user = App_Users.query.filter_by(email=data.get("email")).first()
        if filter_user:
            if check_password_hash(filter_user.encrypted_password,data.get("password")):
                db.session.commit()
                token = jwt.encode({
                    'id':filter_user.id,
                    'exp':datetime.utcnow() + timedelta(minutes=180)
                }, app.config['SECRET_KEY'])
               
                return jsonify({
                    "token":token,
                    "user_name":filter_user.name,
                    "user_id":filter_user.id,
                    "message":"login success"
                }),200
            else:
                return jsonify({"message":"Invalid password enter valid password"}),401  
        else:
            return jsonify({
                "message":"login failed check your email"
            }),404   
    
    except Exception as e:
        return jsonify({"message":str(e)}),500
