const YEAR = eval(document.querySelector('#data-year').innerHTML)
const COMMITS_PER_DAY = eval(document.querySelector('#data-commits-per-day').innerHTML)


const firstDay = new Date(YEAR, 0, 1).getDay()


const isLeapYear = (YEAR % 4 === 0 && YEAR % 100 !== 0) || (YEAR % 400 === 0)
const daysInYear = isLeapYear ? 366 : 365


const rows = 7
const columns = Math.ceil((daysInYear + firstDay) / rows)


const sqrtCommits = COMMITS_PER_DAY.map(commit => Math.sqrt(commit + 1) - 1)
const maxSqrtCommits = Math.max(...sqrtCommits)
const normalizedCommits = sqrtCommits.map(commit => commit / maxSqrtCommits)

const commitMap = document.querySelector('#commit-map')
const commitMapTable = commitMap.querySelector('table')


for (let i = 0; i < rows; i++) {
  const tr = document.createElement('tr')
  commitMapTable.appendChild(tr)
  for (let j = 0; j < columns; j++) {
    const td = document.createElement('td')
    const day = i + j * rows - firstDay + 1
    if (day > 0 && day <= daysInYear) {
      const opacity = normalizedCommits[day - 1]
      td.style.opacity = opacity
    } else {
      td.style.opacity = 0
    }
    tr.appendChild(td)
  }
}
