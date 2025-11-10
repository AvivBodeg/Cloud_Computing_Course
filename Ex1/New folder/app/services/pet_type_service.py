# Service for managing pet-type business logic and in-memory storage
#
# Responsibilities:
# - In-memory storage for pet-types (dict: id -> PetType)
# - ID generation for new pet-types
# - Business validation (duplicate checking, etc.)
# - Orchestrate NinjaAPI calls with storage operations
# - Handle mapping between PetTypeInfo DTO and PetType domain model