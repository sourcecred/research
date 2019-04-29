import ipywidgets as widgets
from traitlets import Unicode
from traitlets import default
from traitlets import List

class scForceChart(widgets.DOMWidget):

    _view_name = Unicode('scForceChartView').tag(sync=True)
    _model_name = Unicode('scForceChartModel').tag(sync=True)
    _view_module = Unicode('source_cred_chart').tag(sync=True)
    _model_module = Unicode('source_cred_chart').tag(sync=True)
    _model_data = List([]).tag(sync=True)
    
    @default('layout')
    def _default_layout(self):
        return widgets.Layout(height='400px', align_self='stretch')

    def set_data(self, js_data):
        self._model_data = js_data