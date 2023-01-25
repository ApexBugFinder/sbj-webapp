from decouple import config

sqluri = 'postgresql://' + config('DB_USER') + ':'+config(
    'DB_PASSWORD')+'@'+config('DB_HOST')+'/'+config('DB_NAME')
print(sqluri)
