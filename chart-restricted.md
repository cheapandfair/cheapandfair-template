---
title: "CSV chart"
author: "Cheap and Fair team"
description: "Demo data repository"
date_created: "2024-09-26"
---


<script src="https://unpkg.com/@globus/sdk/dist/umd/globus.production.js"></script>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js"></script>


This page demonstrates how to plot a CSV file hosted in a Globus Guest Collection with restricted access.

You will need to [join a Globus Group](https://app.globus.org/groups/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/join) to view the sample chart.

<button id="sign-in" style="display: none">Sign In</button>
<button id="sign-out"  style="display: none">Sign Out</button>

<code id="user-information"></code>

<div id="canvas">
<h2>Sample Chart with Restricted Data</h2>
<p>Plotted using <a href="https://www.chartjs.org/docs/latest/getting-started/">Chart.js</a>.</p>
<canvas id="chart"></canvas>
</div>


<script type="text/javascript">
      /* UPDATE: */
      /* Your Collection UUID */
      const collection = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx';
      /* Your new cient ID */
      const client_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx';
      /* The URL of the restricted csv file */
      const redirect_url = 'https://xxxxxxxx.github.io/cheapandfair-template/chart-restricted.html';
      /* The URL of the restricted csv file */
      const csv_url = 'https://xxxxxxxx.c2d0f8.bd7c.data.globus.org/datasets/cmb_spectra/cls.csv';

      globus.logger.setLogger(console);
      globus.logger.setLogLevel('DEBUG');

      const manager = globus.authorization.create({
          /**
           * Your registered Globus Application client ID.
           */
          client: client_id,
          /**
           * The redirect URL for your application.
           * This URL should also be added to your Globus Application configuration.
           */
          redirect: redirect_url,
          scopes: `openid profile email https://auth.globus.org/scopes/${collection}/https`,
          /**
           * This will enable the use of refresh tokens - you probably want this!
           */ 
          useRefreshTokens: true,
      });

      manager.handleCodeRedirect();

      const UI = {
          SIGN_IN: document.getElementById('sign-in'),
          SIGN_OUT: document.getElementById('sign-out'),
          USER_INFO: document.getElementById('user-information'),
	  CANVAS: document.getElementById('canvas'),
	  CHART: document.getElementById('chart'),
      };

      UI.SIGN_IN.addEventListener('click', () => {
          /**
           * This will redirect the user to the Globus Auth login page.
           */
          manager.login();
      });

      UI.SIGN_OUT.addEventListener('click', () => {
          /**
           * This will revoke the user's tokens and clear the stored state.
           */
          manager.revoke();
          // 
          UI.USER_INFO.innerText = '';
          UI.CHART.style.display = 'none';
	  UI.CANVAS.style.display = 'none';
          UI.SIGN_OUT.style.display = 'none';
	  UI.SIGN_IN.style.display = 'block';
      });


      if (manager.authenticated) {
          UI.USER_INFO.innerText = `Welcome, ${manager.user.name}!`;
          UI.SIGN_OUT.style.display = 'block';
	  UI.CANVAS.style.display = 'block';
	  
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

	           new Chart(UI.CHART, cfg);
	      }
      	  };
          request.onloadend = function() {
              if(request.status == 403) {
		console.log('Not authorized for the data, got a 403');
		UI.USER_INFO.innerText = `${manager.user.name}, you are not authorized to load the data. Did you join the the necessary Globus Group?`;
      	UI.CHART.style.display = 'none';
		UI.CANVAS.style.display = 'none';
	    };
	  };
          request.open("GET", csv_url, true);
	  request.setRequestHeader('Authorization', `Bearer ${manager.tokens.gcs(collection).access_token}`);      
          request.send();
      } else {
          UI.SIGN_IN.style.display = 'block';
	  UI.CHART.style.display = 'none';
	  UI.CANVAS.style.display = 'none';
      }
</script>
