from django.db import models

def get_model_fields (model:models.Model) -> list:
    """ Get model fields except relations and _state, id, last_update, created
    
    Args:
        model (models.Model): Model to get fields
    
    Returns:
        list: List of model fields 
    """
    
    fields = model._meta.get_fields()
    
    # Filter only model fields
    fields = list(filter(lambda row: not row.is_relation, fields))

    # Remove extra fields
    extra_fields = ["_state", "id", "last_update", "created"]
    fields = list(filter(lambda row: row.name not in extra_fields, fields))
    
    return fields