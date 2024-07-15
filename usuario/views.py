from django.shortcuts import render, redirect
from .models import Usuario,  ComentarioForo
from .forms import LoginForm, RegisterForm, ComentarioFormForo, CambiarNombreForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from catalogo.models import Genero, Catalogo_Entretenimiento, DetallesCatalogo, Director, Tipo, Genero, Comentario, Historial
from datetime import datetime, timedelta
from catalogo.forms import ComentarioForm
from django.utils import timezone
from django.db.models import Avg, Count, Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import RecuperarContraseñaForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            contraseña = form.cleaned_data['contraseña']
            try:
                usuario = Usuario.objects.get(nombre=nombre)
                if usuario.contraseña == contraseña: 
                    request.session['usuario_id'] = usuario.id  
                    return redirect('home') 
                else:
                    form.add_error('contraseña', 'Nombre de usuario o contraseña incorrectos')
            except Usuario.DoesNotExist:
                form.add_error('nombre', 'Usuario no encontrado')
    else:
        form = LoginForm()
    return render(request, 'usuario/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige al login después de registrar
    else:
        form = RegisterForm()
    return render(request, 'usuario/register.html', {'form': form})

def logout_view(request):
    request.session.flush() 
    return redirect('login') 

def home_view(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)
    return render(request, 'usuario/home.html', {'user': usuario})

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

    return render(request, 'usuario/catalogos.html', context)



def detalle_catalogo(request, pk):
    catalogo = get_object_or_404(Catalogo_Entretenimiento, pk=pk)
    detalles = DetallesCatalogo.objects.filter(catalogo=catalogo)
    comentarios = Comentario.objects.filter(catalogo=catalogo).order_by('-fecha')

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            usuario_id = request.session.get('usuario_id')
            if usuario_id:
                User = get_user_model()
                usuario = Usuario.objects.get(pk=usuario_id)
                comentario.usuario = usuario
                comentario.catalogo = catalogo
                comentario.save()
                messages.success(request, 'Comentario agregado correctamente.')
                return redirect('detalle_catalogo', pk=catalogo.pk)
            else:
                messages.error(request, 'Debes iniciar sesión para dejar un comentario.')
                return redirect('login')
    else:
        form = ComentarioForm()

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

def foro_view(request):
    if request.method == 'POST':
        form = ComentarioFormForo(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            usuario_id = request.session.get('usuario_id')
            if usuario_id:
                comentario.usuario = Usuario.objects.get(pk=usuario_id)
                comentario.save()
                return redirect('foro')
    else:
        form = ComentarioFormForo()

    comentarios = ComentarioForo.objects.all().order_by('-fecha_creacion')
    return render(request, 'usuario/foro.html', {'form': form, 'comentarios': comentarios})

def perfil_view(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)
        show_form = request.GET.get('show_form') == 'true'
        
        if request.method == 'POST':
            form = CambiarNombreForm(request.POST, instance=usuario)
            if form.is_valid():
                form.save()
                messages.success(request, 'Nombre de usuario cambiado exitosamente.')
                return redirect('perfil')
        else:
            form = CambiarNombreForm(instance=usuario)

        return render(request, 'usuario/perfil.html', {
            'usuario': usuario, 
            'form': form, 
            'show_form': show_form
        })
    else:
        return redirect('login')
    

def reciente(request):
    recientes = Catalogo_Entretenimiento.objects.order_by('-fecha_lanzamiento')[:6]
    context = {
        'recientes': recientes
    }
    return render(request, 'usuario/reciente.html', context)




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

    return render(request, 'usuario/categorias_por_calificacion.html', context)