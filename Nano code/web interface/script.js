// Manually defined labels for the temperature and battery columns
const labelst = ['Upstairs\t', 'Living room', 'Bedroom\t', 'Kitchen\t'];
const labelsb = ['Upstairs\t', 'Living room', 'Bedroom', 'Kitchen\t'];

// Function to parse CSV data without headers
function parseCSV(data) {
    const lines = data.trim().split("\n");
    const rows = lines.map(line => line.split(","));
    
    const dates = rows.map(row => row[0]);
    const temperatures = labelst.map((label, i) => ({
        label: label,
        data: rows.map(row => parseFloat(row[i + 1]))
    }));

    const batteryLife = labelsb.map((label, i) => ({
        label: label,
        data: rows.map(row => parseFloat(row[i + 5]))
    }));
    
    return { dates, temperatures, batteryLife };
}

// Function to update the recent temperatures and battery life boxes
function updateRecentData(dates, temperatures, batteryLife) {
    const recentTemperaturesList = document.getElementById('recentTemperatures');
    recentTemperaturesList.innerHTML = '';

    const recentBatteryLifeList = document.getElementById('recentBatteryLife');
    recentBatteryLifeList.innerHTML = '';

    // Get the most recent data
    const lastIndex = dates.length - 1;
    // Update the recent temperatures table
    temperatures.forEach(temp => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${temp.label}</td><td>${temp.data[lastIndex]}°C</td>`;
        recentTemperaturesList.appendChild(row);
    });

// Update the recent battery life table
    batteryLife.forEach(battery => {
        batteryPercent = battery.data[lastIndex] - 3.2;
        batteryPercent = Math.round(batteryPercent * 100);
        const row = document.createElement('tr');
        row.innerHTML = `<td>${battery.label}</td><td>${battery.data[lastIndex]}</td><td>(${batteryPercent}%)</td>`;
        recentBatteryLifeList.appendChild(row);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Function to fetch CSV data nd update the chart and info boxes
    function fetchAndUpdateData() {
    // Fetch the CSV file and generate the chart
    fetch('graph2.csv')
    .then(response => response.text())
    .then(csvData => {
        const { dates, temperatures, batteryLife } = parseCSV(csvData);

        // Update the recent data boxes
        updateRecentData(dates, temperatures, batteryLife);

        const ctx = document.getElementById('temperatureChart').getContext('2d');

        // Check if a chart instance already exists and destroy it if it does
        if (window.temperatureChart instanceof Chart) {
            window.temperatureChart.destroy();
        }

        // Fixed colors for the temperature datasets
        const temperatureColors = ['rgba(255,99,132,1)', 'rgba(54,162,235,1)', 'rgba(75,192,192,1)', 'rgba(255,206,86,1)'];

        window.temperatureChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: temperatures.map((temp, index) => ({
                    label: temp.label,
                    data: temp.data,
                    fill: false,
                    borderColor: temperatureColors[index],
                    tension: 0.1
                }))
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Temperature (°C)'
                        }
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error loading the CSV file:', error));
}
fetchAndUpdateData();
setInterval(fetchAndUpdateData, 300000);
});
