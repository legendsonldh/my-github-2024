const COMMITS_PER_HOUR = eval(document.querySelector('#data-commits-per-hour').innerHTML);
COMMITS_PER_HOUR.push(COMMITS_PER_HOUR[0]);
const COMMITS_PER_WEEKDAY = eval(document.querySelector('#data-commits-per-weekday').innerHTML);
COMMITS_PER_WEEKDAY.push(COMMITS_PER_WEEKDAY[0]);
const COMMITS_PER_MONTH = eval(document.querySelector('#data-commits-per-month').innerHTML);

function get_chart_config(label, labels, data) {
  return {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: label,
        data: data,
        borderWidth: 3,
        fill: true,
        borderColor: '#49a1ff',
        backgroundColor: '#49a1ff20',
        pointBackgroundColor: '#49a1ff',
        pointRadius: 3,
        pointBorderWidth: 0,
        tension: 0.6,
        spanGaps: true
      }]
    },
    options: {
      responsive: false,
      scales: {
        x: {
          display: false
        },
        y: {
          display: false,
          beginAtZero: true
        }
      },
      plugins: {
        legend: {
          display: false
        },
        title: {
          display: false
        }
      }
    }
  }
}

const ctx1 = document.getElementById('commits-per-hour');
new Chart(ctx1, get_chart_config('Commits in Hour', ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00',
  '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00',
  '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '0:00'], COMMITS_PER_HOUR));

const ctx2 = document.getElementById('commits-per-weekday');
new Chart(ctx2, get_chart_config('Activities in Weekday', ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Mon'], COMMITS_PER_WEEKDAY));

const ctx3 = document.getElementById('commits-per-month');
new Chart(ctx3, get_chart_config('Activities in Month', ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], COMMITS_PER_MONTH));