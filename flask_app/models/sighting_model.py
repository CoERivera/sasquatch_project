# Import function to return an instance of the database connection
from flask import flash
from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model, skeptic_model

# Modeling the class after the sightings table
class Sighting:
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.date = data['date']
        self.sighted = data['sighted']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sighter_id = data['sighter_id']
        self.skeptical = []
    # Create class methods for queries
    
    # Obtains all the sightings
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

    # Save a new sighting
    @classmethod
    def save_sighting(cls,data):
        query = """
            INSERT INTO sightings(location,description,date,sighted,sighter_id)
            VALUES (%(location)s,%(description)s,%(date)s,%(sighted)s,%(sighter_id)s);
        """
        # data dictionary will pass will be passed onto saved method from server.py

        return connectToMySQL(DATABASE).query_db(query,data)

    # Obtains a specific sighting
    @classmethod
    def get_one_sighting_with_user(cls,id):
        query = """SELECT * FROM sightings
                JOIN users ON sightings.sighter_id = users.id
                WHERE sightings.id = %(id)s;"""
        data = {'id': id}
        # Call the connectToMySQL function to connect to the database
        results = connectToMySQL(DATABASE).query_db(query,data)
        
        
        sighting = cls(results[0])
        sighter_data = {
                **results[0],
                'id': results[0]['users.id'],
                'created_at': results[0]['users.created_at'],
                'updated_at': results[0]['users.updated_at'],
            }
        sighting.sighter = user_model.User(sighter_data)
        sighting.skeptics = skeptic_model.Skeptic.get_all_skeptics_by_sighting(id)
        
        return sighting
    
    # Obtains all the sightings and their users
    @classmethod
    def get_all_sightings_with_users(cls):
        query = """SELECT * FROM sightings
                    JOIN users ON sightings.sighter_id = users.id"""
        
        # Call the connectToMySQL function to connect to the database
        results = connectToMySQL(DATABASE).query_db(query)
        # Create empty list to store all the instances
        sightings = []

        if results:
            # Iterating through all the results to store user along
            # with sighting information for each user
            for sighting in results:
                one_sighting = cls(sighting)              
                sighter_data = {
                    **sighting,
                    'id': sighting['users.id'],
                    'created_at': sighting['users.created_at'],
                    'updated_at': sighting['users.updated_at'],
                }
                one_sighting.sighter = user_model.User(sighter_data)
                one_sighting.skeptics = skeptic_model.Skeptic.get_all_skeptics_by_sighting(one_sighting.id)
                sightings.append(one_sighting)

        print(sightings)
        return sightings

    # Updates sighting info
    @classmethod
    def update_sighting(cls,data):
        query = """UPDATE sightings
                    SET location = %(location)s,
                        description = %(description)s,
                        date = %(date)s,
                        sighted = %(sighted)s,
                        updated_at = NOW()
                    WHERE id = %(id)s;"""
        
        # Call the connectToMySQL function to connect to the database
        connectToMySQL(DATABASE).query_db(query,data)

    # Removes sighting
    @classmethod
    def remove_sighting(cls,id):
        query = """DELETE FROM sightings
                    WHERE id = %(id)s;"""
        data = {'id': id}
        # Call the connectToMySQL function to connect to the database
        connectToMySQL(DATABASE).query_db(query,data)

    
    # Validates sighting information to register it
    @staticmethod
    def validate_sighting(sighting):
        is_valid = True
        
        # Verifies mininum sighting location length
        if len(sighting['location']) < 1:
            flash('Sighting location must not be empty.','location')
            is_valid = False

        # Verifies description isn't empty
        if len(sighting['description']) < 1:
            flash('Sighting description field must not be empty.','description')
            is_valid = False
        
        # Verifies date isn't empty
        if len(sighting['date']) < 10:
            flash('Must provide a valid date.','date')
            is_valid = False

        # Verifies number of sasquatches aren't empty
        if 'sighted' not in sighting or int(sighting['sighted']) < 1:
            flash('Must select a minimum amount of sasquatches sighted.','sighted')
            is_valid = False

        # If no conditionals triggered, returns true
        return is_valid