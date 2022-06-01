from Settings import *
from Api.Auth.Models import *



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.args.get('token')
            if 'access_token' in request.headers:
                token = request.headers['access_token']
            if not token:
                return jsonify({'message':'Token is missing!'}),401
            
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = App_Users.query.filter_by(id=data['id']).first()
            except:
                 return jsonify({
                'message':'Token is invalid'
                }),401
            
        except:
            return jsonify({
                'message':'Token is invalid'
            }),401
        
        return f(current_user,*args, **kwargs)
    return decorated


