---
title: "CSV chart"
author: "Cheap and Fair team"
description: "Demo data repository"
date_created: "2024-09-26"
---


<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>

<canvas id="chart"></canvas>

<script type="text/javascript">
      const queryString = window.location.search;
      console.log(queryString);
      const searchParams = new URLSearchParams(queryString);
      csv_url = searchParams.get("csv");
      console.log(csv_url);
      
      CHART =  document.getElementById('chart');
      var request = new XMLHttpRequest();
      request.onreadystatechange = function() {
	  if (this.readyState == 4 && this.status == 200) {
	      const csv = request.responseText;
	      var lines = csv.split("\n");
	      var column_labels = lines[0].split(",");
	      console.log(column_labels);
	      var csv_data_rows = {};

	      for(var i = 0; i < column_labels.length; i++){
		  csv_data_rows[column_labels[i]] = [];
	      };

	      for(var i = 1; i < lines.length; i++){
		  var currentline = lines[i].split(",");
		  for(var j=0; j < column_labels.length; j++){
		      csv_data_rows[[column_labels[j]]].push(Number(currentline[j]));
		  }
	      }
	      
	      const cfg = {
		  type: 'line',
		  data: {
		      labels: csv_data_rows[column_labels[0]],
		      datasets: [{
			  label: column_labels[1],
			  data: csv_data_rows[column_labels[1]]
		      }]
		  },
		  options: {
		      scales: {
			  y: {
			     display: true,
			      type: 'logarithmic',
			  }
		      }
		  }
	      }
	      
	      new Chart(CHART, cfg);
	  }
      };
      request.open("GET", csv_url, true);
      request.send();
</script>
