from Settings import *
from Api.Teams_Details.Models import *






@app.route("/leader_list",methods=['GET'])
def get_leader_list():
    try:
        member=Member_Profile.query.filter_by(status=0).filter_by(is_leader=1).all()
        if member:
            return jsonify({"data":[Member_Profile.leader_list_json(i) for i in member],"status":True}),200
        else:
            return jsonify({"message":"No data","status":False}),404    
    
    except Exception as e:
        return jsonify({"message":str(e)}),500   





@app.route("/leader/<int:page>/<int:per_page>",methods=['GET'])
def get_leader(page,per_page):
    try:
       
        leader=Member_Profile.query.filter_by(status=0).filter_by(is_leader=1).paginate(page=page,per_page=per_page,error_out=False)
        leader_count=Member_Profile.query.filter_by(is_leader=1).filter_by(status=0).count()
        if leader:
            return jsonify({"data":[Member_Profile.lead_json(i) for i in reversed(leader.items)],"status":True,"total_count":leader_count}),200
        else:
            return jsonify({"message":"No data","status":False}),404    
       
    except Exception as e:
        return jsonify({"message":str(e)}),500   



