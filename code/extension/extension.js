document.addEventListener('DOMContentLoaded', function() {
  var analyzeButton = document.getElementById('analyzeButton');
  var inputText = document.getElementById('inputText');
  var resultContainer = document.querySelector('.results-container');

  analyzeButton.addEventListener('click', function() {
    analyzeButton.disabled = true;
    inputText.disabled = true;

    var inputValue = inputText.value.trim(); // Trim whitespace
    
    // Check if inputText is empty
    if (inputValue === "") {
      showResult("Enter a URL first.", 1);
      return;
    }

    var regex = /i\.(\d+)\.(\d+)/;
    var match = regex.exec(inputValue);

    if (!match) {
      showResult("URL format is not correct or IDs not found.", 1);
      return;
    }
        
    // Get total reviews
    fetch('http://localhost:5000/total', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: inputValue }),
    })
    .then(response => response.json())
    .then(data => {
      showResult(`Scraping ${data.total} reviews from the URL...`, 0);

      var with_context = data.with_context;
      var name = data.name

      // Scrape reviews from URL
      fetch('http://localhost:5000/scraper', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: inputValue }),
      })
      .then(response => response.json())
      .then(data => {
        showResult(`Successfully scraped ${with_context} reviews with comments. Classifying reviews...`, 0);

        // Classify the scraped reviews
        fetch('http://localhost:5000/classify', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          // body: JSON.stringify({ url: inputText }),
        })
        .then(response => response.json())
        .then(data => {
          var classification = data.quality_category;
          var totalReviews = data.total_count;
          var positiveReviews = data.positive_count;
          var negativeReviews = data.negative_count;
          var positivePercentageFormatted = ((positiveReviews / totalReviews) * 100).toFixed(2);
          var negativePercentageFormatted = ((negativeReviews / totalReviews) * 100).toFixed(2);

          // Create elements for the classification result
          var icon = document.createElement('img');
          switch (classification) {
            case "Poor Quality and Possibly Fraudulent":
              resultContainer.style.backgroundColor = "#e57373"; 
              icon.src = 'assets/bad.png';
              break;
            case "Below Average Quality":
              resultContainer.style.backgroundColor = "#ffb74d"; 
              icon.src = 'assets/bad.png';
              break;
            case "Average Quality":
              resultContainer.style.backgroundColor = "#fff176"; 
              icon.src = 'assets/average.png';
              break;
            case "Above Average Quality":
              resultContainer.style.backgroundColor = "#a5d6a7";
              icon.src = 'assets/good.png';
              break;
            case "Excellent Quality and Legitimate Product":
              resultContainer.style.backgroundColor = "#81c784"; 
              icon.src = 'assets/good.png';
              break;
            case "Excellent Quality with Caution on Legitimacy of Product":
              resultContainer.style.backgroundColor = "#80deea"; 
              icon.src = 'assets/good.png';
              break;
            default:
              resultContainer.style.backgroundColor = "#f0f0f0"; 
              break;
          }
          
          icon.alt = 'Classification Icon';
          icon.classList.add('classification-icon');

          var categoryText = document.createElement('h1');
          categoryText.textContent = `${classification}`;
          categoryText.classList.add('category-text');

          var itemName = document.createElement('h4');
          itemName.textContent = `${name}`;
          itemName.classList.add('item-name');

          var summaryDetails = document.createElement('p');
          summaryDetails.innerHTML = `Summary:<br>${totalReviews} total reviews analyzed<br>${positiveReviews} (${positivePercentageFormatted}%) positive ratings<br>${negativeReviews} (${negativePercentageFormatted}%) negative reviews.`;
          summaryDetails.classList.add('summary-details');

          var downloadButton = document.createElement('button');
          downloadButton.textContent = 'Download csv file';
          downloadButton.classList.add('download-button');

          // Clear previous results and append new elements to the result container
          resultContainer.innerHTML = '';
          resultContainer.appendChild(icon);
          resultContainer.appendChild(categoryText);

          if(totalReviews <= 100){
            var warningText = document.createElement('p');
            warningText.innerHTML = "Not enough reviews to create an accurate classification"
            warningText.classList.add('warning-text');
            resultContainer.appendChild(warningText)
          }

          resultContainer.appendChild(itemName);
          resultContainer.appendChild(summaryDetails);
          resultContainer.appendChild(downloadButton);

          // Show the results container
          resultContainer.style.display = 'block';

          // Event listener for the download button
          downloadButton.addEventListener('click', function() {
            var serverEndpoint = 'http://localhost:5000/download';
            // Send a message to the background script to initiate the download
            chrome.runtime.sendMessage({ action: 'download', url: serverEndpoint });
          });

          analyzeButton.disabled = false;
          inputText.disabled = false;
        })
        .catch(error => {
          showResult("Error classifying the reviews.", 1);
        });
      })
      .catch(error => {
        showResult("Error scraping the reviews from provided URL.", 1);
      });
    })
    .catch(error => {
      showResult("Flask server not detected. Make sure that it is running.", 1);
    });
  });

  function showResult(message, error) {
    resultContainer.style.backgroundColor = "#f0f0f0"; 

    // Create and append a paragraph element with the message
    var resultDiv = document.createElement('div');
    resultDiv.classList.add('result');
    resultDiv.textContent = message;

    // Clear previous results
    resultContainer.innerHTML = '';
    
    // Append the new result
    resultContainer.appendChild(resultDiv);
    resultContainer.style.display = 'block'; // Show the results container

    if(error == 1){
      analyzeButton.disabled = false;
      inputText.disabled = false;
    }
  }
});
