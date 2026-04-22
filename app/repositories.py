from uuid import UUID
from app.db import Database
from app.schemas import Profile


class ProfileRepo:
    """Repository for profile database operations."""
    
    def __init__(self, db: Database):
        """Initialize the profile repository with a database instance."""
        self.db = db
    
    async def create_profile(self, profile: Profile) -> UUID:
        """
        Create a new profile in the database.
        
        Args:
            profile: The Profile model instance to create
            
        Returns:
            The ID of the created profile
        """
        query = "INSERT INTO profiles (id, name, gender, gender_probability, age, age_group, country_id, country_name, country_probability, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        await self.db.insert(query, (
            profile.id,
            profile.name,
            profile.gender,
            profile.gender_probability,
            profile.age,
            profile.age_group,
            profile.country_id,
            profile.country_name,
            profile.country_probability,
            profile.created_at,
        ))
        return profile.id
