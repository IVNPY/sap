from django.db import models

class PermisosSistema(models.Model):
    class Meta:
        permissions = (
            ("crear_usuario", "Crear un nuevo usuario"),
            ("modificar_usuario", "Modificar un usuario"),
            ("eliminar_usuario", "Eliminar un usuario"),
            ("crear_rol_sistema", "Crear un nuevo rol de sistema"),
            ("modificar_rol_sistema", "Modificar un rol de sistema"),
            ("eliminar_rol_sistema", "Eliminar un rol de sistema"),
            ("asignar_rol_sistema", "Asignar roles de sistema a un usuario"),
        )

class PermisosProyecto(models.Model):
    class Meta:
        permissions = (
            ("asignar_rol_proyecto", "Asignar roles de proyecto a un usuario"),
        )

