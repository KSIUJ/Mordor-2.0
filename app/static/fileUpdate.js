//TODO remove after debugging
sessionStorage.setItem("selectedFile",1)

const fileId=sessionStorage.getItem("selectedFile")

//TODO: change to my role after implementing it
const role='admin'

//hide unavailable fields
document.addEventListener("DOMContentLoaded", function () {
    if(role!=='admin'){
        document.getElementById('fileStatus').disabled=true
        document.getElementById('changeStatus').hidden=true
    }
})

//submit button function
document.addEventListener("DOMContentLoaded", function (){
    const submitButton=document.getElementById('submit')
    submitButton.addEventListener('click',function (){
        const name=document.getElementById('fileName').value
        const tags=getSelectedTagsIds()
        if(!name){
            alert("Filename field is empty")
            return
        }
        updateFile(tags,name)
    })
})

//change status button (for admin)
document.addEventListener("DOMContentLoaded", function (){
    const statusButton=document.getElementById("changeStatus")
    statusButton.addEventListener('click',function (){
        const newStatus=document.getElementById("fileStatus").value
        changeStatus(newStatus)
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

//func sending update form
async function updateFile(tags,name){
    const formData=new FormData()
    formData.append("file_id",fileId)
    formData.append("tags",JSON.stringify(tags));
    formData.append("name",name)

    //TODO: Include currently logged-in user role
    await fetch(`/test/auth/set-role/${role}`,{
        method: "GET"
    })

    const res=await fetch(`/${role}/update_file`,{
        method: "POST",
        body: formData
    })

    if(!res.ok){
        throw new Error("Update failed")
    }

    window.location.reload();
}

//status changer
async function changeStatus(status) {
    alert(fileId)
    const body={
        file_id: fileId,
        status:status
    }

    //TODO: Include currently logged-in user role
    await fetch(`/test/auth/set-role/${role}`,{
        method: "GET"
    })
    const res=await fetch(`/${role}/change_status`,{
        method: "POST",
        headers: {
                "Content-Type": "application/json",  // ✅ WAŻNE!
        },
        body: JSON.stringify(body)
    })

    if(!res.ok){
        throw new Error("Change failed")
    }

    window.location.reload();
}