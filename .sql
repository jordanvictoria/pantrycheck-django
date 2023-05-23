DELETE FROM pantryapi_pantryuser WHERE id > 1

DELETE FROM auth_user WHERE id > 1

DELETE FROM authtoken_token WHERE user_id > 1
