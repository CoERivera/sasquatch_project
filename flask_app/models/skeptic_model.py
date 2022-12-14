# Import function to return an instance of the database connection
from flask import flash
from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model, sighting_model

# Modeling the class after the skeptics table
class Skeptic:
    def __init__(self, data):
        self.id = data['id']
        self.sighting_id = data['sighting_id']
        self.sighter_id = data['sighter_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Create class methods for queries
    
    # Obtains all the skeptics
    @classmethod
    def get_all_sightings(cls):
        query = "SELECT * FROM sightings;"
        
        # Call the connectToMySQL function to connect to the database
        results = connectToMySQL(DATABASE).query_db(query)
        
        if results:
            # Create empty list to store all the instances
            sightings = []

            # Iterating through all the results to store sighting
            for sighting in results:
                sightings.append(cls(sighting))
            
            return sightings
        
        return False

    # Save a new skeptic
    @classmethod
    def save_skeptic(cls,data):
        query = """
            INSERT INTO skeptics(sighting_id,sighter_id)
            VALUES (%(sighting_id)s,%(sighter_id)s);
        """
        # data dictionary will pass will be passed onto saved method from server.py

        return connectToMySQL(DATABASE).query_db(query,data)

    # Obtains all the skeptics for a specific sighting 
    @classmethod
    def get_all_skeptics_by_sighting(cls,id):
        query = """SELECT * FROM skeptics 
            JOIN users ON sighter_id = users.id
            WHERE sighting_id = %(sighting_id)s;"""

        data = {'sighting_id':id}

        results = connectToMySQL(DATABASE).query_db(query,data)
        skeptics = []
        
        if results:
            for skeptic in results:
                one_skeptic = cls(skeptic)
                skeptic_data = {
                    **skeptic,
                    'id': skeptic['users.id'],
                    "created_at": skeptic['users.created_at'],
                    "updated_at": skeptic['users.updated_at']
                }
                one_skeptic.skeptical = user_model.User(skeptic_data) 
                skeptics.append(one_skeptic)
        
        return skeptics


    @classmethod
    def remove_skeptic(cls,data):
        query = """DELETE FROM skeptics 
            WHERE sighting_id = %(sighting_id)s
            AND sighter_id = %(sighter_id)s;"""

        connectToMySQL(DATABASE).query_db(query,data)