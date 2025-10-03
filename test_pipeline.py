from animal_etl.transformers import batch_animals, transform_animal, transform_friends, transform_timestamp


def test_transform_friends():
    assert transform_friends("Hyena,Hamster,Quail,Cod") == ["Hyena", "Hamster", "Quail", "Cod"]
    assert transform_friends("") == []
    assert transform_friends("   ") == []
    assert transform_friends(" Hyena , Hamster  , Quail ") == ["Hyena", "Hamster", "Quail"]


def test_transform_timestamp():
    result = transform_timestamp(990876974457)
    assert result is not None
    assert "2001-05-26" in result

    result = transform_timestamp(990876974)
    assert result is not None
    assert "1970-01-12" in result


def test_transform_animal():
    animal = {"id": 30, "name": "Mole", "born_at": 990876974457, "friends": "Hyena,Hamster"}
    result = transform_animal(animal)

    assert result["id"] == 30
    assert result["name"] == "Mole"
    assert result["friends"] == ["Hyena", "Hamster"]
    assert "born_at" in result

    animal_no_date = {"id": 1, "name": "Test", "friends": ""}
    result = transform_animal(animal_no_date)
    assert "born_at" not in result
    assert result["friends"] == []


def test_batch_animals():
    animals = [{"id": i} for i in range(5)]
    batches = batch_animals(animals, batch_size=2)

    assert len(batches) == 3
    assert len(batches[0]) == 2
    assert len(batches[2]) == 1
