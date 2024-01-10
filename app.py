from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id

#Use flask shell to access the database 

@app.route("/", methods=['POST','GET'])# this is for creating arguments in the db and should create new routes for deleting and shit
def index():
    if request.method=='POST':
        task_content=request.form['content']
        new_task=Todo(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks=Todo.query.order_by(Todo.date_created).all()#Going to look at all the contents of the database and retunr them in order 
        
        return render_template('update.html', tasks=tasks)
    
@app.route('/delete/<int:id>')#This is for the delete option and the int:id is used to identify which element to delete
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting the task'

@app.route('/index/<int:id>', methods=['GET','POST'])
def update(id):
    task_to_update=Todo.query.get_or_404(id)
    if request.method=='POST':
        task_to_update.content=request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating the task'
    else:
        return render_template('index.html',task=task_to_update)
    
if __name__=="__main__":
    app.run(debug="True")