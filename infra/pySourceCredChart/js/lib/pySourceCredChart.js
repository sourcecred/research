var widgets = require('@jupyter-widgets/base');
require('../style/pySourceCredChart.css');

import * as d3 from 'd3';

/// set constants
const MAX_SIZE_PIXELS = 200

var sourceCredChartModel = widgets.DOMWidgetModel.extend({
	defaults:_.extend(_.result(this, 'widgets.DOMWidgetModel.prototype.defaults'),{
		_model_name: 'sourceCredChartModel',
		_view_name: 'sourceCredChartView',
		_model_module: 'pySourceCredChart',
		_view_module: 'pySourceCredChart',
	})
});

var sourceCredChartView = widgets.DOMWidgetView.extend({
	
	render: function(){
		const that = this;
		
		this.chartContainer = d3.select(this.el);
		
		setScaffolding(that);
		
		const message = new Promise(function(resolve, reject){
			resolve(that.model.get('_model_msg'))
		});
		
		message
			.then(this.message_changed())
			.catch(function(err){
				console.log(err); 
				});
		
		this.model.on('change:_model_msg', this.message_changed, this);
	},
	
	message_changed: function(){
		this.el.msg = this.model.get('_model_msg');
		this.draw(this.el.msg[0]);
	},
	
	draw: function(opts){
		const that = this;


		this.data = opts.data;
		this.scores = opts.scores;
		this.mapping = opts.mapping;
		this.options = opts.options;
		
		this.links = this.data[this.mapping.edges];
		if(that.mapping.source){
			this.links.forEach(function(d){
				d.source = d[that.mapping.source];
				d.target = d[that.mapping.target];
			});
		}
    
		this.nodes = this.data[this.mapping.nodes];
		
		this.simulation = _simulation(that, this.nodes, this.links);
    
		updateNodes(that, this.nodes);
		updateEdges(that, this.links);		
		
		that.simulation.nodes(this.nodes);
		that.simulation.force("link").links(this.links);
		that.simulation.alpha(1).restart();
	}
	
});
	
	/// d3 based calculations; should work for both this library and React+d3 UI	
	function _radius(that, d){
		if(that.scores){
			// Use the square of the score as radius, so area will be proportional to score (if score available).
			// For the Python implementation, the scores are separate from the node so we use the node index to
			// find the score.
			const _maxScore = d3.max(that.scores);
			const score = that.scores[d.index];
			const r = Math.sqrt((score / _maxScore) * MAX_SIZE_PIXELS) + 3;
			
			if (!isFinite(r)) {
				return 0;
				}
				return r;
				} else {
					return 5
					} 
		
		}
	
	function _simulation(that, nodes, links){
		
		const linkForce = d3.forceLink(links)
			//.id((d) => d.address)
			.distance(120);
			
		const nodeCharge = d3.forceManyBody().strength(-380);
		
		const nodeCollide = d3.forceCollide().radius((d) => {
			 _radius(that,d);
		});
			
		 const simulation = d3.forceSimulation(nodes)
			.force("charge", nodeCharge)
			.force("link", linkForce)
			.force("collide", nodeCollide)
			.force("x", d3.forceX())
		    .force("y", d3.forceY())
		    .alphaTarget(0.02)
		    .alphaMin(0.01)
		    .on("tick", ticked);
			
		function ticked(){
			that.node
				.selectAll('.node')
				.attr("cx", (d) =>  d.x )
				.attr("cy", (d) => d.y )
				
			//TODO: fix arrow marker by moving back based on the node radius
			that.edge
				.selectAll('.edge')
				.attr("x1", (d) => d.source.x )
				.attr("y1", (d) => d.source.y )
				.attr("x2", (d) => d.target.x )
				.attr("y2", (d) => d.target.y );
			}
			
		return simulation
	}
	
	/// d3 based DOM functions; trying to mimic React Components
	function setScaffolding(that){
		
		//TODO: find a better way to assert width/height in Jupyter Notebook
		that.width = 800;
		that.height = 600;
		
		that.chartContainer.innerHTML = '';
		that.svg = that.chartContainer.append('svg');
		that.svg.attr('width', that.width);
		that.svg.attr('height', that.height);
		that.chart = that.svg
			.append("g")
			.attr("transform", "translate(" + that.width / 2 + "," + that.height / 2 + ")")
			
		that.chart.append("defs").append("marker")
				.attr("id", "arrow")
				.attr("viewBox", "0 -3 10 10")
				.attr("refX", 18)
				.attr("refY", 0)
				.attr("markerWidth", 5)
				.attr("markerHeight", 5)
				.attr("orient", "auto")
				.append("svg:path")
				.attr("d", "M 0,-5 L 10 ,0 L 0,5");   
		
		that.edge = that.chart.append("g");
		that.node = that.chart.append("g");
		
		that.tooltip = that.chartContainer.append("div")
			.attr("class", "toolTip")
			.style('display', 'none')
			.style('position', 'absolute')
			.style('min-width' , '50px')
			.style('height', 'auto')
			.style('background', 'none repeat scroll 0 0 #ffffff');
	}
	
	function updateNodes(that, nodes){
		
		const nodeColor = d3.scaleOrdinal(d3.schemeCategory10);
		const node = that.node.selectAll(".node").data(nodes);
	
		node.exit()
			.transition()
			.ease(d3.easeQuad)
			.duration(1000)
			.remove();

		const newNode = node.enter()
			.append('circle')
			.attr('class', 'node')
			.on('mouseover', mouseOver)
			.on('mouseout', mouseOff)
			.on('click', clickHalo);
       
		node.merge(newNode)
			.transition()
			.ease(d3.easeQuad)
			.duration(1000)
			.attr('fill', (d) => that.mapping.nodeGroup ? nodeColor(d[that.mapping.nodeGroup]) : 'steelblue')
			.attr('r', (d) => _radius(that, d));
			
		function mouseOver(){
			const data = d3.select(this).data()[0];
			const textDisplay = data['index'] + '<br>' + data[that.mapping.nodeLabel] + '<br>' + data[3] + '<br>' + data[4] ;
			const nodeColor = d3.select(this).style('fill');
			
			that.tooltip
			  .style("left", (d3.event.pageX - 250) + 'px')
			  .style("top", 0 + 'px')
			  .style("display", "inline")
			  .style("background", nodeColor)
			  .html(() => textDisplay );
		}
		
		function mouseOff(){
			that.tooltip.style("display", "none");
		}
		
		function clickHalo(){

			that.svg.selectAll('circle').attr('class', 'node');
			that.svg.selectAll('line').attr('class', 'edge');
			
			const nodeIdx = d3.select(this).data()[0].index;
			console.log(nodeIdx);
			
			d3.select(this).attr('class', 'halo');
			
			const links = that.svg.selectAll(".edge").filter((d) => (d.dstIndex == nodeIdx | d.srcIndex == nodeIdx));
			links.attr('class', 'halo');
		}
	}
	
	function updateEdges(that, links){
		
		const edgeColor = d3.scaleOrdinal(d3.schemeCategory10);

		const edge = that.edge.selectAll('.edge').data(links);
		
		edge.exit().remove();
		
		const newEdge = edge.enter()
			.append('line')
			.attr('class', 'edge');
		
		edge.merge(newEdge)
			.transition()
			.ease(d3.easeQuad)
			.duration(1000)
			.attr("marker-end", "url(#arrow)")
			.attr('stroke-width', (d) => that.mapping.edgeSize ? d[that.mapping.edgeSize] : 0.25)
			.attr('stroke', (d) => that.mapping.edgeGroup ? edgeColor(d[that.mapping.edgeGroup]) : '#000' );
	}
	
module.exports = {
	sourceCredChartModel: sourceCredChartModel,
	sourceCredChartView: sourceCredChartView
};