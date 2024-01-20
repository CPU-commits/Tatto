# Responses
import fastapi
from fastapi.exceptions import HTTPException

status = fastapi.status
# Models
from app.models.category import Category
# Interfaces
from app.interfaces.category import Category as CategoryBody
#User types

#Services

class Categories():
    
    def get_categories(self) -> Category | None:
        return Category.objects()
    def get_by_id(self, id: str) -> Category | None:
        return Category.objects(id=id).first()
    def get_by_name(self, name: str) -> Category | None:
        return Category.objects(name=name).first()

    def create_category(self, category: CategoryBody) -> Category:
        inserted_category = Category(**category.to_model()).save()
        return inserted_category.id
       
    
        

categories_service = Categories()
