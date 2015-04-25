#encoding:utf-8
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from django.db.models import Max
from django.utils.datetime_safe import datetime


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
            ("crear_user_story_proyecto", "Crear un user story del proyecto"),
            ("modificar_user_story_proyecto", "Modificar un user story del proyecto"),
            ("eliminar_user_story_proyecto", "Eliminar un user story del proyecto"),
        )

PRIORIDAD = (
    ('ALTA', 'ALTA'),
    ('MEDIA', 'MEDIA'),
    ('BAJA', 'BAJA'),
)

FASES_ESTADOS = (
    ('ABIERTA', 'ABIERTA'),
    ('FINALIZADA', 'FINALIZADA'),
    ('NO-INICIADA', 'NO-INICIADA'),
)

PROYECTOS_ESTADOS = (
    ('NO-INICIADO', 'NO-INICIADO'),
    ('INICIADO', 'INICIADO'),
    ('FINALIZADO', 'FINALIZADO'),
)


FLUJOS_ESTADOS = (
    ('ABIERTO', 'ABIERTO'),
    ('FINALIZADO', 'FINALIZADO'),
    ('NO-INICIADO', 'NO-INICIADO'),
)


#funcion para validar las fecha de fin de los proyectos recibe una fecha
def validate_even(value):
    if value < datetime.now().date():
        raise ValidationError('%s No es una fecha valida' % value)

#Nuevos campos en el usuario


#User.add_to_class('domicilio', models.CharField(max_length=200))

#User.add_to_class('fechaNac', models.DateField())

#User.add_to_class('telefono', models.PositiveIntegerField(null=True,blank=True))

#User.add_to_class('rol', models.ForeignKey(Rol, related_name='nombre'))

#User.add_to_class('cliente', models.BooleanField(blank=True))






class UserStory(models.Model):
    id_userStory = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=200)
    descripcion= models.CharField(max_length=10000)
    detalle = models.CharField(max_length=1000)
    #sprint = models.ForeignKey(Sprint)
    valNegocio = models.CharField(max_length=100)
    valTecnico = models.CharField(max_length=100)
    usuario = models.OneToOneField(User)
    prioridad = models.CharField(max_length=5,choices=PRIORIDAD)
    horasAcumuladas = models.IntegerField(blank=False)
    estimacion = models.IntegerField(blank=False)
    #flujo = models.ForeignKey(Flujo)

    def __unicode__(self):
        return self.nombre



    class Meta:
        app_label = 'adm'



class Sprint(models.Model):
    id_sprint = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    orden = models.CharField(max_length=200)


    def __unicode__(self):
        return self.nombre


    class Meta:
        app_label = 'adm'

class Proyecto(models.Model):
    idproyecto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=200)
    #costo_temporal = models.IntegerField(default=0)
    #costo_monetario = models.IntegerField(default=0)
    estado = models.CharField(max_length=11, choices=PROYECTOS_ESTADOS, default='NO-INICIADO')
    #numero_flujos = models.IntegerField(blank=False)
    #cambiar despues para que sea la fecha actual al crear
    fecha_inicio = models.DateField(blank=True, default=datetime.now())
    fecha_fin = models.DateField(validators=[validate_even])
    #plazo = models.IntegerField(blank=True, null=True)
    #lider_proyecto = models.ForeignKey(User)
    #miembros = models.ManyToManyField(User, related_name='proyectos')

    def __unicode__(self):
        return self.nombre

    def delete(self):
        Flujo.objects.filter(proyecto_id=self.idproyecto).delete()
        super(Proyecto, self).delete()

    class Meta:
        app_label = 'adm'


class Flujo(models.Model):
    id_flujo = models.AutoField(primary_key=True)
    proyecto = models.ForeignKey(Proyecto, related_name='flujos')
    nombre_flujo = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    estado_flujo = models.CharField(max_length=11, choices=FLUJOS_ESTADOS, default='NO-INICIADA')
    numero_secuencia = models.IntegerField(blank=True)
    #tipo_item = models.ManyToManyField('des.TipoItem', blank=True)

    class Meta:
        app_label = 'adm'

    def __unicode__(self):
        return self.nombre_flujo

    #Para aumentar el numero por cada flujo creado
    def save(self):
        primera_flujo = False
        primera_flujo = Flujo.objects.filter(numero_secuencia=1, proyecto_id=self.proyecto_id).exists()
        existe_flujo = Flujo.objects.filter(id_flujo=self.id_flujo).exists()
        if existe_flujo is False:
            if primera_flujo is True:
                maximo = Flujo.objects.filter(proyecto_id=self.proyecto_id).aggregate(Max('numero_secuencia'))['numero_secuencia__max']
                numero_secuencia = Flujo.objects.get(proyecto_id=self.proyecto_id, numero_secuencia=maximo)
                top = numero_secuencia.numero_secuencia + 1
                self.numero_secuencia = top
            else:
                self.numero_secuencia = 1
                self.estado_flujo = 'ABIERTO'

        super(Flujo, self).save()
        return Flujo

class Rol(models.Model):

    id_rol = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    permisos = models.ForeignKey(PermisosProyecto)
    nombre = models.CharField(max_length=200)
    def __unicode__(self):
        return self.nombre
    class Meta:
        app_label = 'adm'