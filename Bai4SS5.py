from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "stock": 5}
]
class InforProduct(BaseModel):
    code: str
    name: str
    price: int = Field(gt=0)
    stock: int = Field(ge=0)
app = FastAPI()
@app.get("/products")
def get_products():
    return {
        "message": "List Product",
        "data": products
    }
@app.put("/products/{product_id}", status_code=status.HTTP_200_OK)
def update_product(product_id: int, product: InforProduct):
    check_id = next((pro for pro in products if pro["id"] == product_id),None)
    if not check_id:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    else:
        check_code = next((pro["code"] for pro in products if pro["code"] == product.code.upper()),None)
        if check_code:
            raise HTTPException(
                status_code=409,
                detail="Product code already exists"
            )
        else:
            check_id.update(product.dict())
            return {
                "message": "Update successful."
            }

