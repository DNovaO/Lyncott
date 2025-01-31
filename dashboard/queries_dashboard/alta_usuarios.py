# from django.contrib.auth.models import User
# from django.db import transaction, connection

# def importar_usuarios():
#     try:
#         # Inicia una transacción
#         with transaction.atomic():
#             # Consultar todos los usuarios de la tabla MENU_CVE
#             with connection.cursor() as cursor:
#                 cursor.execute("SELECT c1, c2, c3 FROM MENU_CVE")  # Consultar todos los usuarios
#                 usuarios = cursor.fetchall()
            
#             # Iterar sobre los usuarios obtenidos de MENU_CVE
#             for c1, c2, c3 in usuarios:
#                 # Verificar si el usuario ya existe en la tabla auth_user
#                 if User.objects.filter(username=c1).exists():
#                     print(f'El usuario {c1} ya existe, omitiendo...')
#                     continue  # Si el usuario ya existe, lo omitimos y pasamos al siguiente
                
#                 # Crear un nuevo usuario en Django con los valores de c1, c2, y c3
#                 user = User.objects.create_user(username=c1, password=c2)
                
#                 # Asignar el primer nombre (o cualquier otro campo que se corresponda con c3)
#                 user.first_name = c3
                
#                 # Aquí puedes asignar más campos si es necesario
#                 user.last_name = ""  # Si tienes un campo para 'last_name', puedes asignarlo aquí
#                 user.email = ""  # Si tienes un campo para 'email', puedes asignarlo aquí
                
#                 # Guardar el usuario creado
#                 user.save()
                
#                 print(f'Usuario {c1} creado con éxito.')

#             # Consulta de la tabla auth_user para ver los usuarios insertados
#             with connection.cursor() as cursor:
#                 cursor.execute("SELECT id, username, first_name, last_name, email FROM auth_user")
#                 usuarios_auth = cursor.fetchall()
#                 print("\nUsuarios en auth_user después de la inserción:")
#                 for user in usuarios_auth:
#                     print(user)

#     except Exception as e:
#         # Si ocurre un error, la transacción se deshace automáticamente
#         print(f'Ocurrió un error: {e}')

# # Ejecutar la función para importar los usuarios
# importar_usuarios()
