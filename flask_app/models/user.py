from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PW_REGEX = re.compile(r"^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$")
DATABASE = "users_recipes"
from flask_app.models import recipe

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []
 
    @classmethod
    def create(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , password, created_at, updated_at ) VALUES ( %(fname)s , %(lname)s , %(email)s ,%(password)s, NOW() , NOW() );"
        return connectToMySQL(DATABASE).query_db( query, data )
    
    @classmethod
    def get_user_with_recipes( cls , data ):
        query = "SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db( query , data )
        print(results)
        user = cls( results[0] )
        for row_from_db in results:
            recipe_data = {
                "id" : row_from_db["recipes.id"],
                "under_30" : row_from_db["under_30"],
                "instructions" : row_from_db["instructions"],
                "created_at" : row_from_db["recipes.created_at"],
                "updated_at" : row_from_db["recipes.updated_at"],
                "description" : row_from_db["description"],
                "name" : row_from_db["name"],
                "date_made" : row_from_db["date_made"],
                "user_id":row_from_db["user_id"]
            }
            user.recipes.append(recipe.Recipe( recipe_data ) ) 
        return user
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        print(results)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def getOneById(cls,id):
        query = "SELECT * FROM users WHERE id = %(id)s"
        data = {'id':id}
        results = connectToMySQL(DATABASE).query_db(query,data)
        return cls(results[0])
    
    @staticmethod
    def validate_user(user):
        is_valid = True 
   
        if len(user["email"]) == 0:
            flash("* Email cannot be empty", "email")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("* Invalid email format. Should meet username@emaildomain.com", "email")
            is_valid = False  
        if User.get_by_email(user):
            flash('* Email already in database', "email")
            is_valid = False
        if len(user['fname']) < 2 or not user['fname'].isalpha():
            flash("* First name must be at least 2 characters and only letters", "first_name")
            is_valid = False
        if len(user['lname']) < 2 or not user['lname'].isalpha():
            flash("* Last name must be at least 2 characters and only letters", "last_name")
            is_valid = False
        if not PW_REGEX.match(user['password']): 
            flash("* Password should be at least 8 characters with one uppercase and one number no special characters", "password")
            is_valid = False
        if user['password'] != user["cpassword"]:
            flash("* Both passwords don't match", "password")
            is_valid = False
        if is_valid:
            flash("* Registration was successful")
        return is_valid
    
   