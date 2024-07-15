from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Genero, Catalogo_Entretenimiento, DetallesCatalogo, Director, Tipo, Genero, Comentario, Historial
from datetime import datetime, timedelta
from .forms import ComentarioForm
from django.utils import timezone
from django.db.models import Avg, Count, Q

def index(request):
    # Obtener los filtros del GET
    director_filter = request.GET.get('director')
    tipo_filter = request.GET.get('tipo')
    genero_filter = request.GET.get('genero')
    fecha_lanzamiento_filter = request.GET.get('fecha_lanzamiento')
    query = request.GET.get('q')  # Nuevo: Obtener la consulta de búsqueda

    # Filtrar según los parámetros recibidos
    catalogos = Catalogo_Entretenimiento.objects.all()  # Ajusta esto según tu modelo de catálogos

    if query:
        catalogos = catalogos.filter(titulo__icontains=query)
        
    if director_filter:
        catalogos = catalogos.filter(director_id=director_filter)

    if tipo_filter:
        catalogos = catalogos.filter(tipo_id=tipo_filter)

    if genero_filter:
        catalogos = catalogos.filter(genero_id=genero_filter)

    if fecha_lanzamiento_filter:
        # Convertir la fecha a formato DateTime si es necesario
        try:
            fecha_lanzamiento_filter = datetime.strptime(fecha_lanzamiento_filter, "%Y-%m-%d")
            # Ajustar el rango de fechas para abarcar todo el día
            fecha_lanzamiento_siguiente = fecha_lanzamiento_filter + timedelta(days=1)
            # Filtrar entre la fecha de inicio y el día siguiente
            catalogos = catalogos.filter(fecha_lanzamiento__gte=fecha_lanzamiento_filter, 
                                         fecha_lanzamiento__lt=fecha_lanzamiento_siguiente)
        except ValueError:
            pass  # Manejo de error si la fecha no está en el formato esperado

    context = {
        'catalogos': catalogos,
        'directores': Director.objects.all(),
        'tipos': Tipo.objects.all(),
        'generos': Genero.objects.all(),
        'director_filter': director_filter,
        'tipo_filter': tipo_filter,
        'genero_filter': genero_filter,
        'fecha_lanzamiento_filter': fecha_lanzamiento_filter,
        'query': query  # Pasar la consulta de búsqueda al contexto
    }

    return render(request, 'catalogo/catalogos.html', context)

def detalle_catalogo(request, pk):
    catalogo = get_object_or_404(Catalogo_Entretenimiento, pk=pk)
    detalles = DetallesCatalogo.objects.filter(catalogo=catalogo)
    comentarios = Comentario.objects.filter(catalogo=catalogo).order_by('-fecha')

    # Registrar la visita en el historial
    if request.user.is_authenticated:
        Historial.objects.create(usuario=request.user, catalogo=catalogo)
    
    # Agregar calificación si se envía un comentario
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.catalogo = catalogo
            comentario.usuario = request.user
            comentario.save()
            return redirect('detalle_catalogo', pk=catalogo.pk)
    else:
        form = ComentarioForm()

    # Calcular estadísticas de calificación
    calificaciones = Comentario.objects.filter(catalogo=catalogo).aggregate(
        promedio_calificacion=Avg('calificacion'),
        count_1=Count('calificacion', filter=Q(calificacion=1)),
        count_2=Count('calificacion', filter=Q(calificacion=2)),
        count_3=Count('calificacion', filter=Q(calificacion=3)),
        count_4=Count('calificacion', filter=Q(calificacion=4)),
        count_5=Count('calificacion', filter=Q(calificacion=5)),
        total_reviews=Count('calificacion')
    )

    context = {
        'catalogo': catalogo,
        'detalles': detalles,
        'comentarios': comentarios,
        'form': form,
        'promedio_calificacion': calificaciones['promedio_calificacion'],
        'count_1': calificaciones['count_1'],
        'count_2': calificaciones['count_2'],
        'count_3': calificaciones['count_3'],
        'count_4': calificaciones['count_4'],
        'count_5': calificaciones['count_5'],
        'total_reviews': calificaciones['total_reviews']
    }
    return render(request, 'usuario/detalle_catalogo.html', context)


# catalogo/views.py
def reciente(request):
    recientes = Catalogo_Entretenimiento.objects.order_by('-fecha_lanzamiento')[:6]
    context = {
        'recientes': recientes
    }
    return render(request, 'catalogo/reciente.html', context)




from django.shortcuts import render, get_object_or_404, redirect
from .forms import RecuperarContraseñaForm
from .models import Usuario

def recuperar_contraseña(request):
    usuario = None
    if request.method == 'POST':
        form = RecuperarContraseñaForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            respuesta_seguridad = form.cleaned_data['respuesta_seguridad']
            try:
                usuario = Usuario.objects.get(nombre=nombre, respuesta_seguridad=respuesta_seguridad)
            except Usuario.DoesNotExist:
                form.add_error(None, 'Nombre de usuario o respuesta de seguridad incorrecta')
    else:
        form = RecuperarContraseñaForm()

    return render(request, 'catalogo/recuperar_contraseña.html', {'form': form, 'usuario': usuario})





from .models import Catalogo_Entretenimiento

def categorias_por_calificacion(request):
    catalogos = None
    calificacion_seleccionada = None
    
    if request.method == 'POST':
        calificacion_seleccionada = int(request.POST.get('calificacion'))
        catalogos = Catalogo_Entretenimiento.objects.annotate(
            calificacion_promedio=Avg('comentario__calificacion')
        ).filter(comentario__calificacion=calificacion_seleccionada).order_by('-calificacion_promedio')
    else:
        catalogos = Catalogo_Entretenimiento.objects.annotate(
            calificacion_promedio=Avg('comentario__calificacion')
        ).order_by('-calificacion_promedio')

    context = {
        'catalogos': catalogos,
        'calificacion_seleccionada': calificacion_seleccionada,
    }

    return render(request, 'catalogo/categorias_por_calificacion.html', context)
