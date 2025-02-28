from sqlalchemy import Integer, String, LargeBinary
from sqlalchemy.dialects.postgresql import UUID


"""
## Table and Column Validation
"""

"""
- [ ] Confirm the presence of all required tables within the database schema.
"""


def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("users")


"""
- [ ] Validate the existence of expected columns in each table, ensuring correct data types.
"""


def test_model_structure_column_data_types(db_inspector):
    table = "users"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}
    # print(columns)
    assert isinstance(columns["id"]["type"], UUID)
    assert isinstance(columns["username"]["type"], String)
    assert isinstance(columns["hashed_password"]["type"], LargeBinary)


"""
- [ ] Ensure that column Foreign Keys are correctly defined.
"""
# def test_model_structure_foreign_keys(db_inspector):
#     table = "category"
#     foreign_keys = db_inspector.get_foreign_keys(table)
#     category_foreign_key = next(
#         (fk for fk in foreign_keys if set(fk["constrained_columns"])=={"parent"}),
#         None,
#     )
#     assert category_foreign_key is not None

"""
- [ ] Verify nullable or not nullable fields
"""


def test_model_structure_nullable_constraints(db_inspector):
    table = "users"
    # columns = db_inspector.get_columns(table)
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    # make list of columns and expected nullable values
    expected_nullables = {
        "id": False,
        "username": False,
        "hashed_password": False,
    }
    # check columns from the table match it.
    for key, value in expected_nullables.items():
        assert columns[key]["nullable"] is value


"""
- [ ] Test columns with specific constraints to ensure they are accurately defined.
"""


def test_model_structure_column_constraints(db_inspector):
    table = "users"
    constraints = db_inspector.get_check_constraints(table)

    assert any(
        constraint["name"] == "username_length_min_check" for constraint in constraints
    )
    assert any(
        constraint["name"] == "username_length_max_check" for constraint in constraints
    )


"""
- [ ] Verify the correctness of default values for relevant columns.
"""


# def test_model_structure_column_defaults(db_inspector):
#     table = "category"
#     columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}
#     assert columns["is_active"]["default"] == "false"
#     assert columns["level"]["default"] == "100"


"""
- [ ] Ensure that column lengths align with defined requirements.
"""


def test_model_structure_column_lengths(db_inspector):
    table = "users"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}
    assert columns["username"]["type"].length == 100


"""
- [ ]  Validate the enforcement of unique constraints for columns requiring unique values.
"""


def test_model_structure_unique_constraints(db_inspector):
    table = "users"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(
        constraint["name"] == "username_level_unique" for constraint in constraints
    )
