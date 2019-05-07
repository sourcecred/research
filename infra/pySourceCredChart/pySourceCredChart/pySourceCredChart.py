import ipywidgets as widgets
from traitlets import Unicode
from traitlets import default
from traitlets import List

class sourceCredChart(widgets.DOMWidget):
    _view_name = Unicode('sourceCredChartView').tag(sync = True)
    _model_name = Unicode('sourceCredChartModel').tag(sync = True)	
    _view_module = Unicode('pySourceCredChart').tag(sync = True)
    _model_module = Unicode('pySourceCredChart').tag(sync = True)
    _model_msg = List([]).tag(sync = True)
    _model_data = List([]).tag(sync = True)

    @default('layout')
    def _default_layout(self):
	    return widgets.Layout(height = '400px', align_self = 'stretch')
		
    def set_data(self, js_data):
	    self._model_data = js_data
		
    def set_message(self, js_message):
	    self._model_msg = js_message