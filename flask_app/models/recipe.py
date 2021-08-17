from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe
from flask import flash
DATABASE = 'users_recipes'

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.under_30 = data['under_30']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.description = data['description']
        self.name = data['name']
        self.user_id = data['user_id']
        self.date_made = data['date_made']
      
   
    @classmethod
    def create(cls,data):
        query ="INSERT INTO recipes (name, description, instructions, created_at, updated_at, under_30, user_id, date_made) VALUES (%(name)s, %(description)s, %(instructions)s, NOW(), NOW(), %(under_30)s, %(user_id)s, %(date_made)s);"
        return connectToMySQL(DATABASE).query_db(query,data)
        
    
    @classmethod
    def getOneById(cls, id):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        data = {'id':id}
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def edit(cls,data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30 = %(under_30)s, updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def delete(cls,id):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        data = {'id':id}
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True 
   
        if len(recipe['name']) < 3:
            flash("* Name must be at least 3 characters", "name")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("* Description must be at least 3 characters", "description")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("* Instruction must be at least 3 characters", "instructions")
            is_valid = False
        if recipe["date_made"] == "":
            flash("* Please fill in the date", "date_made")
            is_valid = False
        if is_valid:
            flash("* Recipe created successfully.")
        return is_valid