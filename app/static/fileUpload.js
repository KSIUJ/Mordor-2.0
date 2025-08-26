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
//adds selected tag after clicking button
function addTag(tagName,tagId){
    const selectedTags = document.getElementById('selectedTags')

    const li = document.createElement('li')
    li.className='list-inline-item badge bg-primary'
    li.setAttribute('data-tag-id',tagId)
    li.innerHTML = `${tagName} <button type="button" class="btn-close btn-close-white btn-sm"></button>`
    const allTags=document.getElementById('tagOptions')

    li.querySelector('button').addEventListener('click', function(){
        //delete tag from selected

        const tagName = li.textContent.trim()
        const tagId = li.getAttribute('data-tag-id')

        li.remove()

        const allTags = document.getElementById('tagOptions')
        const newOption = document.createElement('option')
        newOption.value = tagName
        newOption.setAttribute('data-id', tagId)

        // get all items
        const options = Array.from(allTags.querySelectorAll('option'))
        let insertIndex = 0

        // find correct index
        for (let i = 0; i < options.length; i++) {
            if (tagName.localeCompare(options[i].value, "en", { sensitivity: "base" }) < 0) {
                allTags.insertBefore(newOption, options[i])
                break
            }
            insertIndex = i + 1
        }

        // insert at end
        if (insertIndex === options.length) {
            allTags.appendChild(newOption)
        }
    })

    selectedTags.appendChild(li)
    const itemToRemove=allTags.querySelector(`[data-id="${tagId}"]`)
    itemToRemove.remove()

}

document.addEventListener('DOMContentLoaded', function() {
    loadTagsFromDB()
    const addButton = document.getElementById('addTagBtn')
    const input = document.getElementById('tags')
    addButton.addEventListener('click', function(){
        const tagValue = input.value.trim()
        const tagId = getTagId(tagValue)
        //input.value = ''
        if(tagValue && tagId){
            input.value = ''
            addTag(tagValue, tagId)

        } else {
            alert('you must select tag from list')
        }
    })
})
function getSelectedTagsIds(){
    const selectedTags = document.querySelectorAll('#selectedTags li[data-tag-id]')
    const tagIds=[]
    selectedTags.forEach(tag => {
        tagIds.push(tag.getAttribute('data-tag-id'))
    })
    return tagIds
}

document.addEventListener("DOMContentLoaded", function (){
    const submitButton=document.getElementById('submit')
    submitButton.addEventListener('click',function (){
        const name=document.getElementById('fileName').value
        const tags=getSelectedTagsIds()
        const file=document.getElementById('uploadedFile').files[0]
        if(!name){
            alert("Filename field is empty")
            return
        }
        if(!file){
            alert("No file included")
            return
        }
        uploadFile(file,tags,name)

    })
})

async function uploadFile(file,tags,name){
    const formData=new FormData()
    formData.append("file",file)
    formData.append("tags",JSON.stringify(tags));
    formData.append("name",name)
    //TODO: Include currently logged-in user role
    await fetch("/test/auth/set-role/user",{
        method: "GET"
    })

    const res=await fetch("/user/upload",{
        method: "PUT",
        body: formData
    })

    if(!res.ok){
        throw new Error("Upload failed")
    }

    window.location.reload();
}