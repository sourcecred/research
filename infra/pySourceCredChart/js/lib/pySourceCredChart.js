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
		var that = this;
		/// set up chart space without data
		this.chartContainer = d3.select(this.el);
		
		// set up scaffolding
		d3setScaffolding(that);
		
		var message = new Promise(function(resolve, reject){
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
		//preserve context for closures
		var that = this;
		
		// parse opts object sent as message
		this.data = opts.data;
		this.scores = opts.scores;
		this.mapping = opts.mapping;
		this.options = opts.options;
		
		//initialize simulation
		///define variables from data for simulation only
		///data updates chart and restarts simulation later
		this.links = this.data[this.mapping.edges];
		if(that.mapping.source){
			this.links.forEach(function(d){
				d.source = d[that.mapping.source];
				d.target = d[that.mapping.target];
			});
		}
    
		this.nodes = this.data[this.mapping.nodes];
		
		/// define simulation object
		this.simulation = _simulation(that, this.nodes, this.links);
    
		// update chart
		// this.addZoom();
		d3updateNodes(that, this.nodes);
		d3updateEdges(that, this.links);		
		
				
		// Update and restart the simulation.
		that.simulation.nodes(this.nodes);
		that.simulation.force("link").links(this.links);
		that.simulation.alpha(1).restart();
		
		function timeIt(){
		  setTimeout(function(){
			console.log("call stop");
			that.simulation.alpha(0).restart();
			that.simulation.stop();
			}, 20000);
		}
		timeIt();
	}
	
});
	
	/// d3 based calculations; should work for both this library and React+d3 UI	
	function _radius(that, d){
		if(that.scores){
			// Use the square of the score as radius, so area will be proportional to score (if score available).
			// For the Python implementation, the scores are separate from the node so we use the node index to
			// find the score.
			const _maxScore = 100;
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
		
		// set link force
		const linkForce = d3.forceLink(links)
			//.id((d) => d.address)
			.distance(120);
			
		// set charge 
		const nodeCharge = d3.forceManyBody().strength(-380);
		
		// set node collide
		const nodeCollide = d3.forceCollide().radius((d) => {
			return _radius(that,d);
		});
			
		//set simulation
		 const simulation = d3.forceSimulation(nodes)
			.force("charge", nodeCharge)
			.force("link", linkForce)
			.force("collide", nodeCollide)
			.force("x", d3.forceX())
		    .force("y", d3.forceY())
		    .alphaTarget(0.02)
		    .alphaMin(0.01)
		    .on("tick", d3ticked);
			
		function d3ticked(){
			that.node.selectAll('.node').attr("cx", function(d) { return d.x; })
					.attr("cy", function(d) { return d.y; })
				
			//TODO: fix arrow marker by moving back based on the node radius
			that.edge.selectAll('.edge').attr("x1", function(d) { return d.source.x; })
				.attr("y1", function(d) { return d.source.y; })
				.attr("x2", function(d) { return d.target.x; })
				.attr("y2", function(d) { return d.target.y; });
			}
			
		return simulation
	}
	
	/// d3 based DOM functions; trying to mimic React Components
	function d3setScaffolding(that){
		
		// define dimensions
		that.width = 800;
		that.height = 600;
		
		// set up parent element and SVG
		that.chartContainer.innerHTML = '';
		that.svg = that.chartContainer.append('svg');
		that.svg.attr('width', that.width);
		that.svg.attr('height', that.height);
		that.chart = that.svg
			.append("g")
			.attr("transform", "translate(" + that.width / 2 + "," + that.height / 2 + ")")
			
		// set up svg defs
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
		
		//chart elements    
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
	
	function d3updateNodes(that, nodes){
		// node data join
		// TODO: add drag behavior
		
		var nodeColor = d3.scaleOrdinal(d3.schemeCategory10);
		var node = that.node.selectAll(".node").data(nodes);

		// node exit	
		node.exit()
			.transition()
			.ease(d3.easeQuad)
			.duration(1000)
			.remove();
			
		//node enter
		var newNode = node.enter()
			.append('circle')
			.attr('class', 'node')
			.on('mouseover', mouseOver)
			.on('mouseout', mouseOff)
			.on('click', clickHalo);
       
		// node update	
		node.merge(newNode)
			.transition()
			.ease(d3.easeQuad)
			.duration(1000)
			.attr('fill', function(d){
				if(that.mapping.nodeGroup){
					return nodeColor(d[that.mapping.nodeGroup]);
				} else {
					return 'steelblue';
				}
			})
			.attr('r', function(d){
				if(that.mapping.nodeSize){
					return Math.min(75,Math.max(1, that.scores[d.index] * 1000));
				} else {
					return 5;
				}
			});
			
		function mouseOver(){
			var data = d3.select(this).data()[0];
			var textDisplay = data['index'] + '<br>' + data[that.mapping.nodeLabel] + '<br>' + data[3] + '<br>' + data[4] ;
			var nodeColor = d3.select(this).style('fill');
			console.log(data);
			
			that.tooltip
			  .style("left", (d3.event.pageX - 250) + 'px')
			  .style("top", 0 + 'px')
			  .style("display", "inline")
			  .style("background", nodeColor)
			  .html(function(){
				  return textDisplay;
			  });
		}
		
		function mouseOff(){
			that.tooltip.style("display", "none");
		}
		
		function clickHalo(){
			//reset classes
			that.svg.selectAll('circle').attr('class', 'node');
			that.svg.selectAll('line').attr('class', 'edge');
			
			//get node index
			var nodeIdx = d3.select(this).data()[0].index;
			console.log(nodeIdx);
			
			//change node class to halo
			d3.select(this).attr('class', 'halo');
			
			//change connected links to class halo
			console.log(that.svg.selectAll(".edge").data()[0]);
			var links = that.svg.selectAll(".edge").filter(function(d){
				console.log(d);
                return (d.dstIndex == nodeIdx | d.srcIndex == nodeIdx);
              });
			links.attr('class', 'halo');
			console.log(links);
		}
	}
	
	function d3updateEdges(that, links){
		
		var edgeColor = d3.scaleOrdinal(d3.schemeCategory10);
		// edge data join
		var edge = that.edge.selectAll('.edge').data(links);
		
		// edge exit
		edge.exit().remove();
		
		// edge enter
		var newEdge = edge.enter()
			.append('line')
			.attr('class', 'edge');
		
		edge.merge(newEdge)
			.transition()
			.ease(d3.easeQuad)
			.duration(1000)
			.attr("marker-end", "url(#arrow)")
			.attr('stroke-width', function(d){
				if(that.mapping.edgeSize){
					return d[that.mapping.edgeSize];
				} else {
					return 0.25;
				}
			})
			.attr('stroke', function(d){
				if(that.mapping.edgeGroup){
					return edgeColor(d[that.mapping.edgeGroup]);
				} else {
					return '#000';
				}
			});
	}
	
	function d3updateHalos(){
		
	}
	
	

module.exports = {
	sourceCredChartModel: sourceCredChartModel,
	sourceCredChartView: sourceCredChartView
};