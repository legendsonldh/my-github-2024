const TOP_3_MOST_COMMITTED_REPOS = eval(document.querySelector('#data-top-3-most-committed-repos').innerHTML)
const TOP_3_LANGUAGES_USED_IN_NEW_REPOS = eval(document.querySelector('#data-top-3-languages-used-in-new-repos').innerHTML)
const TOP_3_CONVENTIONAL_COMMIT_TYPES = eval(document.querySelector('#data-top-3-conventional-commit-types').innerHTML)

function generateRanking(insertPlace, data) {
    const maxNum = Math.max(...data.map(item => item.num))
    const normalizedNum = data.map(item => item.num / maxNum)

    const item = data[0]
    insertPlace.innerHTML += `
        <span class="first">${item.name}</span>
        <progress value="${item.num}" max="${maxNum}" style="opacity:${normalizedNum[0]}"></progress>
    `

    for (let i = 1; i < data.length; i++) {
        const item = data[i]
        insertPlace.innerHTML += `
            <span>${item.name}</span>
            <progress value="${item.num}" max="${maxNum}" style="opacity:${normalizedNum[i]}"></progress>
        `
    }
}

generateRanking(document.querySelector('#top-3-most-committed-repos'), TOP_3_MOST_COMMITTED_REPOS)
generateRanking(document.querySelector('#top-3-languages-used-in-new-repos'), TOP_3_LANGUAGES_USED_IN_NEW_REPOS)
generateRanking(document.querySelector('#top-3-conventional-commit-types'), TOP_3_CONVENTIONAL_COMMIT_TYPES)
