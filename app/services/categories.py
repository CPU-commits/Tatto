# Responses
import fastapi
import json

status = fastapi.status
# Models
from app.models.category import Category
# Interfaces
from app.interfaces.category import Category as CategoryBody
#User types

#Services

class Categories():
    def get_categories(self) -> list[Category] | None:
        return json.loads(Category.objects(state=True).to_json())

    def get_by_id(self, id: str) -> Category | None:
        return Category.objects(id=id).first()

    def get_by_slug(self, slug: str) -> Category | None:
        return Category.objects(slug=slug).first()

    def create_category(self, category: CategoryBody) -> Category:
        inserted_category = Category(**category.to_model()).save()
        return inserted_category.id   

categories_service = Categories()
