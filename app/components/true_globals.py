def insert_into_global_namespace(builtins, locals):
    for key, value in locals.items():
        if not key.startswith("__"):
            setattr(builtins, key, value)
