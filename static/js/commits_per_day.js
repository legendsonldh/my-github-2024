const YEAR = eval(document.querySelector('#data-year').innerHTML)
const COMMITS_PER_DAY = eval(document.querySelector('#data-commits-per-day').innerHTML)

// 计算第一天是周几
const firstDay = new Date(YEAR, 0, 1).getDay()

// 计算一年有多少天
const isLeapYear = (YEAR % 4 === 0 && YEAR % 100 !== 0) || (YEAR % 400 === 0)
const daysInYear = isLeapYear ? 366 : 365

// 计算表格要画多少列
const rows = 7
const columns = Math.ceil((daysInYear + firstDay) / rows)

// 计算 COMMITS_PER_DAY 的最大值
const logCommits = COMMITS_PER_DAY.map(commit => Math.log(commit + 1))
const maxLogCommits = Math.max(...logCommits)
const normalizedCommits = logCommits.map(commit => commit / maxLogCommits)

const commitMap = document.querySelector('#commit-map')
const commitMapTable = commitMap.querySelector('table')

// 画表格
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
