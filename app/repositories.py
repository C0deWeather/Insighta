from uuid import UUID
from typing import List, Optional
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
        query = (
            "INSERT INTO profiles "
            "(id, name, gender, gender_probability, age, age_group, "
            "country_id, country_name, country_probability, created_at) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
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
    
    async def get_by_filter(
        self,
        gender: Optional[str] = None,
        age_group: Optional[str] = None,
        country_id: Optional[str] = None,
        min_age: Optional[int] = None,
        max_age: Optional[int] = None,
        min_gender_probability: Optional[float] = None,
        min_country_probability: Optional[float] = None,
        sort_by: str = "created_at",
        order: str = "desc",
    ) -> List[dict]:
        """
        Get profiles filtered by specified criteria.
        
        Args:
            gender: Filter by gender
            age_group: Filter by age group
            country_id: Filter by country ID
            min_age: Minimum age filter
            max_age: Maximum age filter
            min_gender_probability: Minimum gender probability threshold
            min_country_probability: Minimum country probability threshold
            sort_by: Field to sort by (age, created_at, gender_probability)
            order: Sort order (asc, desc)
            
        Returns:
            List of profile dictionaries matching the filters
        """
        conditions = []
        params = []
        
        if gender is not None:
            conditions.append("gender = %s")
            params.append(gender)
        
        if age_group is not None:
            conditions.append("age_group = %s")
            params.append(age_group)
        
        if country_id is not None:
            conditions.append("country_id = %s")
            params.append(country_id)
        
        if min_age is not None:
            conditions.append("age >= %s")
            params.append(min_age)
        
        if max_age is not None:
            conditions.append("age <= %s")
            params.append(max_age)
        
        if min_gender_probability is not None:
            conditions.append("gender_probability >= %s")
            params.append(min_gender_probability)
        
        if min_country_probability is not None:
            conditions.append("country_probability >= %s")
            params.append(min_country_probability)
        
        # Build the query
        query = "SELECT * FROM profiles"
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        # Validate and add sorting
        valid_sort_fields = {"age", "created_at", "gender_probability"}
        if sort_by not in valid_sort_fields:
            sort_by = "created_at"
        
        valid_orders = {"asc", "desc"}
        if order.lower() not in valid_orders:
            order = "desc"
        
        query += f" ORDER BY {sort_by} {order.upper()}"
        
        results = await self.db.fetch_all(query, tuple(params))
        return results
