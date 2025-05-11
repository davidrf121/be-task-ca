1. **Why can we not easily split this project into two microservices?**

    The User and Item modules are tightly coupled due to multiple interdependencies:
    - The User entity depends on the Item entity through the CartItem relationship.
    - CartItem enforces a foreign key constraint to the Item table.
    - The User use case function add_item_to_cart imports directly from the Item module.

2. **Why does this project not adhere to the clean architecture even though we have seperate modules for api, repositories, usecases and the model?**
    
    The use case functions accept a database session object (Session), which directly ties them to SQLAlchemy.
    To align with clean architecture, the core layers (use cases and entities) should depend only on interfaces or abstractions—not on specific implementations like SQLAlchemy.


3. **What would be your plan to refactor the project to stick to the clean architecture?**
    
    - Implement a repository interface.
    - Implement this interface using an in-memory database, as specified in the requirements.
    - Refactor the usecase functions to accept an instance of this newly created interface.


4. **How can you make dependencies between modules more explicit?**

    Using absolute imports instead of relative imports.
