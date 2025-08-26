//TODO: change to my role after implementing it
const role = 'user'

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

    const res=await fetch(`/${role}/upload`,{
        method: "PUT",
        body: formData
    })

    if(!res.ok){
        throw new Error("Upload failed")
    }

    window.location.reload();
}