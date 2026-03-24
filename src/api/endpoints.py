PET = "/pet"
STORE = "/store"
STORE_ORDER = f"{STORE}/order"


def pet_by_id(pet_id: int) -> str:
    return f"{PET}/{pet_id}"


def order_by_id(order_id: int) -> str:
    return f"{STORE_ORDER}/{order_id}"


def find_by_status(status: str) -> str:
    return f"{PET}/findByStatus?status={status}"
