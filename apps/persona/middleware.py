from django.shortcuts import redirect

class DocenteMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print('\n-- request user', request.user, ' --')
        print('-- view_func name', view_func.__name__, type(view_func.__name__))
        print('-- view_args', view_args)
        print('-- view_kwargs', view_kwargs, ' --\n')
        print('Anonymous: ', request.user.id)

        if 'PersonaCreateView' in view_func.__name__:
            if request.user.id is None or request.user.is_staff is False:
                return redirect('/')

        rutas_pk = [
            'PersonaUpdateView',
            'ExperienciaLaboralView',
            'FormacionAcademicaView',
            'IdiomaCreateView',
            'CientificaView',
            'DistincionView',
            'cursos_create_view',
            'ExportarCVView'
        ]

        if view_func.__name__ in rutas_pk:
            if request.user.id is None:
                return redirect('/')
            if request.user.is_staff is False and request.user.persona_id != int(view_kwargs.get('pk')):
                return redirect('persona:editar_persona', pk=request.user.persona_id)