import pytest
from your_module_name import Supermarket

@pytest.fixture
def supermarket():
    return Supermarket()

def test_supermarket_init(supermarket):
    assert supermarket.items == {}

def test_add_item_normal(supermarket):
    supermarket.add_item("Apple", 1.0, 10)
    assert "Apple" in supermarket.items
    assert supermarket.items["Apple"] == {"price": 1.0, "quantity": 10}

def test_add_item_zero_price_quantity(supermarket):
    supermarket.add_item("Milk", 0.0, 0)
    assert "Milk" in supermarket.items
    assert supermarket.items["Milk"] == {"price": 0.0, "quantity": 0}

def test_add_item_already_exists(supermarket):
    supermarket.add_item("Bread", 2.5, 5)
    with pytest.raises(ValueError, match="Item already exists"):
        supermarket.add_item("Bread", 3.0, 10)

def test_add_item_negative_price(supermarket):
    with pytest.raises(ValueError, match="Invalid price or quantity"):
        supermarket.add_item("Orange", -0.5, 12)

def test_add_item_negative_quantity(supermarket):
    with pytest.raises(ValueError, match="Invalid price or quantity"):
        supermarket.add_item("Banana", 0.75, -5)

def test_remove_item_normal(supermarket):
    supermarket.add_item("Cheese", 5.0, 2)
    supermarket.remove_item("Cheese")
    assert "Cheese" not in supermarket.items
    assert len(supermarket.items) == 0

def test_remove_item_non_existent(supermarket):
    with pytest.raises(KeyError, match="Item not found"):
        supermarket.remove_item("NonExistent")

def test_change_price_normal(supermarket):
    supermarket.add_item("Yogurt", 1.2, 8)
    supermarket.change_price("Yogurt", 1.5)
    assert supermarket.items["Yogurt"]["price"] == 1.5

def test_change_price_to_zero(supermarket):
    supermarket.add_item("Water", 1.0, 10)
    supermarket.change_price("Water", 0.0)
    assert supermarket.items["Water"]["price"] == 0.0

def test_change_price_non_existent(supermarket):
    with pytest.raises(KeyError, match="Item not found"):
        supermarket.change_price("Soda", 2.0)

def test_change_price_negative(supermarket):
    supermarket.add_item("Juice", 3.0, 4)
    with pytest.raises(ValueError, match="Invalid price"):
        supermarket.change_price("Juice", -1.0)

def test_change_quantity_normal(supermarket):
    supermarket.add_item("Cereal", 4.0, 3)
    supermarket.change_quantity("Cereal", 5)
    assert supermarket.items["Cereal"]["quantity"] == 5

def test_change_quantity_to_zero(supermarket):
    supermarket.add_item("Eggs", 2.0, 12)
    supermarket.change_quantity("Eggs", 0)
    assert supermarket.items["Eggs"]["quantity"] == 0

def test_change_quantity_non_existent(supermarket):
    with pytest.raises(KeyError, match="Item not found"):
        supermarket.change_quantity("Bread", 10)

def test_change_quantity_negative(supermarket):
    supermarket.add_item("Coffee", 6.0, 1)
    with pytest.raises(ValueError, match="Invalid quantity"):
        supermarket.change_quantity("Coffee", -2)

def test_get_item_normal(supermarket):
    supermarket.add_item("Pasta", 1.8, 7)
    item = supermarket.get_item("Pasta")
    assert item == {"price": 1.8, "quantity": 7}
    assert item is supermarket.items["Pasta"] # Should return a reference

def test_get_item_non_existent(supermarket):
    with pytest.raises(KeyError, match="Item not found"):
        supermarket.get_item("Rice")

def test_list_items_empty(supermarket):
    items = supermarket.list_items()
    assert items == {}
    assert isinstance(items, dict)

def test_list_items_with_items(supermarket):
    supermarket.add_item("Chocolate", 2.0, 10)
    supermarket.add_item("Candy", 0.5, 20)
    items = supermarket.list_items()
    assert items == {
        "Chocolate": {"price": 2.0, "quantity": 10},
        "Candy": {"price": 0.5, "quantity": 20}
    }
    assert isinstance(items, dict)

def test_list_items_is_copy(supermarket):
    supermarket.add_item("Tea", 3.0, 5)
    items_copy = supermarket.list_items()
    items_copy["Tea"]["price"] = 99.9
    assert supermarket.items["Tea"]["price"] == 3.0
    items_copy["NewItem"] = {"price": 1.0, "quantity": 1}
    assert "NewItem" not in supermarket.items