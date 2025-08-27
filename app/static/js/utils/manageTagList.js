//load available tags from db to tag list
async function loadTagsFromDB(){
    try {
        const response = await fetch('public/tags')
        const tags = await response.json()

        const datalist = document.getElementById('tagOptions')
        datalist.innerHTML = ''

        tags.forEach(tag => {
            const option = document.createElement('option')
            option.value = tag.name
            option.setAttribute('data-id',tag.id)
            datalist.appendChild(option)
        })
    }catch (e){
        console.error(e)
    }
}
// get id from name
function getTagId(tagName) {
    const options = document.getElementById('tagOptions').options
    for (let option of options) {
        if (option.value === tagName) {
            return option.getAttribute('data-id')
        }
    }
    return null
}
//checks which tags are selected
function updateHiddenTags() {
    const selectedTags = document.querySelectorAll('#selectedTags li');
    const tagIds = Array.from(selectedTags).map(li => li.getAttribute('data-tag-id'));
    document.getElementById('tagsInput').value = JSON.stringify(tagIds); // np. "[1,2,3]"
}
// adds selected tag after clicking button
function addTag(tagName,tagId){
    const selectedTags = document.getElementById('selectedTags')
    selectedTags.innerHTML += `
      <li class="list-inline-item badge tag-badge" data-tag-id="${tagId}">
        ${tagName} <button type="button" class="btn-close btn-close-white btn-sm"></button>
      </li>
    `;
    const allTags=document.getElementById('tagOptions')
    const itemToRemove=allTags.querySelector(`[data-id="${tagId}"]`)
    if (itemToRemove) itemToRemove.remove()
    updateHiddenTags()
}

// after selecting a tag it is then removed from tag options
// removing it from selected tags brings it back to all options

// the following function defines 'x' button on selected tag
// it removes a tag from selected and adds it to list of possible tags
// whilst keeping list of possible tags sorted

document.getElementById('selectedTags').addEventListener('click', function (e) {
    if (e.target.classList.contains('btn-close')) {
        const li = e.target.closest('li')
        const tagName = li.textContent.trim()
        const tagId = li.getAttribute('data-tag-id')

        //remove clicked tag from list
        li.remove()

        // bring it back to list of selectable tags
        const allTags = document.getElementById('tagOptions')

        // find correct index to place
        const options = Array.from(allTags.querySelectorAll('option'));
        let insertIndex = options.length;
        for (let i = 0; i < options.length; i++) {
            if (tagName.localeCompare(options[i].value, "en", { sensitivity: "base" }) < 0) {
                insertIndex = i;
                break;
            }
        }
        const newOption = `<option value="${tagName}" data-id="${tagId}"></option>`
        if (insertIndex === options.length) {
            allTags.innerHTML += newOption
        } else {
            options[insertIndex].insertAdjacentHTML("beforebegin", newOption)
        }
        updateHiddenTags()
    }
})


document.addEventListener('DOMContentLoaded', function() {
    loadTagsFromDB()
    const addButton = document.getElementById('addTagBtn')
    const input = document.getElementById('tags')
    addButton.addEventListener('click', function(){
        const tagValue = input.value.trim()
        const tagId = getTagId(tagValue)
        if(tagValue && tagId){
            input.value = ''
            addTag(tagValue, tagId)

        } else {
            alert('you must select tag from list')
        }
    })
})
