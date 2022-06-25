from django.http import HttpResponse
from django.views import View

from reportlab.pdfgen.canvas import Canvas


class PdfView(View):
    filename = ''
    disposition = 'inline'

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = '{}; filename={}'.format(self.disposition, self.filename)
        c = Canvas(response)
        c.setFont('Times-Roman', 11)
        c._doc.setTitle(self.filename)
        c = self.process_canvas(c)
        c.save()
        return response

    def process_canvas(self, _canvas):
        raise NotImplementedError
