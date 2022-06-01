from Settings import *



class Master_Data(db.Model):
    __tablename__="master_data"
    id=db.Column(db.Integer(),primary_key=True)
    property=db.Column(db.String(191),nullable=True)
    value=db.Column(db.String(500),nullable=True)
    created_on=db.Column(db.DateTime(timezone=True),nullable=True,server_default=func.now())
        
    
    def __repr__(self):
        return f"<Master_data>:{self.id}"     