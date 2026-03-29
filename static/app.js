document.getElementById('stockForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var stockName = document.getElementById('stock_name').value;

    fetch(`/predict?stock_name=${stockName}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                // Display the predicted price
                document.getElementById('predictedPrice').innerText = `Predicted Price: ₹${data.predictedPrice}`;
                document.getElementById('predictionDate').innerText = `Prediction Date: ${data.predictionDate}`;
                document.getElementById('tradingDayName').innerText = `Trading Day: ${data.tradingDayName}`;

                // Display visualizations (you might need to dynamically load images)
                document.getElementById('visualizations').innerHTML = `
                    <img src="/visualization/your_visualization_file.png" alt="Stock Visualization" />
                `;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
