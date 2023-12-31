from django.db import models

def get_model_fields (model:models.Model, related_fields:bool=False, get_id:bool=False) -> list:
    """ Get model fields except relations and _state, id, last_update, created
    
    Args:
        model (models.Model): Model to get fields
        related_fields (bool, optional): Get related fields. Defaults to False.
        get_id (bool, optional): Get id field. Defaults to False.
    
    Returns:
        list: List of model fields 
    """
    
    fields = model._meta.get_fields()
        
    # Filter only model fields
    if not related_fields:
        fields = list(filter(lambda row: not row.is_relation, fields))
    
    # Remove extra fields
    extra_fields = ["_state", "id", "last_update", "created"]
    if get_id:
        extra_fields.remove("id")
    fields = list(filter(lambda row: row.name not in extra_fields, fields))
            
    return fields