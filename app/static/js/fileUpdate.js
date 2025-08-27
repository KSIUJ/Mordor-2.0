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

//change status button (for admin)
document.addEventListener("DOMContentLoaded", function (){
    const statusButton=document.getElementById("changeStatus")
    statusButton.addEventListener('click',function (){
        const newStatus=document.getElementById("fileStatus").value
        changeStatus(newStatus)
    })
})

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